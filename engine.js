/* Pure offline transport graph and stop-order optimizer. No live APIs. */
const TripEngine = (() => {
  const finite = n => Number.isFinite(n);
  function valueOfTime(balance=50){return balance>=100?1e7:500*Math.pow(balance/(100-balance),2);}
  function allowed(d,month){return !d.closedMonths.includes(month);}
  function amounts(e,party){const m=e.basis==='vehicle'?Math.ceil(party/4):party;return {low:e.low*m,high:e.high*m};}
  function edgeHours(e){return e.hours+(e.mode==='flight'?(e.a==='KTM'||e.b==='KTM'?3:2):e.mode==='train'?.5:0);}
  function hubService(data){
    const flight=new Map(),train=new Map(),boat=new Map();
    for(const e of data.edges){
      const bump=(m,a,b)=>{m.set(a,(m.get(a)||0)+1);m.set(b,(m.get(b)||0)+1);};
      if(e.mode==='flight')bump(flight,e.a,e.b);else if(e.mode==='train')bump(train,e.a,e.b);else if(e.mode==='boat')bump(boat,e.a,e.b);
    }
    const served=id=>(flight.get(id)||0)+(train.get(id)||0)+(boat.get(id)||0)>0;
    // Prefer real commercial gateways over thin regional strips (e.g. Chandigarh over Dharamshala for Manali).
    const viable=id=>(flight.get(id)||0)>=2||(train.get(id)||0)>=2||(boat.get(id)||0)>=1;
    return {served,viable};
  }
  // One last-mile feeder per flightless hub → closest viable airport/railhead.
  function feederEdgeIds(data,month){
    const {served,viable}=hubService(data),best=new Map();
    const consider=(preferViable)=>{
      for(const e of data.edges){
        if(e.mode!=='road'||e.access||!e.months.includes(month))continue;
        const a=served(e.a),b=served(e.b);if(a===b)continue;
        const orphan=a?e.b:e.a,gate=a?e.a:e.b;
        if(preferViable&&!viable(gate))continue;
        // Fallback only fills hubs that had no viable gateway — never replace a major hub with a shorter regional strip.
        if(!preferViable&&best.has(orphan))continue;
        const prev=best.get(orphan);
        if(!prev||e.hours<prev.hours)best.set(orphan,{id:e.id,hours:e.hours});
      }
    };
    consider(true);consider(false);
    return new Set([...best.values()].map(v=>v.id));
  }
  function build(data,settings={}) {
    const s={month:12,party:1,balance:50,modes:['flight','train','boat'],...settings};
    const modes=s.modes.filter(m=>m!=='road');
    const adj=Object.fromEntries(data.nodes.map(n=>[n.id,[]]));
    const closed=new Set(data.destinations.filter(d=>!allowed(d,s.month)).map(d=>d.id));
    const feeders=feederEdgeIds(data,s.month);
    const vot=valueOfTime(s.balance);
    for(const e of data.edges){
      if(!e.months.includes(s.month)||closed.has(e.a)||closed.has(e.b))continue;
      const access=!!e.access,feeder=feeders.has(e.id),lastMile=access||feeder;
      if(e.mode==='road'&&!access&&!feeder)continue;
      if(!lastMile&&!modes.includes(e.mode))continue;
      // Last-mile: no fare, but driving time counts in the optimizer score and trip duration.
      const cost=lastMile?{low:0,high:0}:amounts(e,s.party);
      const hours=lastMile?e.hours:edgeHours(e);
      const score=lastMile?vot*hours:(cost.low+cost.high)/2/s.party+vot*hours;
      adj[e.a].push({to:e.b,edge:e,score,hours,lastMile,...cost});adj[e.b].push({to:e.a,edge:e,score,hours,lastMile,...cost});
    }
    return {adj,s:{...s,modes}};
  }
  // Binary heap keeps all-stop optimization responsive even on the full destination bank.
  class Heap{constructor(){this.a=[];}push(v){let a=this.a,i=a.length;a.push(v);while(i){let p=(i-1)>>1;if(a[p][0]<=v[0])break;a[i]=a[p];i=p;}a[i]=v;}pop(){const a=this.a,root=a[0],v=a.pop();if(a.length){let i=0;while(2*i+1<a.length){let j=2*i+1;if(j+1<a.length&&a[j+1][0]<a[j][0])j++;if(a[j][0]>=v[0])break;a[i]=a[j];i=j;}a[i]=v;}return root;}}
  function tree(graph,start){
    const dist={},prev={},q=new Heap();dist[start]=0;q.push([0,start]);
    while(q.a.length){const [v,u]=q.pop();if(v!==dist[u])continue;for(const t of graph.adj[u]||[]){const alt=v+t.score;if(dist[t.to]===undefined||alt<dist[t.to]-1e-8){dist[t.to]=alt;prev[t.to]={from:u,...t};q.push([alt,t.to]);}}}
    return {dist,prev};
  }
  function path(t,a,b){
    if(a===b)return {from:a,to:b,steps:[],hours:0,low:0,high:0,score:0};
    if(!finite(t.dist[b]))return null;
    const steps=[];let v=b,guard=0;
    while(v!==a){const p=t.prev[v];if(!p||guard++>1000)return null;steps.unshift({from:p.from,to:v,...p});v=p.from;}
    return {from:a,to:b,steps,hours:steps.reduce((s,e)=>s+e.hours,0),low:steps.reduce((s,e)=>s+e.low,0),high:steps.reduce((s,e)=>s+e.high,0),score:t.dist[b]};
  }
  function isLastMile(s){return !!(s.lastMile||s.edge?.access||s.edge?.mode==='road');}
  function modeTotals(steps){
    const groups=new Map();
    for(const s of steps){
      const last=isLastMile(s),m=last?'lastmile':s.edge.mode;
      const transit=last?s.hours:s.edge.hours,handling=last?0:Math.max(0,s.hours-transit);
      if(!transit&&!handling&&!s.low&&!s.high)continue;
      if(!groups.has(m))groups.set(m,{mode:m,low:0,high:0,transit:0,handling:0,hours:0,segments:0});
      const g=groups.get(m);
      if(last){g.transit+=s.hours;g.hours+=s.hours;}
      else{g.low+=s.low;g.high+=s.high;g.transit+=transit;g.handling+=handling;g.hours+=s.hours;}
      g.segments++;
    }
    return ['flight','train','boat','lastmile'].filter(m=>groups.has(m)).map(m=>groups.get(m));
  }
  function pathOptions(data,a,b,settings){
    const r=[];
    for(const [kind,balance] of [['Balanced',settings.balance],['Cheapest',0],['Quickest',100]]){
      const p=path(tree(build(data,{...settings,balance}),a),a,b);if(!p)continue;
      const key=p.steps.map(s=>s.edge.id).join('/');const old=r.find(x=>x.key===key);
      if(old){old.kinds.push(kind);continue;}r.push({...p,key,kinds:[kind]});
    }
    return r;
  }
  function routeScore(order,m,loop){let score=0;for(let i=1;i<order.length;i++)score+=m[order[i-1]][order[i]];if(loop&&order.length>1)score+=m[order.at(-1)][order[0]];return score;}
  function exact(m,start,end,loop){
    const n=m.length,size=1<<n,dp=new Float64Array(size*n);dp.fill(Infinity);const parent=new Int16Array(size*n);parent.fill(-1);
    for(let i=0;i<n;i++)if((start===null||i===start)&&(end===null||i!==end||n===1))dp[(1<<i)*n+i]=0;
    // A round trip has a fixed start in solve(), so its closing cost is well defined.
    for(let mask=1;mask<size;mask++)for(let j=0;j<n;j++){
      const v=dp[mask*n+j];if(!finite(v))continue;
      for(let k=0;k<n;k++)if(!(mask&(1<<k))&&(end===null||k!==end||(mask|(1<<k))===size-1)){
        const at=(mask|(1<<k))*n+k,x=v+m[j][k];if(x<dp[at]){dp[at]=x;parent[at]=j;}
      }
    }
    let last=-1,best=Infinity;
    for(let j=0;j<n;j++)if(end===null||j===end){const v=dp[(size-1)*n+j]+(loop?m[j][start]:0);if(v<best){best=v;last=j;}}
    if(last<0)return null;const order=[];let mask=size-1;
    while(last>=0){order.unshift(last);const p=parent[mask*n+last];mask^=1<<last;last=p;}return order;
  }
  function heuristic(m,start,end,loop){
    const n=m.length,candidates=Array.from({length:n},(_,i)=>i).filter(i=>i!==end),starts=start===null?(candidates.length<=12?candidates:Array.from({length:12},(_,i)=>candidates[Math.floor(i*candidates.length/12)])):[start];let best=null,bestV=Infinity;
    for(const st of starts){const order=[st],left=new Set(Array.from({length:n},(_,i)=>i).filter(i=>i!==st&&i!==end));
      while(left.size){let k=null,v=Infinity;for(const j of left)if(m[order.at(-1)][j]<v){k=j;v=m[order.at(-1)][j];}if(k===null)break;order.push(k);left.delete(k);}
      if(end!==null&&end!==st)order.push(end);if(order.length!==n)continue;
      let val=routeScore(order,m,loop),improved=true,passes=0;
      while(improved&&passes++<30){improved=false;for(let i=start===null?0:1;i<n-1;i++)for(let j=i+1;j<(end===null?n:n-1);j++){
        // Symmetric graph: reversal changes only the two boundary edges.
        let delta=i>0?m[order[i-1]][order[j]]-m[order[i-1]][order[i]]:0;
        if(j<n-1)delta+=m[order[i]][order[j+1]]-m[order[j]][order[j+1]];
        else if(loop)delta+=m[order[i]][order[0]]-m[order[j]][order[0]];
        if(delta < -1e-6){order.splice(i,j-i+1,...order.slice(i,j+1).reverse());val+=delta;improved=true;}
      }}if(val<bestV){bestV=val;best=order;}}
    return best;
  }
  function solve(data,ids,settings={}){
    ids=[...new Set(ids)];if(ids.length<2)throw Error('Select at least two places to generate a route.');
    const by=Object.fromEntries(data.destinations.map(d=>[d.id,d]));
    if(ids.some(id=>!by[id]))throw Error('A selected destination is missing from this version.');
    const month=settings.month||12,blocked=ids.filter(id=>!allowed(by[id],month));
    if(blocked.length)throw Error('Main attraction out of season: '+blocked.map(id=>by[id].name).join(', ')+'. Change the month or remove these stops.');
    let start=settings.start&&ids.includes(settings.start)?ids.indexOf(settings.start):null;
    let end=settings.end&&ids.includes(settings.end)?ids.indexOf(settings.end):null;
    if(settings.loop){if(start===null)start=0;end=null;}
    if(start!==null&&start===end)throw Error('Choose different start and finish points, or enable round trip.');
    const graph=build(data,settings),trees=ids.map(id=>tree(graph,id));
    const m=ids.map((a,i)=>ids.map(b=>a===b?0:trees[i].dist[b]??Infinity));
    const unavailable=[];for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++)if(!finite(m[i][j]))unavailable.push(by[ids[i]].name+' ↔ '+by[ids[j]].name);
    if(unavailable.length)throw Error('No known flight/train/ferry connection with these modes/month: '+unavailable.slice(0,2).join('; ')+'. Add flights or trains, or choose another month. Road/car travel is not planned.');
    const order=ids.length<=12?exact(m,start,end,!!settings.loop):heuristic(m,start,end,!!settings.loop);
    if(!order)throw Error('No valid order matches those start and finish constraints.');
    const ordered=order.map(i=>ids[i]),pairs=ordered.slice(1).map((id,i)=>[ordered[i],id]);if(settings.loop)pairs.push([ordered.at(-1),ordered[0]]);
    const legs=pairs.map(([a,b])=>path(trees[ids.indexOf(a)],a,b));
    const originalScore=routeScore(ids.map((_,i)=>i),m,!!settings.loop),optimizedScore=routeScore(order,m,!!settings.loop);
    return {order:ordered,legs,method:ids.length<=12?'Exact within this network':'Multi-start + 2-opt heuristic',objective:optimizedScore,originalObjective:originalScore,settings:{...settings},generated:new Date().toISOString()};
  }
  return {valueOfTime,allowed,amounts,edgeHours,build,tree,path,modeTotals,isLastMile,pathOptions,solve,routeScore,exact,heuristic};
})();
if(typeof module!=='undefined')module.exports=TripEngine;
