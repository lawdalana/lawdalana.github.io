/* Run with the same cached Playwright dependency as scripts/test-slides.sh.
 * QUANTIZATION_BASE_URL points to a built Jekyll preview or the published site.
 * Optional QUANTIZATION_REPORT_DIR saves screenshots and JSON verification.
 */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const base = process.env.QUANTIZATION_BASE_URL || 'http://127.0.0.1:8874';
const reportDir = process.env.QUANTIZATION_REPORT_DIR;
const routes = ['/notes/gsq-gumbel-softmax-quantization', '/notes/rco-riemannian-constrained-optimization'];

(async () => {
  if (reportDir) fs.mkdirSync(reportDir, {recursive:true});
  const browser = await chromium.launch({headless:true});
  const report = [];
  const assets = new Set();
  try {
    for (const viewport of [{width:1440,height:1000}, {width:390,height:844}]) {
      for (const [index,route] of routes.entries()) {
        const page = await browser.newPage({viewport});
        const errors = [];
        page.on('pageerror', error=>errors.push(error.message));
        const response = await page.goto(base+route, {waitUntil:'networkidle'});
        assert.equal(response.status(),200,route);
        const figures = page.locator('main .quantization-article figure.quantization-figure');
        assert.equal(await figures.count(),3,'Three explanatory figures per article');
        for (let i=0;i<3;i++) {
          const figure = figures.nth(i);
          const image = figure.locator('img');
          await image.scrollIntoViewIfNeeded();
          await image.evaluate(el=>el.decode());
          const data = await image.evaluate(el=>({src:el.getAttribute('src'),alt:el.alt,
            width:el.naturalWidth,height:el.naturalHeight,loading:el.loading,
            rect:el.getBoundingClientRect().toJSON()}));
          assert.ok(data.width>0 && data.height>0,'Image must really load');
          assert.match(data.alt,/[\u0E00-\u0E7F]/,'Accessible Thai description');
          assert.equal(data.loading,'lazy');
          assert.ok(data.rect.left>=-1 && data.rect.right<=viewport.width+1,'Image fits phone/desktop');
          assert.match(await figure.locator('figcaption').innerText(),/[\u0E00-\u0E7F]/,'Thai explanatory caption');
          assert.equal(await figure.locator('a').getAttribute('href'),data.src);
          assets.add(data.src);
          if (i===0) {
            const [popup] = await Promise.all([page.waitForEvent('popup'),figure.locator('a').click()]);
            await popup.waitForLoadState('load');
            assert.ok(popup.url().endsWith(data.src),'Image can open at full size');
            await popup.close();
          }
          if (reportDir) await figure.screenshot({path:path.join(reportDir,`${index}-${i}-${viewport.width}.png`)});
        }
        const metrics = await page.evaluate(()=>({width:document.documentElement.clientWidth,
          scrollWidth:document.documentElement.scrollWidth,
          math:document.querySelectorAll('main .katex').length,
          mathErrors:document.querySelectorAll('main .katex-error').length,
          staleLinks:document.querySelectorAll('main .stale-link').length}));
        assert.equal(metrics.mathErrors,0);
        assert.ok(metrics.math>15);
        assert.equal(metrics.staleLinks,0);
        assert.ok(metrics.scrollWidth<=metrics.width+1,'No document horizontal overflow');
        assert.deepEqual(errors,[]);
        report.push({route,viewport,figures:3,...metrics,errors});
        await page.close();
      }
    }
    assert.equal(assets.size,6);
    for (const asset of assets) {
      const page = await browser.newPage({viewport:{width:820,height:1200}});
      const response = await page.goto(base+asset,{waitUntil:'load'});
      assert.equal(response.status(),200,asset);
      await page.evaluate(()=>document.fonts.ready);
      const layout = await page.evaluate(()=>{
        const svg=document.querySelector('svg'), box=svg.viewBox.baseVal;
        const labels=[...svg.querySelectorAll('text')].map(el=>{
          const b=el.getBBox();return {text:el.textContent,x:b.x,y:b.y,width:b.width,height:b.height};
        });
        return {width:box.width,height:box.height,labels,
          clipped:labels.filter(b=>b.x<12||b.y<0||b.x+b.width>box.width-12||b.y+b.height>box.height)};
      });
      assert.deepEqual(layout.clipped,[],'SVG text fits its canvas: '+asset+' '+JSON.stringify(layout.clipped));
      // An explicit clip avoids Chromium's standalone-SVG fullPage capture hang.
      if (reportDir) await page.screenshot({path:path.join(reportDir,path.basename(asset,'.svg')+'.png'),
        clip:{x:0,y:0,width:layout.width,height:layout.height}});
      report.push({asset,svgTextLabels:layout.labels.length,clipped:layout.clipped});
      await page.close();
    }
    const page = await browser.newPage();
    await page.goto(base+'/',{waitUntil:'networkidle'});
    for (const route of routes) assert.ok(await page.locator(`a[href="${route}"]`).count()>0,'Article remains in the feed');
    const search=await page.request.get(base+'/assets/js/SearchData.json');
    const searchText=await search.text();
    JSON.parse(searchText);
    assert.ok(searchText.includes('GSQ')&&searchText.includes('RCO'));
    report.push({feedAndSearch:true});
    if (reportDir) fs.writeFileSync(path.join(reportDir,'browser-report.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify(report,null,2));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exit(1)});
