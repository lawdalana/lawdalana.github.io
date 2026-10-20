import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';

const draft='/_reports/chengdu-slides/draft/index.html';
const canonical=name=>JSON.parse(readFileSync(new URL('../../_data/chengdu_slides/'+name+'.json',import.meta.url),'utf8'));
const sourceEntries=[...canonical('support').map(unit=>({unit,facts:unit.facts||{}})),...['attractions','restaurants','gifts'].flatMap(cat=>canonical(cat).flatMap(item=>item.units.map(unit=>({unit,facts:item.facts}))))];
const expectedSlides=sourceEntries.reduce((n,{unit})=>n+(unit.pagination?unit.pagination.length+unit.pagination.reduce((sum,p)=>sum+p['zh-Hans'].length,0):2),0);
const expectedBodies=Object.fromEntries(sourceEntries.map(({unit,facts})=>[unit.id,Object.fromEntries(['th','zh-Hans'].map(lang=>[lang,unit.body[lang].map(t=>t.replace(/\{(\w+)\}/g,(_,key)=>String(facts[key])))]))]));

test('actual sourced draft: every unequal-language topic, image, font and fixed-stage text fits',async({page})=>{
  test.setTimeout(90000);
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(draft);await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(async()=>{
    const slides=[...document.querySelectorAll('.slide')],bad=[],pairs=[],bodies={},groups=new Map();
    for(let i=0;i<slides.length;i++){
      const s=slides[i];
      if(!groups.has(s.dataset.pairId))groups.set(s.dataset.pairId,[]);groups.get(s.dataset.pairId).push(s);
      bodies[s.dataset.pairId]??={th:[],'zh-Hans':[]};
      bodies[s.dataset.pairId][s.dataset.lang].push(...[...s.querySelectorAll('.copy li')].map(li=>li.textContent));
      const image=s.querySelector('img');image.loading='eager';
      try{await image.decode();}catch{bad.push({id:s.id,error:'image decode failed'});}
      const scale=document.querySelector('#deckStage').getBoundingClientRect().width/1920;
      const end=s.querySelector('.copy li:last-child')?.getBoundingClientRect().bottom||0;
      const footer=s.querySelector('footer').getBoundingClientRect().top;
      if(end>footer-8*scale)bad.push({id:s.id,error:'copy overlaps footer',overflow:(end-footer)/scale});
      const caption=s.querySelector('figcaption').getBoundingClientRect().bottom;
      if(caption>footer-8*scale)bad.push({id:s.id,error:'caption overlaps footer',overflow:(caption-footer)/scale});
    }
    for(const [topic,rows] of groups)for(const lang of ['th','zh-Hans']){
      const pages=rows.filter(s=>s.dataset.lang===lang);
      if(!pages.length||pages[0].id!==topic+'--'+lang||pages.some((s,n)=>Number(s.dataset.pagePart)!==n+1||Number(s.dataset.pageTotal)!==pages.length))pairs.push(topic+':'+lang);
    }
    return{count:slides.length,bad,pairs,bodies,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),images:slides.filter(s=>s.querySelector('img').naturalWidth>0).length};
  });
  expect(result.count).toBe(expectedSlides);expect(result.pairs).toEqual([]);expect(result.images).toBe(expectedSlides);expect(errors).toEqual([]);
  expect(result.bodies).toEqual(expectedBodies);
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
  await page.click('#toolbar');
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

test('tablet no-JavaScript photo details keep a readable copy column',async({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:1024,height:768}}),page=await context.newPage();
  await page.goto('http://127.0.0.1:8765'+draft);
  const details=page.locator('.photo-slide.layout-details').first();
  const columns=await details.evaluate(e=>({copy:e.querySelector('.copy').getBoundingClientRect().width,image:e.querySelector('.visual').getBoundingClientRect().width}));
  expect(columns.copy).toBeGreaterThan(columns.image);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  await context.close();
});
