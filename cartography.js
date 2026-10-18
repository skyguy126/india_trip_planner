/* Planning-map hierarchy. Country polygons: Mapbox Countries v1; state lines: Streets v8.
   Preserve the Outdoors style's all/US worldview and visibly distinguish disputed lines. */
const TripCartography=(()=>{
 const WORLDVIEW=['any',['==',['get','worldview'],'all'],['in','US',['coalesce',['get','worldview'],'']]];
 const name=['coalesce',['get','name_en'],['get','name'],''];
 const fc=features=>({type:'FeatureCollection',features});
 const point=(label,lon,lat,props={})=>({type:'Feature',properties:{name:label,...props},geometry:{type:'Point',coordinates:[lon,lat]}});
 const regions={nepal:{name:'Nepal',bounds:[[80.0,26.3],[88.3,30.5]]},bhutan:{name:'Bhutan',bounds:[[88.7,26.6],[92.2,28.4]]},andamans:{name:'Andaman Islands',bounds:[[91.6,10.35],[96.1,14.4]]}};
 const stateRows=`Rajasthan|73.8|26.4|large
Gujarat|71.5|22.6|large
Maharashtra|76.0|19.5|large
Madhya Pradesh|78.1|23.5|large
Uttar Pradesh|80.8|27.2|large
Bihar|85.6|25.8|large
West Bengal|87.5|23.3|large
Odisha|84.5|20.3|large
Chhattisgarh|82.0|21.2|large
Jharkhand|85.5|23.7|large
Telangana|79.1|17.9|large
Andhra Pradesh|80.0|15.7|large
Karnataka|76.2|14.9|large
Kerala|76.4|10.2|large
Tamil Nadu|78.5|10.8|large
Himachal Pradesh|77.2|31.8|small
Uttarakhand|79.2|30.1|small
Punjab|75.3|31.0|small
Haryana|76.0|29.3|small
Assam|92.8|26.5|small
Arunachal Pradesh|94.5|28.1|small
Sikkim|88.5|27.6|small
Meghalaya|91.3|25.55|small
Nagaland|94.5|26.1|small
Manipur|93.9|24.7|small
Mizoram|92.8|23.2|small
Tripura|91.6|23.8|small
Goa|74.0|15.3|small
Ladakh|77.8|34.0|small
Jammu & Kashmir|75.0|33.65|small
Delhi|77.1|28.7|ut
Chandigarh|76.8|30.75|ut
Puducherry|79.8|11.9|ut
Lakshadweep|72.6|10.6|ut
Andaman & Nicobar Islands|92.8|9.2|ut
Dadra & Nagar Haveli and Daman & Diu|72.95|20.3|ut`;
 // The Andaman island group retains a prominent text label below;
 // no manually drawn state or country geometry is used for these text anchors.
 const statePoints=stateRows.split('\n').map((r,i)=>{const [n,x,y,group]=r.split('|');return point(n,+x,+y,{kind:'state',group,priority:i});});
 const anchorRows=`Manali|77.189|32.243|5.5
Naggar|77.173|32.116|7.5
Bir|76.722|32.040|6.5
Barot|76.845|32.041|8
McLeod Ganj|76.320|32.239|6.5
Shimla|77.173|31.105|5.5
Narkanda|77.465|31.258|7.5
Kalpa|78.252|31.538|7
Chitkul|78.437|31.351|8
Kaza|78.071|32.224|6.5
Keylong|77.032|32.571|7
Dalhousie|75.966|32.538|7
Gulmarg|74.381|34.049|6.5
Pahalgam|75.318|34.017|6.5
Sonamarg|75.293|34.299|7
Gurez|74.750|34.633|7.5
Leh|77.584|34.153|5.5
Diskit|77.550|34.550|7.5
Hanle|78.964|32.780|8
Rishikesh|78.268|30.087|5.5
Haridwar|78.164|29.946|6
Joshimath|79.565|30.553|7
Uttarkashi|78.450|30.726|7
Harsil|78.727|31.038|8
Munsiyari|80.238|30.068|7.5
Shillong|91.893|25.578|5.5
Sohra|91.732|25.270|7
Dawki|92.025|25.184|8
Jowai|92.197|25.450|7.5
Tawang|91.862|27.586|6.5
Dirang|92.249|27.359|7.5
Ziro|93.825|27.544|7
Mechuka|94.128|28.602|8
Gangtok|88.613|27.338|5.5
Pelling|88.233|27.300|7.5
Lachung|88.745|27.690|8
Darjeeling|88.263|27.041|6.5
Kalimpong|88.470|27.060|7.5
Khonoma|94.021|25.652|8
Pushkar|74.551|26.490|7
Bundi|75.650|25.430|7
Khajuraho|79.922|24.832|7
Orchha|78.641|25.351|7.5
Hampi|76.461|15.335|7
Gokarna|74.319|14.548|7
Fort Kochi|76.242|9.965|8
Munnar|77.062|10.089|7
Varkala|76.716|8.737|7.5
Kodaikanal|77.489|10.239|7
Sri Vijaya Puram|92.727|11.667|6.5
Pokhara|83.986|28.210|5.5
Nagarkot|85.520|27.717|7.5
Bhaktapur|85.429|27.672|7
Bandipur|84.407|27.938|8
Sarangkot|83.948|28.244|8
Thimphu|89.639|27.472|6
Paro|89.413|27.430|7.5
Punakha|89.864|27.592|8`;
 const anchors=anchorRows.split('\n').map((r,i)=>{const [n,x,y,minZoom]=r.split('|');return point(n,+x,+y,{kind:'town',minZoom:+minZoom,priority:i});});
 const aliases=[...new Set([...anchors.map(f=>f.properties.name),'Dharamsala','Dharamshala','Dharmsala','McLeodganj','McLeodGanj','Cherrapunji','Cherrapunjee','Sohra (Cherrapunjee)','Joshimath','Jyotirmath','Port Blair','Kaza Khas'])];
 function geography(){return fc([...statePoints,...anchors,point('NEPAL',84.1,28.55,{kind:'focus',key:'nepal'}),point('BHUTAN',90.45,27.5,{kind:'focus',key:'bhutan'}),point('ANDAMAN\nISLANDS',94.6,12.6,{kind:'focus',key:'andamans'})]);}
 const rank=['coalesce',['get','symbolrank'],19],capital=['==',['get','capital'],2];
 const cityFilter=['all',WORLDVIEW,['in',['get','class'],['literal',['settlement','disputed_settlement']]],['in',['get','type'],['literal',['city','town']]],['<=',['coalesce',['get','filterrank'],3],3],['!', ['in',name,['literal',aliases]]],['any',['in',['get','iso_3166_1'],['literal',['IN','NP','BT']]],['<=',rank,7]],['step',['zoom'],['any',capital,['<=',rank,6]],5,['any',capital,['<=',rank,8]],6.5,['<=',rank,10],8,['<=',rank,12],9.5,['<=',rank,14],11,['<=',rank,16]]];
 function install(map){
  const layers=map.getStyle().layers||[],streets=layers.find(l=>l['source-layer']==='admin')?.source||'composite',placeSource=layers.find(l=>l['source-layer']==='place_label')?.source||streets;
  const beforeFill=layers.find(l=>l.type==='line')?.id,beforeLabel=layers.find(l=>l.type==='symbol')?.id;
  const add=(l,before)=>{if(!map.getLayer(l.id))map.addLayer(l,before);};
  if(!map.getSource('trip-countries'))map.addSource('trip-countries',{type:'vector',url:'mapbox://mapbox.country-boundaries-v1'});
  if(!map.getSource('trip-geography'))map.addSource('trip-geography',{type:'geojson',data:geography()});
  const countryFilter=['all',WORLDVIEW,['==',['get','disputed'],'false'],['in',['get','iso_3166_1'],['literal',['IN','NP','BT']]]];
  const countries={source:'trip-countries','source-layer':'country_boundaries',filter:countryFilter};
  add({id:'trip-country-tints',type:'fill',...countries,paint:{'fill-color':'#5c896e','fill-opacity':.05}},beforeFill);
  add({id:'trip-country-halo',type:'line',...countries,layout:{'line-join':'round'},paint:{'line-color':'#fffdf5','line-width':5,'line-opacity':.95}},beforeLabel);
  add({id:'trip-country-outlines',type:'line',...countries,layout:{'line-join':'round'},paint:{'line-color':'#285d4d','line-width':2.4}},beforeLabel);
  const stateFilter=['all',WORLDVIEW,['==',['get','admin_level'],1],['==',['get','iso_3166_1'],'IN'],['==',['get','maritime'],'false']];
  add({id:'trip-state-halo',type:'line',source:streets,'source-layer':'admin',filter:stateFilter,minzoom:3,paint:{'line-color':'#fffdf5','line-width':['interpolate',['linear'],['zoom'],3,3.6,7,4.8],'line-opacity':.85}},beforeLabel);
  add({id:'trip-state-lines',type:'line',source:streets,'source-layer':'admin',filter:stateFilter,minzoom:3,paint:{'line-color':'#617e72','line-width':['interpolate',['linear'],['zoom'],3,1.4,7,2.1],'line-dasharray':[5,1.8]}},beforeLabel);
  const disputed=['all',WORLDVIEW,['==',['get','admin_level'],0],['==',['get','disputed'],'true'],['==',['get','maritime'],'false'],['in','IN',['coalesce',['get','iso_3166_1'],'']]];
  add({id:'trip-disputed-halo',type:'line',source:streets,'source-layer':'admin',filter:disputed,paint:{'line-color':'#fffdf5','line-width':5.3}},beforeLabel);
  add({id:'trip-disputed-lines',type:'line',source:streets,'source-layer':'admin',filter:disputed,paint:{'line-color':'#8b7952','line-width':2.5,'line-dasharray':[2.2,1.7]}},beforeLabel);
  // Regional labels are placed first so city labels respect their collision boxes.
  for(const [group,z,max] of [['large',3,10],['small',3.7,10.5],['ut',5.3,11]])add({id:'trip-state-labels-'+group,type:'symbol',source:'trip-geography',minzoom:z,maxzoom:max,filter:['all',['==',['get','kind'],'state'],['==',['get','group'],group]],layout:{'text-field':['get','name'],'text-font':['DIN Pro Bold','Arial Unicode MS Bold'],'text-size':['interpolate',['linear'],['zoom'],3,12,6,16,9,20],'text-transform':'uppercase','text-letter-spacing':.045,'text-max-width':9,'text-line-height':1.2,'text-padding':6,'text-allow-overlap':false,'symbol-sort-key':['get','priority']},paint:{'text-color':'#3e6653','text-halo-color':'#fffdf5','text-halo-width':2.5,'text-halo-blur':.35,'text-opacity':1}},beforeLabel);
  add({id:'trip-focus-labels',type:'symbol',source:'trip-geography',minzoom:2.5,maxzoom:9,filter:['==',['get','kind'],'focus'],layout:{'text-field':['get','name'],'text-font':['DIN Pro Bold','Arial Unicode MS Bold'],'text-size':['interpolate',['linear'],['zoom'],3,12,6,18],'text-letter-spacing':.1,'text-max-width':9,'text-padding':4,'text-allow-overlap':false},paint:{'text-color':'#986c37','text-halo-color':'#fffdf5','text-halo-width':2}},beforeLabel);
  const bins=[...new Set(anchors.map(f=>f.properties.minZoom))].sort((a,b)=>a-b);
  for(const z of bins)add({id:'trip-travel-towns-'+String(z).replace('.','_'),type:'symbol',source:'trip-geography',minzoom:z,maxzoom:15,filter:['all',['==',['get','kind'],'town'],['==',['get','minZoom'],z]],layout:{'text-field':['get','name'],'text-font':['DIN Pro Medium','Arial Unicode MS Regular'],'text-size':['interpolate',['linear'],['zoom'],5,11,10,13,14,16],'text-variable-anchor':['left','right','top','bottom'],'text-radial-offset':.9,'text-max-width':8,'text-padding':5,'symbol-sort-key':['get','priority'],'text-allow-overlap':false},paint:{'text-color':'#24493d','text-halo-color':'#fffdf5','text-halo-width':1.7}},beforeLabel);
  add({id:'trip-context-cities',type:'symbol',source:placeSource,'source-layer':'place_label',minzoom:2.5,maxzoom:18,filter:cityFilter,layout:{'text-field':name,'text-font':['DIN Pro Medium','Arial Unicode MS Regular'],'text-size':['interpolate',['linear'],['zoom'],3,11,7,12.5,12,15,16,18],'text-variable-anchor':['left','right','top','bottom'],'text-radial-offset':.5,'text-max-width':8,'text-padding':5,'text-allow-overlap':false,'symbol-sort-key':rank},paint:{'text-color':'#3d4c49','text-halo-color':'#fffdf5','text-halo-width':1.5}},beforeLabel);
  for(const l of layers){
   if(l.id.startsWith('trip-'))continue;
   if(l['source-layer']==='place_label'&&l.id!=='country-label')map.setLayoutProperty(l.id,'visibility','none');
   if(l.id==='country-label')map.setFilter(l.id,['all',l.filter||true,['!', ['in',['get','iso_3166_1'],['literal',['NP','BT']]]]]);
   if(l['source-layer']==='poi_label')map.setLayerZoomRange(l.id,12,24);
   if(l['source-layer']==='natural_label'&&l.id==='natural-point-label')map.setLayerZoomRange(l.id,8,24);
   if(l.id==='settlement-subdivision-label'){map.setLayerZoomRange(l.id,13,24);map.setLayoutProperty(l.id,'visibility','visible');}
  }
 }
 function paint(map,dark,reduced=false){if(!map)return;const halo=dark?'#182e2a':'#fffdf5',ink=dark?'#e0f0d3':'#244d38',duration=reduced?0:450;
  const set=(id,properties)=>{if(!map.getLayer(id))return;for(const [key,value] of Object.entries(properties)){if(/color$|opacity$/.test(key))map.setPaintProperty(id,key+'-transition',{duration,delay:0});map.setPaintProperty(id,key,value);}};
  set('trip-country-tints',{'fill-color':['match',['get','iso_3166_1'],'NP',dark?'#d5ad65':'#b88b45','BT',dark?'#c3a4d4':'#a384b3',dark?'#7ea58b':'#6c9a7a'],'fill-opacity':['match',['get','iso_3166_1'],['NP','BT'],dark?.2:.15,.035]});
  set('trip-country-halo',{'line-color':halo,'line-opacity':.95});
  set('trip-country-outlines',{'line-color':['match',['get','iso_3166_1'],'NP',dark?'#e3bc78':'#98713e','BT',dark?'#c6a9d7':'#8a6c9d',dark?'#b5d9b4':'#2d624d'],'line-width':['interpolate',['linear'],['zoom'],3,1.9,6,2.8,10,3.2]});
  set('trip-state-halo',{'line-color':halo});set('trip-state-lines',{'line-color':dark?'#c5d8a5':'#3f6d46'});set('trip-disputed-halo',{'line-color':halo});set('trip-disputed-lines',{'line-color':dark?'#e0bf84':'#8b7952'});
  for(const group of ['large','small','ut'])set('trip-state-labels-'+group,{'text-color':ink,'text-halo-color':halo});
  set('trip-focus-labels',{'text-color':['match',['get','key'],'nepal',dark?'#edc889':'#805d2f','bhutan',dark?'#d6b8e7':'#7d5d92',dark?'#8ee1e3':'#126875'],'text-halo-color':halo});
  for(const z of new Set(anchors.map(f=>f.properties.minZoom)))set('trip-travel-towns-'+String(z).replace('.','_'),{'text-color':dark?'#e2ece4':'#284e40','text-halo-color':halo});
  set('trip-context-cities',{'text-color':dark?'#bed0c8':'#4c5c55','text-halo-color':halo});
  set('country-label',{'text-color':['match',['get','iso_3166_1'],'IN',dark?'#c5dfc3':'#3e6652',dark?'#91aaa1':'#6f8075'],'text-halo-color':halo,'text-opacity':.85});
 }
 function fallback(project,dark){const ink=dark?'#a0cec0':'#3d6f5d',halo=dark?'#182e2a':'#f4f6ed';return geography().features.filter(f=>f.properties.kind==='focus').map(f=>{const [x,y]=project(...f.geometry.coordinates);return `<text x="${x}" y="${y}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="1.2" fill="${ink}" stroke="${halo}" stroke-width="3" paint-order="stroke">${f.properties.name.replace('\n',' ')}</text>`;}).join('');}
 return {install,paint,regions,geography,cityFilter,aliases,fallback};
})();
if(typeof module!=='undefined')module.exports=TripCartography;
