import {test,expect} from '@playwright/test';

test('reduced-motion language changes never paint two language pages at once',async({page})=>{
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/_reports/chengdu-slides/fixture/index.html');
  await page.waitForFunction(()=>[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).visibility==='visible'&&parseFloat(getComputedStyle(s).opacity)>.001).length===1);
  await page.click('#pair');
  const painted=await page.evaluate(()=>[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).visibility==='visible'&&parseFloat(getComputedStyle(s).opacity)>.001).map(s=>s.dataset.lang));
  expect(painted).toEqual(['zh-Hans']);
});
test('mobile reading controls collapse without hiding the paired content',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.click('#read');
  await expect(page.locator('.deck-controls')).toBeHidden();
  await expect(page.locator('#toolbar')).toHaveAttribute('aria-expanded','false');
  expect(await page.locator('.slide[aria-hidden="true"]').count()).toBe(0);
  await page.click('#toolbar');await expect(page.locator('.deck-controls')).toBeVisible();
  await expect(page.locator('#toolbar')).toHaveAttribute('aria-expanded','true');
  await page.click('#read');await expect(page.locator('html')).not.toHaveClass(/reading/);
  await expect(page.locator('.deck-controls')).toBeVisible();await expect(page.locator('#toolbar')).toBeHidden();
});

const path='/_reports/chengdu-slides/fixture/index.html';
test.beforeEach(async({page})=>{await page.goto(path);});
test('next back pair and unknown deep link retain valid slide',async({page})=>{
  await expect(page.locator('.slide.active')).toHaveCount(1);
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','th');
  await page.locator('#next').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','fixture-details--th');
  await page.locator('#pair').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','fixture-details--zh-Hans');
  await page.locator('#prev').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','fixture-intro--zh-Hans');
  await page.goto(path+'#slide=unknown');
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','fixture-intro--th');
});
test('editable focus does not advance and denied fullscreen keeps navigation working',async({page})=>{
  await page.evaluate(()=>{const i=document.createElement('input');i.id='testing-input';i.style.position='fixed';i.style.zIndex='9999';document.body.append(i);});
  await page.locator('#testing-input').focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','th');
  await page.evaluate(()=>{document.documentElement.requestFullscreen=()=>Promise.reject(new Error('denied'));});
  await page.locator('#fullscreen').click();
  await page.locator('#next').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-slide-id','fixture-details--th');
});
test('fixed stage stays 1920x1080 and reading view preserves all paired content',async({page})=>{
  const size=await page.locator('#deckStage').evaluate(e=>({w:e.offsetWidth,h:e.offsetHeight}));
  expect(size).toEqual({w:1920,h:1080});
  await page.setViewportSize({width:390,height:844});
  await page.locator('#read').click();
  await expect(page.locator('html')).toHaveClass(/reading/);
  expect(await page.locator('.slide').count()).toBe(4);
  const dimensions=await page.locator('body').evaluate(e=>({w:e.scrollWidth,client:innerWidth}));
  expect(dimensions.w).toBeLessThanOrEqual(dimensions.client+1);
});

test('keyboard history wheel and horizontal touch preserve navigation boundaries',async({page})=>{
  const active=page.locator('.slide.active');
  await page.locator('body').click({position:{x:5,y:5}});
  await page.keyboard.press('ArrowRight');
  await expect(active).toHaveAttribute('data-slide-id','fixture-details--th');
  await page.goBack();await expect(active).toHaveAttribute('data-slide-id','fixture-intro--th');
  await page.goForward();await expect(active).toHaveAttribute('data-slide-id','fixture-details--th');
  await page.keyboard.press('End');await expect(page.locator('#next')).toBeDisabled();
  await page.keyboard.press('Home');await expect(page.locator('#prev')).toBeDisabled();
  await page.evaluate(()=>{
    const target=document.querySelector('.slide.active');
    const point=(x,y)=>new Touch({identifier:1,target,clientX:x,clientY:y});
    target.dispatchEvent(new TouchEvent('touchstart',{touches:[point(600,300)],bubbles:true}));
    target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[point(100,310)],bubbles:true}));
  });
  await expect(active).toHaveAttribute('data-slide-id','fixture-details--th');
  await page.evaluate(()=>{
    const target=document.querySelector('.slide.active');
    const point=(x,y)=>new Touch({identifier:2,target,clientX:x,clientY:y});
    target.dispatchEvent(new TouchEvent('touchstart',{touches:[point(500,100)],bubbles:true}));
    target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[point(505,600)],bubbles:true}));
  });
  await expect(active).toHaveAttribute('data-slide-id','fixture-details--th');
  await page.waitForTimeout(700);await page.mouse.move(5,5);await page.mouse.wheel(0,-120);
  await expect(active).toHaveAttribute('data-slide-id','fixture-intro--th');
});
