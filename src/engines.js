/* ---------- lookups for the word decks ----------
   Wikipedia for theory / production / genre (they're real articles), Wiktionary for
   adjectives / abstract nouns / emotions (they're words, not topics). Both fire on
   hover only — no bulk prefetch, so switching decks stays instant. */
const CARD2=Object.create(null);            // "deck|name" -> {title,extract,thumb,url,pos,state}
const ckey=(p,n)=>p+'|'+n;
function itemOf(name){
  const L=WORD[PAL]; if(!L)return null;
  if(!L._map){ L._map=Object.create(null); L.items.forEach(i=>L._map[i.n]=i); }
  return L._map[name];
}
async function lookupWP(name){
  const k=ckey(PAL,name), it=itemOf(name); if(CARD2[k]||!it)return;
  try{
    let js=await jsonp({action:'query',prop:'extracts|pageimages',exintro:'1',explaintext:'1',
      exsentences:'2',piprop:'thumbnail',pithumbsize:'420',redirects:'1',titles:(it.w||name)});
    let p=Object.values((js.query&&js.query.pages)||{})[0];
    if(!p||p.missing!==undefined){
      js=await jsonp({action:'query',generator:'search',
        gsrsearch:name+' '+(WORD[PAL].hint||''),gsrlimit:'1',
        prop:'extracts|pageimages',exintro:'1',explaintext:'1',exsentences:'2',
        piprop:'thumbnail',pithumbsize:'420'});
      p=Object.values((js.query&&js.query.pages)||{})[0];
    }
    if(!p) throw 0;
    CARD2[k]={title:p.title,url:wikiURL(p.title),extract:(p.extract||'').trim(),
      thumb:(p.thumbnail&&p.thumbnail.source)||'',state:'ok'};
  }catch(e){ CARD2[k]={state:'fail'} }
}
/* Wiktionary is CASE-SENSITIVE: "Frigid" 404s where "frigid" exists, so try the
   lowercase entry first. For invented compounds ("grateful grief") nothing exists at
   the phrase, so fall back to defining the head word. Preferred part of speech follows
   the deck — the Adjectives deck wants the adjective sense, not the noun. */
function wtVariants(name){
  const v=[], add=x=>{ if(x && !v.includes(x)) v.push(x); };
  add(name.toLowerCase());
  add(name);
  const parts=name.trim().split(/[\s\u2013-]+/);
  if(parts.length>1){ add(parts[parts.length-1].toLowerCase()); add(parts[0].toLowerCase()); }
  return v;
}
function wtPick(en,order){
  let best=null;
  for(const w of order){ best=en.find(s=>(s.partOfSpeech||'').toLowerCase()===w); if(best)break; }
  best=best||en[0];
  if(!best) return null;
  const d=(best.definitions||[]).find(x=>x.definition&&x.definition.replace(/<[^>]+>/g,'').trim());
  if(!d) return null;
  let t=d.definition.replace(/<[^>]+>/g,'').replace(/&[a-z]+;/g,' ').replace(/\s+/g,' ').trim();
  t=t.replace(/^\((?:[^()]|\([^()]*\))*\)\s*/,'');       // drop leading (context) tags
  const cut=t.match(/^[^.;:]+[.;:]?/); if(cut) t=cut[0].replace(/[;:]$/,'.');
  t=t.trim(); if(!t) return null;
  if(!/[.!?]$/.test(t)) t+='.';
  return {t:t.charAt(0).toUpperCase()+t.slice(1), pos:best.partOfSpeech||''};
}
async function lookupWT(name){
  const k=ckey(PAL,name); if(CARD2[k])return;
  const POS={adjective:['adjective','noun','verb'],verb:['verb','noun','adjective']};
  const order = POS[PAL] || ['noun','adjective','verb'];
  for(const v of wtVariants(name)){
    try{
      const r=await fetch('https://en.wiktionary.org/api/rest_v1/page/definition/'+
        encodeURIComponent(v.replace(/ /g,'_')));
      if(!r.ok) continue;
      const js=await r.json();
      const got=wtPick(js.en||[],order);
      if(!got) continue;
      CARD2[k]={extract:got.t,pos:got.pos,title:v,
        url:'https://en.wiktionary.org/wiki/'+encodeURIComponent(v.replace(/ /g,'_')),
        via:(v.toLowerCase()!==name.toLowerCase()? v : ''),state:'ok'};
      return;
    }catch(e){}
  }
  CARD2[k]={state:'fail'};
}
function paintWord(name){
  const it=itemOf(name), lk=WORD[PAL].lk, c=CARD2[ckey(PAL,name)];
  const meta=(it&&it.c)? WORD[PAL].name+' · '+it.c : WORD[PAL].name;
  let head='', body='<p class="t">'+esc(name)+'</p>';
  if(!c) body+='<p class="load">looking it up…</p>';
  else if(c.state==='fail') body+='<p class="def" style="opacity:.6">No entry found — the word still stands.</p>';
  else{
    if(lk==='wp'&&c.thumb) head='<img class="ph" src="'+c.thumb+'" alt="">';
    if(c.pos) body+='<p class="pos">'+esc(c.pos)+(c.via?' &middot; from &ldquo;'+esc(c.via)+'&rdquo;':'')+'</p>';
    body+='<p class="def">'+esc(c.extract||'')+'</p>';
  }
  card.innerHTML=head+'<div class="body">'+body+'<p class="m">'+esc(meta)+
    ' &nbsp;<button class="alt" id="pin">'+(PINS.includes(name)?'unpin':'pin')+'</button></p></div>';
  const pn=card.querySelector('#pin');
  if(pn) pn.onclick=()=>{ togglePin(name); paintWord(name); if(curEl)place(curEl); };
}

/* ---------- hover card ---------- */
