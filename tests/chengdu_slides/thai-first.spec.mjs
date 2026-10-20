import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const route='/_reports/chengdu-slides/draft/index.html';
const data=name=>JSON.parse(readFileSync(new URL('../../_data/chengdu_slides/'+name+'.json',import.meta.url)));
const units=[...data('support'),...['attractions','restaurants','gifts'].flatMap(c=>data(c).flatMap(item=>item.units))];
const multi=()=>units.find(u=>u.pagination?.length>1);
test.use({reducedMotion:'reduce'});

for(const viewport of [{width:1280,height:720},{width:390,height:844}]){
 test(`Chinese continuation switches to the first page of the same topic at ${viewport.width}px`,async({page})=>{
  await page.setViewportSize(viewport);const topic='museum-collection-magnet-intro';
  await page.goto(route+'#slide='+topic+'--th');
  expect(await page.locator('.slide[data-pair-id="'+topic+'"][lang="th"]').count()).toBe(1);
  expect(await page.locator('.slide[data-pair-id="'+topic+'"][lang="zh-Hans"]').count()).toBe(2);
  await page.click('#pair');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'--zh-Hans');
  await page.click('#next');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'-page-2--zh-Hans');
  await page.click('#pair');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'--th');
  await page.click('#pair');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'--zh-Hans');
 });
}

test('switching from a later Thai page also resets to the first translated topic page',async({page})=>{
 const topic=multi().id;await page.goto(route+'#slide='+topic+'-page-2--th');
 await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'-page-2--th');
 await page.click('#pair');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'--zh-Hans');
 await page.click('#pair');await expect(page.locator('.slide.active')).toHaveAttribute('id',topic+'--th');
});

test('old split-page deep links resolve to their original topic instead of the cover',async({page})=>{
 await page.goto(route+'#slide=panda-base-details-present-2--th');
 await expect(page.locator('.slide.active')).toHaveAttribute('id','panda-base-details--th');
});

test('Thai page breaks are measured necessities rather than a two-bullet ceiling',async({page})=>{
 await page.goto(route);await page.evaluate(()=>document.fonts.ready);
 const result=await page.evaluate(units=>{
  const unnecessary=[],scale=document.querySelector('#deckStage').getBoundingClientRect().width/1920;
  for(const unit of units){
   for(let n=0;n+1<unit.pagination.length;n++){
    const id=unit.id+(n?'-page-'+(n+1):'')+'--th',slide=document.getElementById(id),list=slide.querySelector('.copy ul');
    const next=document.getElementById(unit.id+'-page-'+(n+2)+'--th').querySelector('.copy li').cloneNode(true);
    list.append(next);
    const bottom=next.getBoundingClientRect().bottom,limit=Math.min(slide.querySelector('.spread').getBoundingClientRect().bottom,slide.querySelector('footer').getBoundingClientRect().top-16*scale);
    if(bottom<=limit)unnecessary.push(id);next.remove();
   }
  }
  return {unnecessary,maxBullets:Math.max(...[...document.querySelectorAll('.slide[lang="th"] .copy ul')].map(e=>e.children.length)),fontSize:getComputedStyle(document.querySelector('.photo-slide:not(.layout-chapter)[lang="th"] .copy ul')).fontSize};
 },units);
 expect(result.unnecessary).toEqual([]);expect(result.maxBullets).toBeGreaterThan(2);expect(result.fontSize).toBe('32px');
});
