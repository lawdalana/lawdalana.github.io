import {test,expect} from '@playwright/test';
import {fileURLToPath} from 'node:url';
import {readFileSync,mkdirSync,rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const directory=fileURLToPath(new URL('../../_reports/chengdu-slides/draft/',import.meta.url));

test('self-contained draft works fully offline and produces actual print pages',async({browser})=>{
  test.setTimeout(300000);
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
  // PDF has no native WebP stream: use real-source JPEG derivatives, not huge lossless rasters.
  await page.evaluate(async()=>{
    const encoded=new Map();
    for(const image of document.images){
      const original=image.currentSrc||image.src;
      if(!encoded.has(original)){
        const canvas=document.createElement('canvas');canvas.width=Math.min(1400,image.naturalWidth);
        canvas.height=Math.round(image.naturalHeight*canvas.width/image.naturalWidth);
        canvas.getContext('2d').drawImage(image,0,0,canvas.width,canvas.height);
        encoded.set(original,canvas.toDataURL('image/jpeg',.9));
      }
      image.src=encoded.get(original);await image.decode();
    }
  });
  await page.addStyleTag({content:'@media print{.visual img{filter:none!important}.visual{box-shadow:none!important}}'});
  await page.evaluate(()=>document.querySelectorAll('.slide').forEach(s=>{s.inert=false;s.removeAttribute('aria-hidden');}));
  await page.addStyleTag({content:`@page{size:1920px 1080px;margin:0}@media print{html,body{width:1920px;height:auto;overflow:visible}.deck-viewport{position:static;overflow:visible}.deck-stage{position:static;transform:none!important;width:1920px;height:auto;overflow:visible}.slide{position:relative;visibility:visible;opacity:1;pointer-events:auto;width:1920px;height:1080px;overflow:hidden;break-after:page}.slide:last-child{break-after:auto}.deck-controls{display:none!important}}`});
  const count=await page.locator('.slide').count(),parts=[],chunks=directory+'print-chunks/';mkdirSync(chunks,{recursive:true});
  // Bound Chromium's photo rasterization memory; every real page is still printed and merged.
  for(let start=0;start<count;start+=32){
    await page.evaluate(({start,end})=>document.querySelectorAll('.slide').forEach((slide,index)=>{
      slide.style.setProperty('display',index>=start&&index<end?'block':'none','important');
      slide.style.breakAfter=index===end-1?'auto':'page';
    }),{start,end:Math.min(start+32,count)});
    const part=chunks+'part-'+String(start).padStart(4,'0')+'.pdf';
    await page.pdf({path:part,printBackground:true,preferCSSPageSize:true});parts.push(part);
  }
  const target=directory+'Chengdu_Thai_Chinese_Draft.pdf';execFileSync('pdfunite',[...parts,target]);
  const info=execFileSync('pdfinfo',[target],{encoding:'utf8'});
  expect(Number(info.match(/^Pages:\s+(\d+)/m)?.[1])).toBe(count);
  parts.forEach(path=>rmSync(path));
  expect(readFileSync(directory+'Chengdu_Thai_Chinese_Draft.pdf').subarray(0,5).toString()).toBe('%PDF-');
  expect(network).toEqual([]);expect(errors).toEqual([]);
  await context.close();
});
