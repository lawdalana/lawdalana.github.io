const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test, before, after } = require('node:test');
const { chromium } = require('playwright');
const v8toIstanbul = require('v8-to-istanbul');
const { root, catalog, startSite } = require('./helpers/slides-site.cjs');

let browser;
let site;
const coverage = [];
before(async () => {
  site = await startSite();
  const executablePath = process.env.SLIDES_BROWSER_PATH || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
  browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
});
after(async () => {
  if (browser) await browser.close();
  if (site) await new Promise(resolve => site.server.close(resolve));
  if (coverage.length) {
    const lines = new Map();
    for (const entry of coverage) {
      const converter = v8toIstanbul(path.join(root, 'assets/js/SlidesDropdown.js'), 0, { source: entry.source });
      await converter.load();
      converter.applyCoverage(entry.functions);
      const report = Object.values(converter.toIstanbul())[0];
      for (const [id, hits] of Object.entries(report.s)) {
        const line = report.statementMap[id].start.line;
        lines.set(line, Boolean(lines.get(line) || hits > 0));
      }
    }
    const covered = [...lines.values()].filter(Boolean).length;
    const percentage = covered / lines.size * 100;
    console.log('SlidesDropdown.js Chromium line coverage: ' + percentage.toFixed(1) + '% (' + covered + '/' + lines.size + ').');
    assert.ok(percentage >= 80, 'dropdown line coverage must be at least 80%');
  }
});

async function visit(t, fixture = 'grouped', width = 1280, base = '') {
  const page = await browser.newPage({ viewport: { width, height: 800 }, ...(width <= 480 ? { isMobile: true, hasTouch: true } : {}) });
  page.setDefaultTimeout(2000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.coverage.startJSCoverage({ resetOnNavigation: false });
  t.after(async () => {
    coverage.push(...(await page.coverage.stopJSCoverage()).filter(entry => entry.url.includes('/assets/js/SlidesDropdown.js')));
    await page.close();
    assert.deepEqual(errors, [], 'browser must have no uncaught JavaScript errors');
  });
  await page.goto(site.url + base + '/?fixture=' + fixture);
  return page;
}

async function expanded(page, value) {
  await page.waitForFunction(expected => document.querySelector('[aria-controls="slides-dropdown-panel"]')?.getAttribute('aria-expanded') === expected, String(value), { timeout: 1500 });
  assert.equal(await page.locator('#slides-dropdown-panel').isVisible(), value);
}

test('desktop hover reveals grouped slide links in catalog order', async t => {
  const page = await visit(t);
  const toggle = page.getByRole('button', { name: 'Slides', exact: true });
  assert.equal(await toggle.count(), 1, 'navbar should expose a Slides disclosure');
  await expanded(page, false);
  await toggle.hover();
  await expanded(page, true);
  assert.deepEqual(await page.locator('.slides-dropdown__heading').allTextContents().then(items => items.map(item => item.trim())), ['AI / ML', 'Data']);
  assert.deepEqual(await page.locator('.slides-dropdown__link').allTextContents().then(items => items.map(item => item.trim())), ['First AI deck', 'Second AI deck', 'Database deck']);
  await page.getByRole('button', { name: 'Outside navigation' }).hover();
  await expanded(page, false);
});

test('empty catalog exposes an honest empty state and no broken deck links', async t => {
  const page = await visit(t, 'empty');
  await page.getByRole('button', { name: 'Slides', exact: true }).hover();
  await expanded(page, true);
  assert.match(await page.locator('#slides-dropdown-panel').textContent(), /No slides yet/i);
  assert.equal(await page.locator('.slides-dropdown__link').count(), 0);
});

test('catalog labels are escaped and nonlocal URLs cannot become slide links', async t => {
  const page = await visit(t, 'unsafe');
  await page.getByRole('button', { name: 'Slides', exact: true }).hover();
  await expanded(page, true);
  assert.equal(await page.locator('#slides-dropdown-panel img, #slides-dropdown-panel script').count(), 0);
  assert.deepEqual(await page.locator('.slides-dropdown__link').evaluateAll(links => links.map(link => link.getAttribute('href'))), ['/safe-slides/']);
  assert.match(await page.locator('.slides-dropdown__link').textContent(), /<img src=x onerror=alert\(1\)>/);
});

test('Escape closes without immediately reopening and restores button focus', async t => {
  const page = await visit(t);
  const toggle = page.getByRole('button', { name: 'Slides', exact: true });
  await toggle.hover();
  await page.keyboard.press('Escape');
  await expanded(page, false);
  assert.equal(await toggle.evaluate(element => element === document.activeElement), true);
  await toggle.click();
  await expanded(page, true);
  await page.getByRole('button', { name: 'Outside navigation' }).click();
  await expanded(page, false);
});

test('keyboard focus and Tab reach direct links, then close on focus leaving', async t => {
  const page = await visit(t);
  await page.getByRole('link', { name: 'AI Knowledge', exact: true }).focus();
  await page.keyboard.press('Tab');
  assert.equal(await page.getByRole('button', { name: 'Slides', exact: true }).evaluate(element => element === document.activeElement), true);
  await expanded(page, true);
  await page.keyboard.press('Tab');
  assert.equal(await page.getByRole('link', { name: 'First AI deck', exact: true }).evaluate(element => element === document.activeElement), true);
  await page.getByRole('button', { name: 'Outside navigation' }).focus();
  await expanded(page, false);
});

test('selecting a slide opens its page directly and preserves existing navbar links', async t => {
  const page = await visit(t);
  for (const name of ['Notes', 'Posts', 'AI Knowledge', 'Obs']) assert.equal(await page.getByRole('link', { name, exact: true }).count(), 1);
  await page.getByRole('button', { name: 'Slides', exact: true }).hover();
  await page.getByRole('link', { name: 'First AI deck', exact: true }).click();
  assert.equal(new URL(page.url()).pathname, '/first-slides/');
  assert.equal(await page.getByRole('heading', { name: 'Selected deck' }).count(), 1);
});

test('touch-size menu opens on first tap and closes when hamburger collapses', async t => {
  const page = await visit(t, 'grouped', 390);
  const burger = page.locator('.navbar-burger');
  const toggle = page.getByRole('button', { name: 'Slides', exact: true });
  assert.equal(await toggle.isVisible(), false);
  await burger.tap();
  await toggle.tap();
  await expanded(page, true);
  const bounds = await page.locator('#slides-dropdown-panel').boundingBox();
  assert.ok(bounds.x >= 0 && bounds.x + bounds.width <= 390, 'mobile dropdown must fit viewport');
  await burger.tap();
  await burger.tap();
  await expanded(page, false);
  await toggle.tap();
  await expanded(page, true);
  await page.getByRole('link', { name: 'Second AI deck', exact: true }).tap();
  await page.waitForURL('**/second-slides/');
  assert.equal(new URL(page.url()).pathname, '/second-slides/');
});

test('links respect a site subpath and the panel remains readable in dark mode', async t => {
  const page = await visit(t, 'grouped', 1024, '/garden');
  await page.evaluate(() => document.documentElement.dataset.theme = 'dark');
  await page.getByRole('button', { name: 'Slides', exact: true }).hover();
  await expanded(page, true);
  assert.equal(await page.getByRole('link', { name: 'First AI deck', exact: true }).getAttribute('href'), '/garden/first-slides/');
  const style = await page.locator('#slides-dropdown-panel').evaluate(element => ({ bg: getComputedStyle(element).backgroundColor, text: getComputedStyle(element).color }));
  assert.notEqual(style.bg, style.text);
  const bounds = await page.locator('#slides-dropdown-panel').boundingBox();
  assert.ok(bounds.x >= 0 && bounds.x + bounds.width <= 1024);
  const link = page.getByRole('link', { name: 'First AI deck', exact: true });
  await link.hover();
  const colors = await link.evaluate(element => ({ text: getComputedStyle(element).color, bg: getComputedStyle(element).backgroundColor }));
  const luminance = color => color.match(/[\d.]+/g).slice(0, 3).map(Number).map(value => value / 255).map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4).reduce((sum, value, index) => sum + value * [0.2126, 0.7152, 0.0722][index], 0);
  const levels = [luminance(colors.text), luminance(colors.bg)].sort((a, b) => b - a);
  assert.ok((levels[0] + 0.05) / (levels[1] + 0.05) >= 4.5, 'hovered slide text must remain readable in dark mode');
});

test('the real Latent Lab deck is the first registered menu entry', async () => {
  const slides = await catalog();
  assert.equal(slides[0]?.decks?.[0]?.url, '/latent-ai-slides/');
  assert.ok(slides[0].decks[0].title && slides[0].category);
});

test('the illustrated Latent Lab deck is standalone and contains the requested source', async () => {
  const file = path.join(root, 'latent-ai-slides/index.html');
  assert.ok(fs.existsSync(file), 'Latent Lab presentation should exist');
  const html = fs.readFileSync(file, 'utf8');
  assert.ok(!html.startsWith('---'), 'standalone HTML must not be processed as a Jekyll layout');
  assert.ok((html.match(/class="[^"]*\bslide\b/g) || []).length >= 20, 'reading deck should include at least 20 slides');
  assert.ok((html.match(/<svg\b|<img\b/g) || []).length >= 10, 'deck should contain explanatory visuals');
  assert.ok(html.includes('https://lawdalana.github.io/latent-ai-knowledge-base/'));
  assert.ok(html.includes('deck-stage') && html.includes('1920') && html.includes('1080'));
});

test('deck keyboard controls advance slides and keep one active slide', async t => {
  const page = await visit(t);
  await page.goto(site.url + '/latent-ai-slides/');
  await page.evaluate(() => document.fonts.ready);
  assert.equal(await page.locator('.slide.active').count(), 1);
  const first = await page.locator('.slide.active').textContent();
  await page.keyboard.press('ArrowRight');
  assert.notEqual(await page.locator('.slide.active').textContent(), first);
  assert.equal(await page.locator('.slide.active').count(), 1);
  await page.keyboard.press('ArrowLeft');
  assert.equal(await page.locator('.slide.active').textContent(), first);
});

test('every deck slide fits the fixed stage on desktop and phone', async t => {
  const page = await visit(t);
  await page.goto(site.url + '/latent-ai-slides/');
  await page.evaluate(() => document.fonts.ready);
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: width === 390 ? 844 : 720 });
    await page.waitForFunction(expected => {
      const stage = document.querySelector('.deck-stage').getBoundingClientRect();
      return stage.x >= -1 && stage.y >= -1 && stage.right <= expected + 1;
    }, width);
    const bounds = await page.locator('.deck-stage').boundingBox();
    assert.ok(Math.abs(bounds.width / bounds.height - 16 / 9) < 0.001, 'stage must retain 16:9');
    assert.ok(bounds.x >= -1 && bounds.y >= -1 && bounds.x + bounds.width <= width + 1);
    const total = await page.locator('.slide').count();
    for (let index = 0; index < total; index++) {
      const overflow = await page.locator('.slide.active').evaluate(slide => ({ width: slide.scrollWidth - slide.clientWidth, height: slide.scrollHeight - slide.clientHeight }));
      assert.ok(overflow.width <= 1 && overflow.height <= 1, 'slide ' + (index + 1) + ' must not overflow');
      await page.keyboard.press('ArrowRight');
    }
    await page.keyboard.press('Home');
  }
});
