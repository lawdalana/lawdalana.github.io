import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';

const draft='/_reports/chengdu-slides/draft/index.html';
const canonical=name=>JSON.parse(readFileSync(new URL('../../_data/chengdu_slides/'+name+'.json',import.meta.url),'utf8'));
const expectedSlides=2*(canonical('support').length+['attractions','restaurants','gifts'].reduce((sum,cat)=>sum+canonical(cat).reduce((n,item)=>n+item.units.length,0),0));

test('actual sourced draft: every pair, image, font and fixed-stage text fits',async({page})=>{
  test.setTimeout(90000);
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(draft);await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(async()=>{
    const slides=[...document.querySelectorAll('.slide')],bad=[],pairs=[];
    for(let i=0;i<slides.length;i++){
      const s=slides[i];
      if(i%2===0&&(!slides[i+1]||s.dataset.lang!=='th'||slides[i+1].dataset.lang!=='zh-Hans'||s.dataset.pairId!==slides[i+1].dataset.pairId))pairs.push(s.id);
      const image=s.querySelector('img');image.loading='eager';
      try{await image.decode();}catch{bad.push({id:s.id,error:'image decode failed'});}
      const scale=document.querySelector('#deckStage').getBoundingClientRect().width/1920;
      const end=s.querySelector('.copy li:last-child')?.getBoundingClientRect().bottom||0;
      const footer=s.querySelector('footer').getBoundingClientRect().top;
      if(end>footer-8*scale)bad.push({id:s.id,error:'copy overlaps footer',overflow:(end-footer)/scale});
      const caption=s.querySelector('figcaption').getBoundingClientRect().bottom;
      if(caption>footer-8*scale)bad.push({id:s.id,error:'caption overlaps footer',overflow:(caption-footer)/scale});
    }
    return{count:slides.length,bad,pairs,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),images:slides.filter(s=>s.querySelector('img').naturalWidth>0).length};
  });
  expect(result.count).toBe(expectedSlides);expect(result.pairs).toEqual([]);expect(result.images).toBe(expectedSlides);expect(errors).toEqual([]);
  expect(result.fonts.filter(f=>f.status!=='loaded')).toEqual([]);
  await test.info().attach('actual-content-layout.json',{body:JSON.stringify(result,null,2),contentType:'application/json'});
  expect(result.bad).toEqual([]);
});

test('actual mobile reading view has no horizontal overflow and all content is exposed',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto(draft);await page.click('#read');await page.evaluate(()=>document.fonts.ready);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  expect(await page.locator('.slide[aria-hidden="true"]').count()).toBe(0);
  await page.screenshot({path:'../../_reports/chengdu-slides/mobile-reading.png',fullPage:false});
});

test('actual reading view follows natural scroll before language and mode changes',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto(draft);await page.click('#read');
  await page.locator('#yang-bo-ying-intro--th').evaluate(e=>e.scrollIntoView({block:'start'}));
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','yang-bo-ying-intro--th');
  await page.click('#pair');
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','yang-bo-ying-intro--zh-Hans');
  expect(await page.locator('.slide[lang="th"] .copy ul').first().evaluate(e=>getComputedStyle(e).fontFamily)).toContain('TravelThai');
  await page.click('#read');
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','yang-bo-ying-intro--zh-Hans');
  await expect(page.locator('html')).not.toHaveClass(/reading/);
});

test('actual reading view preserves native PageDown instead of jumping to stale slides',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto(draft);await page.click('#read');
  await page.locator('#yang-bo-ying-intro--th').evaluate(e=>e.scrollIntoView({block:'start'}));
  await page.evaluate(()=>document.activeElement?.blur());
  const before=await page.evaluate(()=>scrollY);await page.keyboard.press('PageDown');
  await expect.poll(()=>page.evaluate(()=>scrollY)).toBeGreaterThan(before);
});

test('mobile no-JavaScript fallback is fluid instead of a desktop-width canvas',async({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}}),page=await context.newPage();
  await page.goto('http://127.0.0.1:8765'+draft);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  const copy=await page.locator('.copy').first().boundingBox();
  expect(copy.x+copy.width).toBeLessThanOrEqual(391);
  expect(await page.locator('.copy ul').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize))).toBeGreaterThanOrEqual(18);
  await context.close();
});

test('actual deck is readable with JavaScript disabled',async({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:1920,height:1080}});const page=await context.newPage();
  await page.goto('http://127.0.0.1:8765'+draft);
  expect(await page.locator('.slide').count()).toBe(expectedSlides);
  await expect(page.locator('.slide').first()).toBeVisible();await expect(page.locator('.slide').last()).toBeVisible();
  await context.close();
});
