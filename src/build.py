# -*- coding: utf-8 -*-
import json, sys
from pal2 import P
from wtitles import W as WTITLE
LOOKUP={"theory":("wp","music theory"),"production":("wp","audio production"),
        "genre":("wp","music genre"),"adjective":("wt",""),"abstract":("wt",""),
        "emotion":("wt",""),"verb":("wt","")}

h=open('base.html').read()
def sub(old,new,label):
    global h
    if old not in h: sys.exit("PATCH FAILED: "+label)
    h=h.replace(old,new,1)

WORD={}
ORDER_IDS=["emotion","theory","adjective","verb","abstract","production","genre"]
for k in ORDER_IDS:
    n,b,g,flat = P[k]
    mode,hint = LOOKUP.get(k,("",""))
    def mk(w,cat):
        it={"n":w,"c":cat}
        if mode=="wp": it["w"]=WTITLE.get(w,w)
        return it
    if flat is not None:
        WORD[k]={"name":n,"blurb":b,"flat":1,"order":[],"lk":mode,"hint":hint,
                 "items":[mk(w,"") for w in flat]}
    else:
        WORD[k]={"name":n,"blurb":b,"order":list(g.keys()),"lk":mode,"hint":hint,
                 "items":[mk(w,cat) for cat,ws in g.items() for w in ws]}
WJSON=json.dumps(WORD,ensure_ascii=False,separators=(',',':'))

# ---------- 1. palette tab bar ----------
sub("""<div class="bar">
  <div class="seg" id="seg">""",
"""<nav class="tabs" id="tabs"></nav>

<div class="bar">
  <div class="seg" id="seg">""","tabs html")

sub("""header{border-bottom:2px solid var(--ink);padding-bottom:12px;margin-bottom:6px}""",
"""header{border-bottom:2px solid var(--ink);padding-bottom:12px;margin-bottom:6px}
.tabs{display:flex;flex-wrap:wrap;gap:5px;margin:11px 0 0}
.tabs button{font:inherit;font-size:12.5px;padding:5px 12px;cursor:pointer;
 background:transparent;color:var(--soft);border:1px solid var(--rule);border-radius:20px}
.tabs button:hover{color:var(--ink)}
.tabs button.on{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.blurb{font-size:12.5px;color:var(--soft);font-style:italic;margin:10px 0 0}
.flatlist{break-inside:auto}
.flatlist li{padding:0}
.acts{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 0}
.acts button{font:inherit;font-size:12.5px;padding:5px 13px;cursor:pointer;
 background:transparent;color:var(--accent);border:1px solid var(--rule);border-radius:7px}
.acts button:hover{background:var(--tint);border-color:var(--accent)}
#tray{margin:12px 0 0;padding:9px 12px;border:1px dashed var(--accent);border-radius:8px;
 display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#tray .pill{font-size:12px;background:var(--tint);border-radius:20px;padding:3px 9px;
 display:inline-flex;gap:6px;align-items:center}
#tray .pill i{cursor:pointer;font-style:normal;opacity:.5}
#tray .pill i:hover{opacity:1;color:var(--accent)}
#tray .tact{font:inherit;font-size:11.5px;background:none;border:0;color:var(--accent);
 cursor:pointer;text-decoration:underline;padding:0}
#tray .lbl2{font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--soft)}
#focus{position:fixed;inset:0;z-index:120;background:var(--paper);display:flex;
 flex-direction:column;align-items:center;justify-content:center;gap:18px;padding:40px;text-align:center}
#focus[hidden]{display:none}
#tray[hidden]{display:none}
#focus .big{font-size:clamp(34px,7vw,76px);line-height:1.05;letter-spacing:-.02em;margin:0}
#focus .cat{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--soft);margin:0}
#focus .row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
#focus button{font:inherit;font-size:13px;padding:7px 16px;cursor:pointer;background:transparent;
 color:var(--accent);border:1px solid var(--rule);border-radius:8px}
#roll .pairx{color:var(--soft);padding:0 6px}
#roll .brow{display:block;margin:3px 0}
#roll .bk{display:inline-block;min-width:118px;font-size:10.5px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--soft)}
li.pinned a,li.pinned{color:var(--accent)!important;font-weight:600}
li a.wt{cursor:default}
#card .def{font-size:12.4px;line-height:1.45;margin:0;opacity:.88}
#card .pos{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--soft);margin:0 0 3px}""","tabs css")

sub("""  <p class="sub">When the melody is done and you still don't know who's playing it.
  Every entry is checked against Wikipedia on load; anything with no article is dropped.</p>""",
"""  <p class="sub">Mind-sweep decks for making music. Switch decks when you're stuck in one dimension.</p>""","sub")
h=h.replace("<h1>The Instrument Palette</h1>","<h1>Palettes</h1>")
h=h.replace("<title>The Instrument Palette</title>","<title>Palettes — music mind-sweep</title>")

sub("""<div id="roll"></div>""","""<p class="blurb" id="blurb"></p>
<div class="acts">
  <button data-m="brief">Brief</button><button data-m="roll">Roll 3</button>
  <button data-m="collide">Collide</button><button data-m="focus">Focus</button>
  <button data-m="shuffle">Shuffle</button>
</div>
<div id="tray" hidden></div>
<div id="roll"></div>
<div id="focus" hidden></div>""","blurb")

# ---------- 2. palette state + rewritten render ----------
sub("""function render(){
  const out=document.getElementById('out');
  out.innerHTML='';
  for(const g of ORDER[key]){
    const items=DATA.filter(d=>d[key]===g && (showRej? !passes(d.n) : passes(d.n)))
                    .sort((a,b)=>a.n.localeCompare(b.n));
    if(!items.length) continue;
    const sec=document.createElement('section');
    sec.className='group';
    sec.innerHTML='<h2>'+g+' <span>'+items.length+'</span></h2>'+
      (key==='r'&&HINT[g]?'<p class="hint">'+HINT[g]+'</p>':'')+
      '<ul>'+items.map(d=>{
        const i=INFO[d.n];
        const href=(i&&i.url)||wikiURL(d.w);
        const c=[]; if(showRej)c.push('dead'); if(AUD[d.n]&&AUD[d.n].length)c.push('aud');
        const cls=c.length?' class="'+c.join(' ')+'"':'';
        return '<li'+cls+'><span class="snd" aria-hidden="true">\\u266a</span>'+
          '<a href="'+href+'" target="_blank" rel="noopener" data-n="'+esc(d.n)+'">'+esc(d.n)+'</a></li>';
      }).join('')+'</ul>';
    out.appendChild(sec);
  }
  filter();
}""",
"""const WORD=__WORD__;
const DECKS=[['instruments','Instruments']].concat(
  Object.keys(WORD).map(k=>[k,WORD[k].name]));
let PAL='instruments';
let PINS=[], shuf=0;
const isInst=()=>PAL==='instruments';
const curItems=()=>isInst()? DATA : WORD[PAL].items;
const curKey =()=>isInst()? key : 'c';
const curOrder=()=>isInst()? ORDER[key] : WORD[PAL].order;

function render(){
  const out=document.getElementById('out');
  const K=curKey(), inst=isInst();
  out.innerHTML='';
  if(!inst && WORD[PAL].flat){          /* uncategorised deck — one list, flowing */
    const items=arrange(curItems().slice());
    out.innerHTML='<ul class="flatlist">'+items.map(d=>
      '<li'+(PINS.includes(d.n)?' class="pinned"':'')+'><a class="wt" data-n="'+esc(d.n)+'">'+
      esc(d.n)+'</a></li>').join('')+'</ul>';
    filter(); return;
  }
  for(const g of curOrder()){
    const items=curItems()
      .filter(d=>d[K]===g && (inst? (showRej? !passes(d.n) : passes(d.n)) : !showRej));
    arrange(items);
    if(!items.length) continue;
    const sec=document.createElement('section');
    sec.className='group';
    sec.innerHTML='<h2>'+g+' <span>'+items.length+'</span></h2>'+
      (inst&&key==='r'&&HINT[g]?'<p class="hint">'+HINT[g]+'</p>':'')+
      '<ul>'+items.map(d=>{
        if(!inst){
          const cl=PINS.includes(d.n)?' class="pinned"':'';
          const lk=WORD[PAL].lk;
          if(lk==='wp') return '<li'+cl+'><a href="'+wikiURL(d.w||d.n)+
            '" target="_blank" rel="noopener" data-n="'+esc(d.n)+'">'+esc(d.n)+'</a></li>';
          if(lk==='wt') return '<li'+cl+'><a class="wt" data-n="'+esc(d.n)+'">'+esc(d.n)+'</a></li>';
          return '<li'+cl+'>'+esc(d.n)+'</li>';
        }
        const i=INFO[d.n];
        const href=(i&&i.url)||wikiURL(d.w);
        const c=[]; if(showRej)c.push('dead'); if(AUD[d.n]&&AUD[d.n].length)c.push('aud');
        if(PINS.includes(d.n))c.push('pinned');
        const cls=c.length?' class="'+c.join(' ')+'"':'';
        return '<li'+cls+'><span class="snd" aria-hidden="true">\\u266a</span>'+
          '<a href="'+href+'" target="_blank" rel="noopener" data-n="'+esc(d.n)+'">'+esc(d.n)+'</a></li>';
      }).join('')+'</ul>';
    out.appendChild(sec);
  }
  filter();
}

/* shuffle: sweeping in random order breaks the alphabetical rut */
function arrange(a){
  if(shuf){ for(let i=a.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;[a[i],a[j]]=[a[j],a[i]];} }
  else a.sort((x,y)=>x.n.localeCompare(y.n));
  return a;
}
const pick=(arr,k)=>{const p=arr.slice(),o=[];
  while(o.length<k&&p.length)o.push(p.splice((Math.random()*p.length)|0,1)[0]);return o};
function deckItems(id){ return id==='instruments'? DATA.filter(d=>passes(d.n)) : WORD[id].items; }
const tagOf=d=>(d.f? d.r.toLowerCase()+', '+d.f.toLowerCase() : (d.c||''));

/* pin tray — collect scraps from any deck, then copy them out */
function togglePin(n){
  const i=PINS.indexOf(n); if(i<0)PINS.push(n); else PINS.splice(i,1);
  drawTray(); render();
}
function drawTray(){
  const t=document.getElementById('tray');
  if(!PINS.length){ t.hidden=true; return; }
  t.hidden=false;
  t.innerHTML='<span class="lbl2">pinned</span>'+
    PINS.map(n=>'<span class="pill"><b>'+esc(n)+'</b><i data-x="'+esc(n)+'">&times;</i></span>').join('')+
    '<button class="tact" id="tcopy">copy</button><button class="tact" id="tclear">clear</button>';
}
document.addEventListener('click',e=>{
  const x=e.target.closest('#tray i[data-x]'); if(x){ togglePin(x.dataset.x); return; }
  if(e.target.id==='tcopy'){ try{navigator.clipboard.writeText(PINS.join(', '))}catch(err){}
    e.target.textContent='copied'; setTimeout(()=>e.target.textContent='copy',1200); return; }
  if(e.target.id==='tclear'){ PINS=[]; drawTray(); render(); return; }
  const li=e.target.closest('#out li');
  if(li&&!isInst()&&WORD[PAL].lk!=='wp') togglePin(li.textContent.trim());
});

function showRoll(html){ const r=document.getElementById('roll');
  r.style.display='block'; r.innerHTML=html; }
const fmt=d=>{const t=tagOf(d);
  return '<b>'+esc(d.n)+'</b>'+(t?' <span style="opacity:.65">('+esc(t)+')</span>':'');};
function modeRoll(){ const p=pick(deckItems(PAL),3);
  showRoll('<span class="lbl">try building around these three</span>'+p.map(fmt).join(' &nbsp;&middot;&nbsp; ')); }
function modeCollide(){ const p=pick(deckItems(PAL),2); if(p.length<2)return;
  showRoll('<span class="lbl">force these two together</span>'+fmt(p[0])+'<span class="pairx">&times;</span>'+fmt(p[1])); }
/* Brief: one draw from every deck at once — a whole starting point, not a word */
function modeBrief(){
  const rows=DECKS.map(([id,label])=>{ const it=pick(deckItems(id),1)[0]; if(!it)return '';
    return '<span class="brow"><span class="bk">'+esc(label)+'</span><b>'+esc(it.n)+'</b></span>'; }).join('');
  showRoll('<span class="lbl">one brief, drawn from every deck</span>'+rows);
}
let focusCur=null;
function modeFocus(){
  const f=document.getElementById('focus'), d=pick(deckItems(PAL),1)[0]; if(!d)return;
  focusCur=d.n; f.hidden=false;
  f.innerHTML='<p class="cat">'+esc(tagOf(d)||(WORD[PAL]?WORD[PAL].name:''))+'</p>'+
    '<p class="big">'+esc(d.n)+'</p><div class="row">'+
    '<button data-f="next">Another</button><button data-f="pin">'+
    (PINS.includes(d.n)?'Unpin':'Pin')+'</button><button data-f="close">Close</button></div>'+
    '<p class="cat" style="opacity:.6">N another &nbsp; P pin &nbsp; Esc close</p>';
}
document.addEventListener('click',e=>{
  const b=e.target.closest('#focus button'); if(!b)return;
  if(b.dataset.f==='next') modeFocus();
  else if(b.dataset.f==='pin'){ togglePin(focusCur); modeFocus(); }
  else document.getElementById('focus').hidden=true;
});
document.addEventListener('click',e=>{
  const b=e.target.closest('.acts button'); if(!b)return;
  const m=b.dataset.m;
  if(m==='roll')modeRoll(); else if(m==='collide')modeCollide();
  else if(m==='brief')modeBrief(); else if(m==='focus')modeFocus();
  else { shuf=!shuf; b.textContent=shuf?'Unshuffle':'Shuffle'; render(); }
});
addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  const f=document.getElementById('focus');
  if(e.key==='Escape'){ f.hidden=true; hide(); }
  else if(!f.hidden&&/^[nN]$/.test(e.key)) modeFocus();
  else if(!f.hidden&&/^[pP]$/.test(e.key)){ togglePin(focusCur); modeFocus(); }
  else if(/^[rR]$/.test(e.key)) modeRoll();
  else if(/^[bB]$/.test(e.key)) modeBrief();
});

/* deck switching: the Wikipedia/audio machinery belongs to the instrument deck only,
   so the word decks render instantly and hide the controls that mean nothing to them. */
function buildTabs(){
  const t=document.getElementById('tabs');
  t.innerHTML=DECKS.map(([id,label])=>
    '<button data-p="'+id+'"'+(id===PAL?' class="on"':'')+'>'+esc(label)+'</button>').join('');
}
function selectPalette(p){
  PAL=p; showRej=false; key='f';
  document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('on',b.dataset.p===p));
  const inst=isInst();
  document.getElementById('seg').style.display=inst?'':'none';
  document.getElementById('status').style.display=inst?'':'none';
  const rb=document.getElementById('rej');
  rb.style.display=inst?'':'none';
  if(inst) rb.textContent='show '+((window.__UNRESOLVED__||[]).length)+' with no article';
  document.querySelectorAll('#seg button').forEach((b,i)=>b.classList.toggle('on',i===0));
  document.getElementById('blurb').textContent=inst
    ? 'Every entry is checked against Wikipedia on load; anything with no article is dropped. Hover for a picture, the opening line, and a recording where one exists.'
    : WORD[p].blurb;
  document.getElementById('q').value='';
  document.getElementById('roll').style.display='none';
  document.getElementById('focus').hidden=true;
  shuf=0; const sb=document.querySelector('.acts button[data-m="shuffle"]');
  if(sb) sb.textContent='Shuffle';
  hide(); render(); scrollTo(0,0);
}
document.addEventListener('click',e=>{
  const b=e.target.closest('#tabs button'); if(b) selectPalette(b.dataset.p);
});""","render")

h=h.replace("__WORD__",WJSON)

# ---------- 3. count + roll are palette-aware ----------
sub("""  const shown=document.querySelectorAll('#out li').length;
  document.getElementById('count').textContent =
    v? (n+' match'+(n===1?'':'es')) : (shown+' instruments');""",
"""  const shown=document.querySelectorAll('#out li').length;
  document.getElementById('count').textContent =
    v? (n+' match'+(n===1?'':'es')) : (shown+(isInst()?' instruments':' entries'));""","count")

sub("""  const p=[...DATA],pick=[];
  while(pick.length<3) pick.push(p.splice(Math.floor(Math.random()*p.length),1)[0]);
  const r=document.getElementById('roll');
  r.style.display='block';
  r.innerHTML='<span class="lbl">try building around these three</span>'+
    pick.map(d=>'<b>'+esc(d.n)+'</b> <span style="opacity:.65">('+d.r.toLowerCase()+', '+d.f.toLowerCase()+')</span>').join(' &nbsp;·&nbsp; ');""",
"""  const p=[...curItems()],pick=[];
  while(pick.length<3&&p.length) pick.push(p.splice(Math.floor(Math.random()*p.length),1)[0]);
  const r=document.getElementById('roll');
  r.style.display='block';
  r.innerHTML='<span class="lbl">try building around these three</span>'+
    pick.map(d=>'<b>'+esc(d.n)+'</b> <span style="opacity:.65">('+
      esc(isInst()? d.r.toLowerCase()+', '+d.f.toLowerCase() : d.c.toLowerCase())+')</span>')
      .join(' &nbsp;·&nbsp; ');""","roll")

# ---------- 4. print: hide tabs, keep blurb out ----------
sub(".bar,.dice,#roll,#card,#status,#rej,li .snd{display:none!important}",
    ".bar,.dice,#roll,#card,#status,#rej,li .snd,.tabs,.blurb,.acts,#tray,#focus{display:none!important}","print")

# ---------- 5. boot ----------
sub("render(); loadAll();","buildTabs(); selectPalette('instruments'); loadAll();","boot")

sub("""'<p class="m">'+esc(meta)+'</p></div>';""",
    """'<p class="m">'+esc(meta)+' &nbsp;<button class="alt" id="pin">'+
      (PINS.includes(name)?'unpin':'pin')+'</button></p></div>';""","card pin")
sub("""  const alt=card.querySelector('#alt');""",
    """  const pn=card.querySelector('#pin');
  if(pn) pn.onclick=()=>{ togglePin(name); paint(name); if(curEl)place(curEl); };
  const alt=card.querySelector('#alt');""","card pin wire")

ENG=open('engines.js').read()
sub("/* ---------- hover card ---------- */", ENG, "engines")
sub("""async function show(el){
  clearTimeout(hideT);
  const name=el.dataset.n;
  if(cur!==name) altIdx=0;
  cur=name; curEl=el;""",
"""async function show(el){
  clearTimeout(hideT);
  const name=el.dataset.n;
  if(cur!==name) altIdx=0;
  cur=name; curEl=el;
  if(!isInst()){
    const lk=WORD[PAL].lk; if(!lk) return;
    paintWord(name); card.classList.add('show'); card.setAttribute('aria-hidden','false'); place(el);
    if(!CARD2[ckey(PAL,name)]){
      await (lk==='wp'? lookupWP(name) : lookupWT(name));
      if(cur===name){ paintWord(name); place(el);
        const c=CARD2[ckey(PAL,name)]; if(c&&c.url&&el.tagName==='A'&&lk==='wp') el.href=c.url; }
    }
    return;
  }""","show route")

open('../index.html','w').write(h)
print(len(WORD),"word decks |",sum(len(v['items']) for v in WORD.values()),"words |",len(h),"bytes")
