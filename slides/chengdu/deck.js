/* === PROGRESSIVE FIXED-STAGE PRESENTATION CONTROLLER === */
class SlidePresentation {
  constructor(){
    this.slides=[...document.querySelectorAll('.slide')];
    if(!this.slides.length)return;
    this.stage=document.getElementById('deckStage');this.index=0;this.touch=null;this.lastWheel=0;
    this.prev=document.getElementById('prev');this.next=document.getElementById('next');
    this.progress=document.getElementById('progress');this.contents=document.getElementById('contents');
    this.prev.addEventListener('click',()=>{this.syncReadingPosition();this.show(this.index-1);});
    this.next.addEventListener('click',()=>{this.syncReadingPosition();this.show(this.index+1);});
    document.getElementById('pair').addEventListener('click',()=>{
      this.syncReadingPosition();
      const current=this.slides[this.index];
      const next=this.slides.findIndex(s=>s.dataset.pairId===current.dataset.pairId&&s.dataset.lang!==current.dataset.lang);
      if(next>=0)this.show(next);
    });
    this.contents.addEventListener('change',()=>this.show(this.slides.findIndex(s=>s.id===this.contents.value)));
    document.getElementById('read').addEventListener('click',()=>this.toggleReading());
    this.toolbar=document.getElementById('toolbar');
    this.toolbar.addEventListener('click',()=>this.toggleToolbar(!document.documentElement.classList.contains('toolbar-collapsed')));
    document.getElementById('fullscreen').addEventListener('click',async()=>{
      try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();}
      catch{this.progress.title='Fullscreen unavailable; normal navigation remains available.';}
    });
    window.addEventListener('hashchange',()=>this.fromHash());
    window.addEventListener('popstate',()=>this.fromHash());
    window.addEventListener('resize',()=>this.scale());
    window.addEventListener('scroll',()=>{
      if(!document.documentElement.classList.contains('reading')||this.readingFrame)return;
      this.readingFrame=true;requestAnimationFrame(()=>{this.readingFrame=false;this.syncReadingPosition();});
    },{passive:true});
    document.addEventListener('fullscreenchange',()=>this.scale());
    document.addEventListener('keydown',e=>{
      if(e.ctrlKey||e.metaKey||e.altKey||this.interactive(e.target))return;
      if(document.documentElement.classList.contains('reading')){
        if(['ArrowDown','ArrowUp','PageDown','PageUp',' ','Home','End'].includes(e.key))return;
        this.syncReadingPosition();
      }
      const delta={ArrowRight:1,ArrowDown:1,PageDown:1,' ':1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1}[e.key];
      if(delta){e.preventDefault();this.show(this.index+delta);}
      else if(e.key==='Home'){e.preventDefault();this.show(0);}
      else if(e.key==='End'){e.preventDefault();this.show(this.slides.length-1);}
    });
    document.addEventListener('touchstart',e=>{
      this.touch=e.touches.length===1&&!this.interactive(e.target)?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;
    },{passive:true});
    document.addEventListener('touchcancel',()=>{this.touch=null;},{passive:true});
    document.addEventListener('touchend',e=>{
      if(!this.touch||!e.changedTouches.length)return;
      const dx=e.changedTouches[0].clientX-this.touch.x,dy=e.changedTouches[0].clientY-this.touch.y;
      this.touch=null;if(Math.abs(dx)>65&&Math.abs(dx)>Math.abs(dy)*1.7)this.show(this.index+(dx<0?1:-1));
    },{passive:true});
    document.addEventListener('wheel',e=>{
      if(document.documentElement.classList.contains('reading')||e.ctrlKey||this.interactive(e.target))return;
      if(Math.abs(e.deltaY)>45&&performance.now()-this.lastWheel>650){this.lastWheel=performance.now();this.show(this.index+(e.deltaY>0?1:-1));}
    },{passive:true});
    document.documentElement.classList.add('enhanced');
    this.fromHash();this.scale();document.fonts.ready.then(()=>this.scale());
  }
  interactive(target){return target instanceof Element&&!!target.closest('input,textarea,select,button,a,[contenteditable]');}
  fromHash(){
    let id='';try{id=decodeURIComponent(location.hash.startsWith('#slide=')?location.hash.slice(7):'');}catch{}
    const found=this.slides.findIndex(s=>s.id===id);this.show(found<0?0:found,false);
  }
  show(index,history=true,scroll=true){
    this.index=Math.max(0,Math.min(index,this.slides.length-1));
    const reading=document.documentElement.classList.contains('reading');
    this.slides.forEach((s,i)=>{const active=i===this.index;s.classList.toggle('active',active);s.classList.toggle('visible',active);s.setAttribute('aria-hidden',String(!reading&&!active));s.inert=!reading&&!active;});
    const slide=this.slides[this.index];document.documentElement.lang=slide.dataset.lang;
    this.progress.textContent=`${this.index+1} / ${this.slides.length}`;
    this.prev.disabled=this.index===0;this.next.disabled=this.index===this.slides.length-1;this.contents.value=slide.id;
    if(history)window.history.pushState(null,'','#slide='+encodeURIComponent(slide.id));
    if(reading&&scroll)slide.scrollIntoView({block:'start',behavior:'instant'});
  }
  scale(){
    if(document.documentElement.classList.contains('reading')){this.reserveReadingSpace();return;}
    const controls=document.querySelector('.deck-controls').getBoundingClientRect().height;
    const available=Math.max(120,innerHeight-controls-36),factor=Math.min(innerWidth/1920,available/1080);
    this.stage.style.transform=`translate(${(innerWidth-1920*factor)/2}px,${(available-1080*factor)/2+8}px) scale(${factor})`;
  }
  syncReadingPosition(){
    if(!document.documentElement.classList.contains('reading'))return;
    let best=this.index,visible=0;
    this.slides.forEach((slide,index)=>{const r=slide.getBoundingClientRect();const height=Math.max(0,Math.min(r.bottom,innerHeight)-Math.max(r.top,0));if(height>visible){visible=height;best=index;}});
    if(best!==this.index){this.show(best,false,false);window.history.replaceState(null,'','#slide='+encodeURIComponent(this.slides[best].id));}
  }
  toggleReading(){
    this.syncReadingPosition();
    document.documentElement.classList.toggle('reading');
    this.toggleToolbar(document.documentElement.classList.contains('reading')&&innerWidth<=650);
    this.show(this.index,false);this.scale();
    if(!document.documentElement.classList.contains('reading'))window.scrollTo(0,0);
  }
  toggleToolbar(collapsed){
    document.documentElement.classList.toggle('toolbar-collapsed',collapsed);
    this.toolbar.setAttribute('aria-expanded',String(!collapsed));this.reserveReadingSpace();
  }
  reserveReadingSpace(){
    const collapsed=document.documentElement.classList.contains('toolbar-collapsed');
    const height=collapsed?84:document.querySelector('.deck-controls').getBoundingClientRect().height+90;
    document.documentElement.style.setProperty('--reading-controls-space',height+'px');
  }
}
new SlidePresentation();
