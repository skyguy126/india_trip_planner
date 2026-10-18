/* Pure presentation rules: editorial categories, climate tendencies and concise activities. */
const TripPresentation=(()=>{
 const categories=[
  {id:'sacred',name:'Temples & shrines',symbol:'◈',pattern:/temple|mandir|shrine|gur[ud]+wara|gurdwara|masjid|mosque|imambara|monaster|pilgrimage|sacred|stupa|dargah|langar|aarti/},
  {id:'history',name:'History & forts',symbol:'▥',pattern:/fort\b|palace|heritage|history|historical|tomb|archaeolog|ruins|monument|stepwell|rock.carv|havel|imambara|minar|residency/},
  {id:'adventure',name:'Adventure',symbol:'↗',pattern:/adventure|trek|hiking|hike|climb|paraglid|rafting|surf|kayak|rappell|caving|canyon|skiing|camping|balloon|parasail|dune bashing/},
  {id:'mountains',name:'Mountains & hikes',symbol:'△',pattern:/mountain|hill|trek|hiking|hike|summit|ridge|alpine|glacier|himalay|ghats|bugyal/},
  {id:'water',name:'Water & beaches',symbol:'≈',pattern:/lake|river|coast|beach|waterfall|backwater|lagoon|kayak|rafting|surf|island|boat|ferr/},
  {id:'wildlife',name:'Wildlife & forests',symbol:'❧',pattern:/wildlife|national park|tiger|forest|wetland|bird|safari|sanctuary|blackbuck|leopard|naturalist/},
  {id:'caves',name:'Caves',symbol:'⌁',pattern:/cave|caving|limestone|stalactite/},
  {id:'cities',name:'Cities & food',symbol:'▦',pattern:/city|cities|old.town|market|bazaar|food|cuisine|café|cafe|street|culinary/},
  {id:'culture',name:'Culture & villages',symbol:'⌂',pattern:/culture|cultural|village|craft|weav|pottery|local.life|heritage|plantation|tea estate/},
  {id:'stars',name:'Stars & night skies',symbol:'✧',pattern:/stargaz|night.sky|night sky|astrophot|milky way|dark.sk/}
 ];
 function categoriesFor(d){const text=[d.name,...(d.tags||[]),...(d.activities||[])].join(' ').toLowerCase();return categories.filter(c=>c.pattern.test(text)).map(c=>c.id);}
 function matches(d,selected){return !selected.size||categoriesFor(d).some(id=>selected.has(id));}
 const fahrenheit=c=>Math.round(c*9/5+32);
 function weather(d,w,month){if(w.hi<=5)return {kind:'snow',label:'Cold · snow or ice possible',glyph:'❄'};if((w.rain??0)>=80||(['southeast'].includes(d.climate)&&[10,11,12].includes(month))||([6,7,8,9].includes(month)&&!['leh'].includes(d.climate)))return {kind:'rain',label:'Rainy-season influence',glyph:'☂'};if(w.lo<5)return {kind:'snow',label:'Cold nights · layered clothing',glyph:'❄'};if(w.hi>=30)return {kind:'sun',label:'Warm / hot days',glyph:'☀'};return {kind:'mixed',label:'Mild days · cooler evenings',glyph:'⛅'};}
 function experience(raw){const clean=String(raw).trim(),first=clean.split(/(?<=[.!?])\s+/)[0],parts=first.split(/\s[—–]\s|:\s/),title=parts[0].length<=64?parts[0]:parts[0].split(/\s+/).slice(0,7).join(' '),tail=parts.length>1?parts.slice(1).join(' — '):first.length>64?first.slice(title.length).replace(/^[,;:.\s]+/,''):'';
  const rules=[[/closur|permit|clearance/i,'Check the linked access requirements before planning.'],[/cav|limestone|geology/i,'Explore the permitted route with an experienced cave guide.'],[/raft|kayak|surf|paraglid|parasail|rappell|skiing|climb/i,'Arrange a suitable operator and confirm current conditions.'],[/trek|walk|trail|hike|ridge|summit|viewpoint/i,'Follow the authorized route for scenery and photo stops.'],[/temple|monaster|shrine|devotion|masjid|mosque|langar|aarti/i,'Visit respectfully and check current worship-site access.'],[/fort|palace|ruin|tomb|architect|heritage|stepwell/i,'Explore the open precinct and its architectural details.'],[/food|cuisine|cafe|café|market|bazaar/i,'Leave time for local flavors and unhurried street exploration.'],[/lake|boat|waterfront|river|ghat|beach/i,'Enjoy the waterside setting; arrange any boat outing separately.'],[/wildlife|bird|safari|forest/i,'Use permitted viewing routes; sightings are never guaranteed.'],[/star|night.sky|milky/i,'Plan around cloud cover, moonlight and local night access.'],[/plantation|tea|village|craft|pottery/i,'Arrange local access and ask before photographing people at work.']];
  const phrase=tail||rules.find(([re])=>re.test(first))?.[1]||'';
  return {title,description:phrase.length>135?phrase.slice(0,132).replace(/\s+\S*$/,'')+'…':phrase};
 }
 return {categories,categoriesFor,matches,fahrenheit,weather,experience};
})();
if(typeof module!=='undefined')module.exports=TripPresentation;
