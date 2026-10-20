// Measure the real local fonts/CSS. Never guess fit from character or bullet counts.
import {createRequire} from 'node:module';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const root=process.cwd(),require=createRequire(root+'/tests/chengdu_slides/package.json');
const {chromium}=require('@playwright/test');
const [input,probe,output]=process.argv.slice(2);
if(!input||!probe||!output)throw Error('usage: node measure-pagination.mjs input.json probe.html output.json');
const data=JSON.parse(readFileSync(input,'utf8')),browser=await chromium.launch({headless:true});
try{
 const context=await browser.newContext({viewport:{width:1920,height:1200},reducedMotion:'reduce'}),page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(resolve(probe)).href);await page.evaluate(()=>document.fonts.ready);
 const measured=await page.evaluate(()=>{
  const rows={},audit=[],stage=document.querySelector('#deckStage'),scale=stage.getBoundingClientRect().width/1920;
  if(Math.abs(scale-1)>.001)throw Error('measurement stage must be unscaled');
  const all=[...document.querySelectorAll('.slide')];
  for(const thai of all.filter(s=>s.dataset.lang==='th')){
   const chinese=all.find(s=>s.dataset.pairId===thai.dataset.pairId&&s.dataset.lang==='zh-Hans');
   if(!chinese)throw Error('missing Chinese source: '+thai.id);
   const templates=new Map([thai,chinese].map(s=>[s,[...s.querySelectorAll('.copy li')].map(li=>li.cloneNode(true))]));
   const n=templates.get(thai).length;if(n!==templates.get(chinese).length)throw Error('source correspondence mismatch');
   function fit(slide,start,end){
    const list=slide.querySelector('.copy ul');list.replaceChildren(...templates.get(slide).slice(start,end).map(li=>li.cloneNode(true)));
    slide.querySelector('.continuation')?.remove();
    if(start>0||end<n){const badge=document.createElement('span');badge.className='continuation';badge.textContent='1 / '+n;slide.querySelector('.eyebrow').append(badge)}
    const last=list.lastElementChild.getBoundingClientRect(),frame=slide.querySelector('.spread').getBoundingClientRect(),footer=slide.querySelector('footer').getBoundingClientRect();
    const limit=Math.min(frame.bottom,footer.top-16),copy=slide.querySelector('.copy').getBoundingClientRect();
    return {fits:last.bottom<=limit&&last.right<=copy.right+.5,remaining:limit-last.bottom,bottom:last.bottom,limit};
   }
   function largest(slide,start,end){
    for(let stop=end;stop>start;stop--){const result=fit(slide,start,stop);if(result.fits)return {stop,...result}}
    throw Error('one source bullet does not fit: '+slide.id+' at '+start);
   }
   const plan=[];let start=0;
   while(start<n){
    const th=largest(thai,start,n),cn=[];let cursor=start;
    while(cursor<th.stop){const result=largest(chinese,cursor,th.stop);cn.push([cursor,result.stop]);cursor=result.stop}
    plan.push({'th':[start,th.stop],'zh-Hans':cn});
    audit.push({topic:thai.dataset.pairId,range:[start,th.stop],thaiRemaining:th.remaining,chinesePages:cn.length});start=th.stop;
   }
   rows[thai.dataset.pairId]=plan;
  }
  return {plans:rows,audit,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))};
 });
 if(errors.length)throw Error(JSON.stringify(errors));
 if(measured.fonts.some(f=>f.status!=='loaded'))throw Error('measurement requires every local font loaded');
 for(const unit of [...data.support,...['attractions','restaurants','gifts'].flatMap(c=>data[c].flatMap(item=>item.units))]){
  if(!measured.plans[unit.id])throw Error('missing measured topic: '+unit.id);unit.pagination=measured.plans[unit.id];
 }
 writeFileSync(output,JSON.stringify(data,null,2)+'\n');writeFileSync(output+'.audit.json',JSON.stringify(measured,null,2)+'\n');
 console.log(JSON.stringify({topics:Object.keys(measured.plans).length,thaiPages:measured.audit.length,chinesePages:measured.audit.reduce((n,r)=>n+r.chinesePages,0),fonts:measured.fonts}));
 await context.close();
}finally{await browser.close()}
