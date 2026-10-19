import {test,expect} from '@playwright/test';
import {fileURLToPath} from 'node:url';
import {readFileSync} from 'node:fs';
const directory=fileURLToPath(new URL('../../_reports/chengdu-slides/draft/',import.meta.url));

test('self-contained draft works fully offline and produces actual print pages',async({browser})=>{
  test.setTimeout(90000);
  const context=await browser.newContext({offline:true,viewport:{width:1920,height:1080}});
  const page=await context.newPage(),network=[],errors=[];
  page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('file://'+directory+'Chengdu_Thai_Chinese_Draft.html');
  await page.evaluate(async()=>{await document.fonts.ready;for(const image of document.images){image.loading='eager';await image.decode();}});
  expect(await page.evaluate(()=>[...document.images].every(i=>i.naturalWidth>0))).toBe(true);
  expect(await page.evaluate(()=>[...document.fonts].every(f=>f.status==='loaded'))).toBe(true);
  await page.selectOption('#contents','panda-base-intro--th');await page.waitForTimeout(350);
  await page.screenshot({path:directory+'Chengdu_Thai_preview.png'});
  await page.click('#pair');await page.waitForTimeout(350);
  await page.screenshot({path:directory+'Chengdu_Chinese_preview.png'});
  await page.evaluate(()=>document.querySelectorAll('.slide').forEach(s=>{s.inert=false;s.removeAttribute('aria-hidden');}));
  await page.addStyleTag({content:`@page{size:1920px 1080px;margin:0}@media print{html,body{width:1920px;height:auto;overflow:visible}.deck-viewport{position:static;overflow:visible}.deck-stage{position:static;transform:none!important;width:1920px;height:auto;overflow:visible}.slide{position:relative;visibility:visible;opacity:1;pointer-events:auto;width:1920px;height:1080px;overflow:hidden;break-after:page}.slide:last-child{break-after:auto}.deck-controls{display:none!important}}`});
  await page.pdf({path:directory+'Chengdu_Thai_Chinese_Draft.pdf',printBackground:true,preferCSSPageSize:true});
  expect(readFileSync(directory+'Chengdu_Thai_Chinese_Draft.pdf').subarray(0,5).toString()).toBe('%PDF-');
  expect(network).toEqual([]);expect(errors).toEqual([]);
  await context.close();
});
