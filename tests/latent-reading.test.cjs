const assert = require('node:assert/strict');
const fs = require('node:fs');
const { test, before, after } = require('node:test');
const { chromium } = require('playwright');
const { root, startSite } = require('./helpers/slides-site.cjs');

const html = fs.readFileSync(root + '/latent-ai-knowledge-base/index.html', 'utf8');
const data = JSON.parse(html.match(/<script type="application\/json" id="knowledge-data">([\s\S]*?)<\/script>/)[1]);
let site;
let browser;

before(async () => {
  site = await startSite();
  const executablePath = process.env.SLIDES_BROWSER_PATH || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
  browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
});

after(async () => {
  if (browser) await browser.close();
  if (site) await new Promise(resolve => site.server.close(resolve));
});

test('the Markdown learning path matches chapter prose and mathematical sources', () => {
  const markdown = fs.readFileSync(root + '/latent-ai-knowledge-base/knowledge/learning-story.md', 'utf8');
  const includes = text => markdown.includes(text) || markdown.includes(text.replaceAll('|', '\\|'));
  for (const text of [data.story.title, data.story.premise, data.story.finish, ...data.story.baseline]) assert.ok(includes(text), 'overview prose must be synchronized');
  for (const chapter of data.story.chapters) {
    const prose = [chapter.title, chapter.question, chapter.problem, chapter.recap, chapter.takeaway, chapter.bridge,
      chapter.checkpoint.question, chapter.checkpoint.answer, ...Object.values(chapter.tryThis),
      ...chapter.readingGuide.map(item => item.why)];
    for (const section of chapter.sections) {
      prose.push(section.title, ...section.paragraphs);
      for (const equation of section.equations) {
        prose.push(equation.meaning, equation.guide.readAs, equation.guide.takeaway,
          ...Object.values(equation.guide.example).flat(), ...equation.guide.symbols.map(item => item.meaning));
        for (const part of equation.mathParts) if (part.tex) assert.ok(markdown.includes(part.tex), 'LaTeX source must be preserved');
      }
    }
    for (const text of prose) assert.ok(includes(text), 'chapter ' + chapter.topicId + ' differs from Markdown: ' + text);
  }
});

async function visit(t, width, route = '') {
  const page = await browser.newPage({ viewport: { width, height: 844 } });
  page.setDefaultTimeout(3000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => {
    if (['error', 'warning'].includes(message.type())) errors.push(message.text());
  });
  t.after(async () => {
    await page.close();
    assert.deepEqual(errors, [], 'reading pages must have no console errors or warnings');
  });
  await page.goto(site.url + '/latent-ai-knowledge-base/' + route);
  await page.evaluate(() => document.fonts.ready);
  return page;
}

for (const width of [1280, 390, 320]) {
  test('tensor dimensions remain inline and readable at ' + width + 'px', async t => {
    const page = await visit(t, width);
    const formulas = await page.locator('.story-reading-note li .math-inline').evaluateAll(elements => elements.map(element => {
      const style = getComputedStyle(element);
      const mathml = element.querySelector('.katex-mathml');
      return {
        display: style.display,
        height: element.getBoundingClientRect().height,
        fontSize: parseFloat(style.fontSize),
        mathmlClip: getComputedStyle(mathml).clipPath,
        glyphDisplays: [...element.querySelectorAll('.mord, .mbin, .mopen, .mclose')].map(glyph => getComputedStyle(glyph).display)
      };
    }));
    assert.ok(formulas.length >= 2, 'baseline must explain matrix input and output dimensions');
    for (const formula of formulas) {
      assert.equal(formula.display, 'inline-block', 'prose styles must not turn math into blocks');
      assert.ok(formula.height < formula.fontSize * 2, 'a simple shape must fit one line');
      assert.notEqual(formula.mathmlClip, 'none', 'MathML must remain available without a visible duplicate');
      assert.ok(formula.glyphDisplays.every(display => display === 'inline'), 'math symbols must not stack vertically');
    }
  });

  test('chapter explanations and article reader remain legible at ' + width + 'px', async t => {
    const page = await visit(t, width, '#story/01');
    const sizes = await page.evaluate(() => {
      const size = selector => parseFloat(getComputedStyle(document.querySelector(selector)).fontSize);
      return {
        paragraph: size('.technical-section > p'),
        example: size('.equation-example li'),
        definition: size('.story-terms dd'),
        question: size('.story-checkpoint p')
      };
    });
    assert.ok(sizes.paragraph >= 18, 'main article text needs at least 18px');
    for (const key of ['example', 'definition', 'question']) assert.ok(sizes[key] >= 16, key + ' needs at least 16px');
    await page.locator('.technical-sources a').first().click();
    await page.waitForSelector('#reader[open]');
    const readerFont = await page.locator('#reader-content').evaluate(element => parseFloat(getComputedStyle(element).fontSize));
    assert.ok(readerFont >= 18, 'full articles must use the same readable body size');
    assert.equal(await page.locator('.reader-file-link').getAttribute('href'), data.posts.find(post => post.id === data.story.chapters[0].postIds[0]).file);
    await page.keyboard.press('Escape');
    await page.waitForSelector('#reader', { state: 'hidden' });
  });

  test('all chapters preserve equations, source links and viewport bounds at ' + width + 'px', async t => {
    const page = await visit(t, width);
    for (const chapter of data.story.chapters) {
      await page.goto(site.url + '/latent-ai-knowledge-base/#story/' + chapter.topicId);
      await page.waitForSelector('.story-heading h1');
      assert.equal(await page.locator('.story-heading h1').textContent(), chapter.title);
      assert.equal(await page.locator('.katex-error').count(), 0);
      const equations = chapter.sections.flatMap(section => section.equations.map(equation => equation.expression));
      assert.deepEqual(await page.locator('.equation-display').evaluateAll(elements => elements.map(element => element.dataset.equationSource)), equations);
      assert.deepEqual(await page.locator('.technical-sources a').evaluateAll(elements => elements.map(element => element.getAttribute('href'))), chapter.postIds.map(id => '#post/' + id));
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert.ok(overflow <= 1, 'chapter ' + chapter.topicId + ' must not overflow the page');
    }
  });
}
