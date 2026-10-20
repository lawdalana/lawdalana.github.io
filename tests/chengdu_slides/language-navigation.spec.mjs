import {test,expect} from '@playwright/test';
const fixture='/_reports/chengdu-slides/fixture/index.html';
test.use({reducedMotion:'reduce'});
const active=page=>page.locator('.slide.active');

for(const lang of ['th','zh-Hans']){
  test(`next and previous stay in ${lang}; switching language retains the logical page`,async({page})=>{
    await page.goto(fixture+'#slide=fixture-intro--'+lang);
    await expect(page.locator('#prev')).toBeDisabled();
    await expect(page.locator('#progress')).toHaveText('1 / 2');
    await page.click('#next');await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
    await expect(page.locator('#next')).toBeDisabled();await expect(page.locator('#progress')).toHaveText('2 / 2');
    const other=lang==='th'?'zh-Hans':'th';await page.click('#pair');
    await expect(active(page)).toHaveAttribute('id','fixture-details--'+other);await expect(page.locator('#next')).toBeDisabled();
    await expect(page.locator('.slide.active .page-no')).toHaveText('002');
    await page.click('#prev');await expect(active(page)).toHaveAttribute('id','fixture-intro--'+other);
    await expect(page.locator('#prev')).toBeDisabled();await expect(page.locator('#progress')).toHaveText('1 / 2');
    const options=await page.locator('#contents option').evaluateAll(options=>options.map(o=>({value:o.value,label:o.textContent})));
    expect(options.map(o=>o.value)).toEqual(['fixture-intro--'+other,'fixture-details--'+other]);
    expect(options.map(o=>o.label.slice(0,3))).toEqual(['001','002']);
  });

  test(`keyboard, history and language boundaries retain ${lang}`,async({page})=>{
    await page.goto(fixture+'#slide=fixture-intro--'+lang);await page.locator('body').click({position:{x:5,y:5}});
    await page.keyboard.press('ArrowRight');await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
    await page.goBack();await expect(active(page)).toHaveAttribute('id','fixture-intro--'+lang);
    await page.goForward();await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
    await page.keyboard.press('Home');await expect(active(page)).toHaveAttribute('id','fixture-intro--'+lang);
    await expect(page.locator('#prev')).toBeDisabled();await page.keyboard.press('End');
    await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);await expect(page.locator('#next')).toBeDisabled();
    for(const key of ['ArrowRight','ArrowDown','PageDown',' ']){
      await page.keyboard.press('Home');await page.keyboard.press(key);await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
    }
    for(const key of ['ArrowLeft','ArrowUp','PageUp']){
      await page.keyboard.press('End');await page.keyboard.press(key);await expect(active(page)).toHaveAttribute('id','fixture-intro--'+lang);
    }
  });

  test(`wheel and horizontal touch stay in ${lang}`,async({page})=>{
    await page.goto(fixture+'#slide=fixture-intro--'+lang);await page.waitForTimeout(700);await page.mouse.move(5,5);await page.mouse.wheel(0,120);
    await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
    await page.waitForTimeout(700);await page.mouse.wheel(0,-120);await expect(active(page)).toHaveAttribute('id','fixture-intro--'+lang);
    await page.evaluate(()=>{
      const target=document.querySelector('.slide.active'),point=x=>new Touch({identifier:1,target,clientX:x,clientY:300});
      target.dispatchEvent(new TouchEvent('touchstart',{touches:[point(600)],bubbles:true}));
      target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[point(100)],bubbles:true}));
    });
    await expect(active(page)).toHaveAttribute('id','fixture-details--'+lang);
  });
}

test('actual photographic deck has one language of contents and correct end boundaries',async({page})=>{
  await page.goto('/_reports/chengdu-slides/draft/index.html');
  for(const lang of ['th','zh-Hans']){
    if(lang==='zh-Hans')await page.click('#pair');
    const ids=await page.locator('.slide[data-lang="'+lang+'"]').evaluateAll(slides=>slides.map(s=>s.id));
    expect(await page.locator('#contents option').count()).toBe(ids.length);
    await page.locator('body').click({position:{x:5,y:5}});await page.keyboard.press('Home');
    await expect(active(page)).toHaveAttribute('id',ids[0]);await expect(page.locator('#prev')).toBeDisabled();
    await page.click('#next');await expect(active(page)).toHaveAttribute('id',ids[1]);
    await expect(page.locator('#progress')).toHaveText('2 / '+ids.length);
    await page.locator('body').click({position:{x:5,y:5}});
    await page.keyboard.press('End');await expect(active(page)).toHaveAttribute('id',ids.at(-1));
    await expect(page.locator('#next')).toBeDisabled();await page.click('#prev');
    await expect(active(page)).toHaveAttribute('id',ids.at(-2));
    await page.selectOption('#contents',ids[0]);await expect(active(page)).toHaveAttribute('id',ids[0]);
  }
});
