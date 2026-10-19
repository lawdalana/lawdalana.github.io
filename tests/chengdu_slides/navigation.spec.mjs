import {test,expect} from '@playwright/test';
const path='/_reports/chengdu-slides/fixture/index.html';
test.beforeEach(async({page})=>{await page.goto(path);});
test('next back pair and unknown deep link retain valid slide',async({page})=>{
  await expect(page.locator('.slide.active')).toHaveCount(1);
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','th');
  await page.locator('#next').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','zh-Hans');
  await page.locator('#pair').click();
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','th');
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
  await expect(page.locator('.slide.active')).toHaveAttribute('data-lang','zh-Hans');
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
  await expect(active).toHaveAttribute('data-slide-id','fixture-intro--zh-Hans');
  await page.goBack();await expect(active).toHaveAttribute('data-slide-id','fixture-intro--th');
  await page.goForward();await expect(active).toHaveAttribute('data-slide-id','fixture-intro--zh-Hans');
  await page.keyboard.press('End');await expect(page.locator('#next')).toBeDisabled();
  await page.keyboard.press('Home');await expect(page.locator('#prev')).toBeDisabled();
  await page.evaluate(()=>{
    const target=document.querySelector('.slide.active');
    const point=(x,y)=>new Touch({identifier:1,target,clientX:x,clientY:y});
    target.dispatchEvent(new TouchEvent('touchstart',{touches:[point(600,300)],bubbles:true}));
    target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[point(100,310)],bubbles:true}));
  });
  await expect(active).toHaveAttribute('data-slide-id','fixture-intro--zh-Hans');
  await page.evaluate(()=>{
    const target=document.querySelector('.slide.active');
    const point=(x,y)=>new Touch({identifier:2,target,clientX:x,clientY:y});
    target.dispatchEvent(new TouchEvent('touchstart',{touches:[point(500,100)],bubbles:true}));
    target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[point(505,600)],bubbles:true}));
  });
  await expect(active).toHaveAttribute('data-slide-id','fixture-intro--zh-Hans');
  await page.waitForTimeout(700);await page.mouse.move(5,5);await page.mouse.wheel(0,120);
  await expect(active).toHaveAttribute('data-slide-id','fixture-details--th');
});
