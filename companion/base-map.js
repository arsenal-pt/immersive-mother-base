/* Mother Base native map: browser controls never issue game commands.
   Geometry comes from the user's NAV2/FOX2 files; live completed grades gate every part. */
(function(root,factory){
 const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;
 else root.NLabBaseMap=api;
})(typeof window!=="undefined"?window:this,function(){
 "use strict";
 const departments=["Command","Combat","R&D","Support","Medical","Intel","Base Development"];
 const palette=["#64d9c3","#dfbb72","#8baeff","#9fc97e","#e9a4ba","#b6a0ed","#d78f65"];
 const colors={ROAMING:"#78d3b2",MUSTER:"#ffcf78",GATHERING:"#c5a3ff",FACILITY_QUEUE:"#76bcff",FACILITY_USE:"#ff9fab",DUTY:"#a5b8ff"};
 const esc=v=>String(v??"").replace(/[&<>"]/g,x=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]));
 const valid=p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.z);
 function transform(m,p){return {x:m[0]*p.x+m[2]*p.z+m[4],z:m[1]*p.x+m[3]*p.z+m[5]};}
 function built(state,c,p){
  const cluster=(state.clusters||[]).find(x=>x.cluster0===c);
  return cluster&&Number.isInteger(cluster.grade)&&cluster.grade>p;
 }
 function assemble(catalog,state){
  if(!state||!state.inMotherBase)return {parts:[],platforms:[],error:"Mother Base is not currently loaded."};
  if(state.loading||state.activating)return {parts:[],platforms:[],error:"Mother Base is loading. Waiting for its live layout."};
  if(!state.complete)return {parts:[],platforms:[],error:"Waiting for a complete native layout observation."};
  const layout=catalog?.layouts?.[String(state.layoutCode)];
  if(!layout)return {parts:[],platforms:[],error:"Layout "+state.layoutCode+" has no decoded native geometry yet."};
  const command=(state.clusters||[]).find(c=>c.cluster0===0);
  if(command?.grade!==layout.commandGrade)return {parts:[],platforms:[],error:"Live Command grade and native layout disagree. Waiting for a stable construction snapshot."};
  const centers=new Map();
  for(const c of state.clusters||[])for(const p of c.platforms||[])if(valid(p))centers.set(c.cluster0+"-"+p.plant0,p);
  const platforms=layout.parts.filter(p=>p.kind==="platform"&&built(state,p.cluster0,p.plant0));
  if(platforms.some(p=>!centers.has(p.cluster0+"-"+p.plant0)))
   return {parts:[],platforms:[],error:"Waiting for the game's built-platform centres."};
  // A modified layout can reuse a stock code. Do not silently draw the stock layout over it.
  if(platforms.some(p=>{const q=centers.get(p.cluster0+"-"+p.plant0);return Math.hypot(q.x-p.matrix[4],q.z-p.matrix[5])>.25;}))
   return {parts:[],platforms:[],error:"Live platform positions differ from the decoded layout. Map geometry needs a new survey."};
  const parts=layout.parts.filter(p=>(p.requires||[]).every(([c,n])=>built(state,c,n))&&
   (p.excludes||[]).every(([c,n])=>!built(state,c,n)));
  const links=(layout.links||[]).filter(p=>(p.requires||[]).every(([c,n])=>built(state,c,n)));
  return {parts,platforms,links,error:null};
 }
 class Viewport{
  constructor(width=600,height=430){this.width=width;this.height=height;this.x=0;this.z=0;this.scale=1;this.yaw=0;}
  project(p){
   const dx=p.x-this.x,dz=p.z-this.z,c=Math.cos(this.yaw),s=Math.sin(this.yaw);
   return [this.width/2+this.scale*(-c*dx+s*dz),this.height/2-this.scale*(s*dx+c*dz)];
  }
  unproject(q){
   const sx=(q[0]-this.width/2)/this.scale,sy=-(q[1]-this.height/2)/this.scale,c=Math.cos(this.yaw),s=Math.sin(this.yaw);
   return {x:this.x-c*sx+s*sy,z:this.z+s*sx+c*sy};
  }
  pan(dx,dy){
   const a=this.unproject([this.width/2-dx,this.height/2-dy]);this.x=a.x;this.z=a.z;
  }
  zoom(factor,q=[this.width/2,this.height/2]){
   const a=this.unproject(q);this.scale=Math.max(.025,Math.min(30,this.scale*factor));
   const b=this.unproject(q);this.x+=a.x-b.x;this.z+=a.z-b.z;
  }
  fit(points,padding=45){
   if(!points.length)return;
   const c=Math.cos(this.yaw),s=Math.sin(this.yaw);
   const xs=points.map(p=>-c*p.x+s*p.z),ys=points.map(p=>-s*p.x-c*p.z);
   const xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys);
   this.scale=Math.max(.025,Math.min(30,(this.width-padding*2)/Math.max(1,xmax-xmin),(this.height-padding*2)/Math.max(1,ymax-ymin)));
   const a=(xmin+xmax)/2,b=(ymin+ymax)/2;this.x=-c*a-s*b;this.z=s*a-c*b;
  }
  matrix(m){
   const c=Math.cos(this.yaw),s=Math.sin(this.yaw),k=this.scale,q=this.project({x:m[4],z:m[5]});
   return [-c*k*m[0]+s*k*m[1],-s*k*m[0]-c*k*m[1],-c*k*m[2]+s*k*m[3],-s*k*m[2]-c*k*m[3],q[0],q[1]];
  }
 }
 function extent(catalog,parts){
  const points=[];
  for(const p of parts){
   const b=catalog.meshes[p.mesh]?.bounds;
   if(b)for(const x of [b[0],b[2]])for(const z of [b[1],b[3]])points.push(transform(p.matrix,{x,z}));
  }
  return points;
 }
 function heading(view,player){
  const yaw=Number(player.yaw||0)*Math.PI/180;
  const q=view.project(player),tip=view.project({x:player.x+Math.sin(yaw),z:player.z+Math.cos(yaw)});
  return (Math.atan2(tip[1]-q[1],tip[0]-q[0])*180/Math.PI+270)%360-180;
 }
 class Dashboard{
  constructor(svg,caption,selection){
   this.svg=svg;this.caption=caption;this.selection=selection;this.view=new Viewport();
   this.catalog=null;this.geometryUnavailable=false;this.status=null;this.layout=null;this.scene=null;this.signature=null;this.follow=false;this.camera=false;
   this.gesture=new Map();this.dragDistance=0;this.sceneMarkup="";this.lastSample=null;this.changedAt=0;
   this.defaultFitted=false;
   svg.innerHTML='<defs data-map-defs></defs><g data-map-grid></g><g data-map-native></g><g data-map-overlay></g>';
   this.defs=svg.querySelector("[data-map-defs]");this.gridLayer=svg.querySelector("[data-map-grid]");
   this.nativeLayer=svg.querySelector("[data-map-native]");this.overlay=svg.querySelector("[data-map-overlay]");
   this.measure();this.connectControls();
   fetch("/base-map-geometry").then(r=>{if(!r.ok)throw Error("Native geometry unavailable");return r.json();})
    .then(c=>{this.catalog=c;
     this.defs.innerHTML=Object.entries(c.meshes).map(([id,m])=>'<g id="native_'+esc(id)+'">'+m.bands.map(b=>'<path d="'+b.d+'" fill-opacity="'+(b.height>1?.65:1)+'"/>').join("")+'</g>').join("");
     this.update(this.status,this.layout);})
    .catch(e=>{this.geometryUnavailable=true;this.catalog={source:"observed coordinates only; deck geometry unavailable",meshes:{},layouts:{}};this.update(this.status,this.layout);});
   new ResizeObserver(()=>{this.measure();this.render();}).observe(svg);
  }
  connectControls(){
   const el=id=>document.getElementById(id);
   this.svg.style.touchAction="none";
   const stopFollow=()=>{this.follow=false;el("mapfollow").setAttribute("aria-pressed","false");};
   const change=fn=>{stopFollow();fn();this.render();};
   el("mapzoomIn").onclick=()=>change(()=>this.view.zoom(1.6));
   el("mapzoomOut").onclick=()=>change(()=>this.view.zoom(1/1.6));
   el("mapfit").onclick=()=>change(()=>this.fitBase());
   el("mapsnake").onclick=()=>change(()=>this.focusSnake());
   el("mapactivity").onclick=()=>change(()=>this.focusActivity());
   el("mapfollow").onclick=()=>{
    this.follow=!this.follow;el("mapfollow").setAttribute("aria-pressed",String(this.follow));
    if(this.follow)this.focusSnake();this.render();
   };
   el("maporientation").onclick=()=>{
    this.camera=!this.camera;el("maporientation").textContent=this.camera?"Camera up":"North up";
    this.view.yaw=this.camera?Number(this.player()?.cameraYaw||0)*Math.PI/180:0;this.render();
   };
   this.svg.addEventListener("wheel",e=>{
    e.preventDefault();change(()=>this.view.zoom(Math.exp(-Math.max(-200,Math.min(200,e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?this.view.height:1)))*.006),this.point(e)));
   },{passive:false});
   this.svg.addEventListener("keydown",e=>{
    const actions={ArrowLeft:()=>this.view.pan(50,0),ArrowRight:()=>this.view.pan(-50,0),
     ArrowUp:()=>this.view.pan(0,50),ArrowDown:()=>this.view.pan(0,-50),
     "+":()=>this.view.zoom(1.6),"=":()=>this.view.zoom(1.6),"-":()=>this.view.zoom(1/1.6),
     Home:()=>this.fitBase()};
    if(actions[e.key]){e.preventDefault();change(actions[e.key]);}
   });
   this.svg.addEventListener("pointerdown",e=>{
    if(e.button!==0&&e.pointerType==="mouse")return;
    stopFollow();this.svg.focus({preventScroll:true});this.svg.setPointerCapture(e.pointerId);
    if(!this.gesture.size)this.dragDistance=0;
    this.gesture.set(e.pointerId,this.point(e));this.svg.classList.add("dragging");
   });
   this.svg.addEventListener("pointermove",e=>{
    if(!this.gesture.has(e.pointerId))return;
    const before=[...this.gesture.values()],old=this.gesture.get(e.pointerId),point=this.point(e);
    this.dragDistance+=Math.hypot(point[0]-old[0],point[1]-old[1]);
    this.gesture.set(e.pointerId,point);const after=[...this.gesture.values()];
    if(before.length===2){
     const mid=a=>[(a[0][0]+a[1][0])/2,(a[0][1]+a[1][1])/2],a=mid(before),b=mid(after);
     const d=a=>Math.hypot(a[1][0]-a[0][0],a[1][1]-a[0][1]);
     this.view.pan(b[0]-a[0],b[1]-a[1]);if(d(before)>2)this.view.zoom(d(after)/d(before),b);
    }else this.view.pan(point[0]-old[0],point[1]-old[1]);
    this.render();
   });
   const end=e=>{
    if(!this.gesture.has(e.pointerId))return;
    if(e.type==="pointerup"&&this.dragDistance<4)this.pick(this.point(e));
    this.gesture.delete(e.pointerId);if(!this.gesture.size)this.svg.classList.remove("dragging");
   };
   this.svg.addEventListener("pointerup",end);this.svg.addEventListener("pointercancel",end);
   this.svg.addEventListener("lostpointercapture",end);
  }
  point(e){
   const r=this.svg.getBoundingClientRect();return [e.clientX-r.left,e.clientY-r.top];
  }
  measure(){
   const r=this.svg.getBoundingClientRect();
   this.view.width=Math.max(1,r.width);this.view.height=Math.max(1,r.height);
   this.svg.setAttribute("viewBox","0 0 "+this.view.width+" "+this.view.height);
  }
  update(status,layout){
   if(!status)return;this.status=status;this.layout=layout;
   const live=status.baseMap;
   if(live?.realTime!==this.lastSample){this.lastSample=live?.realTime;this.changedAt=Date.now();}
   if(!this.catalog){this.caption.textContent="Loading native Mother Base geometry…";return;}
   this.scene=this.geometryUnavailable?{parts:[],platforms:[],links:[],error:"Deck geometry unavailable · observed coordinates only"}:assemble(this.catalog,live);
   const sig=JSON.stringify([live?.layoutCode,(live?.clusters||[]).map(c=>[c.grade,c.platforms]),live?.loading,live?.activating,this.scene.error]);
   if(sig!==this.signature){this.signature=sig;this.compileScene();}
   if(!this.defaultFitted&&(this.scene.parts.length||this.geometryUnavailable&&this.actors().length)){this.fitBase();this.defaultFitted=true;}
   if(this.camera)this.view.yaw=Number(this.player()?.cameraYaw||0)*Math.PI/180;
   if(this.follow&&valid(this.player())){this.view.x=this.player().x;this.view.z=this.player().z;}
   this.render();
  }
  player(){
   const s=this.status,l=s?.baseMap;
   return Math.abs((s?.realTime||0)-(l?.realTime||0))<10&&valid(s?.player)?s.player:l?.player;
  }
  actors(){
   const s=this.status,l=s?.baseMap;
   if(!l?.inMotherBase||l.loading||l.activating||Math.abs((s?.realTime||0)-(l?.realTime||0))>=10)return [];
   return (s.actors||[]).filter(valid);
  }
  compileScene(){
   this.sceneMarkup=(this.scene?.parts||[]).map(p=>{
    const color=palette[p.cluster0]||"#809ba9";
    return '<use data-native-part="'+esc(p.id)+'" data-kind="'+p.kind+'" data-mesh="'+esc(p.mesh)+'" href="#native_'+esc(p.mesh)+'" fill="'+color+'" fill-opacity="'+(p.kind==="platform"?.52:p.kind==="division"?.72:.55)+'" transform="matrix('+p.matrix.join(" ")+')"/>';
   }).join("");
   this.nativeLayer.innerHTML=this.sceneMarkup;
  }
  fitBase(){const points=this.scene?.parts.length?extent(this.catalog,this.scene.parts):[...this.actors(),this.player()].filter(valid);if(points.length)this.view.fit(points,Math.min(28,this.view.width*.08));}
  focusSnake(){
   const p=this.player();if(!valid(p))return;this.view.x=p.x;this.view.z=p.z;this.view.scale=Math.min(this.view.width,this.view.height)/115;
  }
  focusActivity(){
   const a=this.actors(),s=this.status;let points=[];
   if(Array.isArray(s.group?.ids))points=a.filter(x=>s.group.ids.includes(x.id)).flatMap(x=>valid(x.target)?[x.target]:[]);
   if(!points.length){const f=a.find(x=>x.facility)?.facility;
    if(f&&this.layout?.facilities?.[f])points=[...(this.layout.facilities[f].queue||[]),...(this.layout.facilities[f].uses||[])].filter(valid);}
   if(points.length){const xs=points.map(x=>x.x),zs=points.map(x=>x.z);
    points.push({x:Math.min(...xs)-12,z:Math.min(...zs)-12},{x:Math.max(...xs)+12,z:Math.max(...zs)+12});
    this.view.fit(points,Math.min(28,this.view.width*.08));
   }else this.focusSnake();
  }
  pick(point){
   let nearest=null,dist=14;
   for(const x of this.actors()){const p=this.view.project(x),d=Math.hypot(p[0]-point[0],p[1]-point[1]);if(d<dist){nearest=x;dist=d;}}
   this.selection.textContent=nearest?nearest.label+" · "+(nearest.dutyLabel||nearest.state)+" · height "+Math.round(nearest.y||0)+" m":"";
  }
  render(){
   if(!this.status||!this.catalog||!this.scene)return;
   const v=this.view,s=this.status,live=s.baseMap,actors=this.actors(),parts=[],w=v.width,h=v.height;
   const project=p=>v.project(p),num=n=>Number(n).toFixed(2);
   const line=(a,b,extra)=>'<path d="M'+a.map(num).join(" ")+'L'+b.map(num).join(" ")+'" '+extra+'/>';
   const label=(p,text,color="#d3e3e8",size=12,align="start")=>'<text x="'+num(p[0])+'" y="'+num(p[1])+'" fill="'+color+'" font-size="'+size+'" text-anchor="'+align+'" paint-order="stroke" stroke="#0d1a22" stroke-width="3">'+esc(text)+'</text>';
   const stale=Number(live?.feedAgeSeconds)>10||Date.now()-this.changedAt>5500||(live?.capturedUnix&&Date.now()/1000-live.capturedUnix>10);
   const builtCount=this.scene.platforms.length;
   this.caption.textContent=this.scene.error||builtCount+" built platforms · layout "+live.layoutCode+" · "+actors.length+" observed staff"+(stale?" · last observed layout (feed paused)":" · live construction");
   this.svg.dataset.centerX=String(v.x);this.svg.dataset.centerZ=String(v.z);this.svg.dataset.scale=String(v.scale);
   this.svg.dataset.yaw=String(v.yaw);this.svg.dataset.platformCount=String(builtCount);
   this.svg.dataset.layoutCode=String(live?.layoutCode??"");this.svg.dataset.liveTime=String(live?.realTime??"");
   this.svg.dataset.geometrySource=this.catalog.source;
   // Ocean grid in metres, with spacing suited to the current zoom.
   const corners=[[0,0],[w,0],[0,h],[w,h]].map(p=>v.unproject(p));
   const xs=corners.map(p=>p.x),zs=corners.map(p=>p.z),x0=Math.min(...xs),x1=Math.max(...xs),z0=Math.min(...zs),z1=Math.max(...zs);
   const ideal=75/v.scale,power=10**Math.floor(Math.log10(ideal)),step=[1,2,5,10].map(x=>x*power).find(x=>x>=ideal)||10*power;
   for(let x=Math.ceil(x0/step)*step;x<x1;x+=step)parts.push(line(project({x,z:z0}),project({x,z:z1}),'stroke="#1b3543" stroke-width="1"'));
   for(let z=Math.ceil(z0/step)*step;z<z1;z+=step)parts.push(line(project({x:x0,z}),project({x:x1,z}),'stroke="#1b3543" stroke-width="1"'));
   for(const l of this.scene.links||[])parts.push(line(project({x:l.a[0],z:l.a[1]}),project({x:l.b[0],z:l.b[1]}),'stroke="#477b89" stroke-width="'+Math.max(.7,Math.min(3,v.scale*2))+'"'));
   this.gridLayer.innerHTML=parts.join("");parts.length=0;
   this.nativeLayer.setAttribute("transform","matrix("+v.matrix([1,0,0,1,0,0]).join(" ")+")");
   for(const p of this.scene.platforms){
    const q=project({x:p.matrix[4],z:p.matrix[5]});
    if(q[0]<-90||q[0]>w+90||q[1]<-60||q[1]>h+60)continue;
    const align=q[0]>w*.65?"end":"start",offset=align==="end"?-8:8;
    if(v.scale>.55)parts.push(label([q[0]+offset,q[1]-12],departments[p.cluster0]+" "+(p.plant0+1),palette[p.cluster0],11,align));
    else if(p.plant0===0)parts.push(label([q[0]+offset,q[1]-8],departments[p.cluster0],palette[p.cluster0],10,align));
   }
   if(v.scale>.7){
    const anchor=s.muster?.commander;
    if(valid(anchor)){const q=project(anchor);parts.push('<path d="M'+q[0]+' '+(q[1]-5)+'l5 5 -5 5 -5 -5z" fill="none" stroke="#bac9d0"/>');}
    for(const p of s.muster?.slots||[]){const q=project(p);parts.push('<rect x="'+(q[0]-3)+'" y="'+(q[1]-3)+'" width="6" height="6" fill="none" stroke="#a08553"/>');}
    for(const [key,f]of Object.entries(this.layout?.facilities||{})){
     if(valid(f.fixtureOrigin)){const q=project(f.fixtureOrigin);parts.push('<rect x="'+(q[0]-5)+'" y="'+(q[1]-6)+'" width="10" height="12" fill="#448799"/>');}
     if(actors.some(x=>x.facility===key)){
      for(const p of f.queue||[]){const q=project(p);parts.push('<rect x="'+(q[0]-4)+'" y="'+(q[1]-4)+'" width="8" height="8" fill="none" stroke="#76bcff"/>');}
      if(valid(f.queue?.[0]))parts.push(label(project(f.queue[0]),key,"#92c9d6",11));
     }
    }
   }
   for(const [i,x]of actors.entries()){
    const q=project(x),color=colors[x.state]||"#d2dae0";
    if(valid(x.target)&&v.scale>.3)parts.push(line(q,project(x.target),'stroke="'+color+'" opacity=".45" stroke-dasharray="4 4"'));
    if(q[0]<-15||q[0]>w+15||q[1]<-15||q[1]>h+15)continue;
    const badge=String(x.index??i+1).padStart(2,"0");
    parts.push('<g data-map-person="'+esc(x.label)+'"><circle cx="'+q[0]+'" cy="'+q[1]+'" r="'+(v.scale>.7?8:2.7)+'" fill="'+color+'"><title>'+esc(x.label)+" · "+esc(x.state)+'</title></circle>');
    if(v.scale>.7)parts.push('<text x="'+q[0]+'" y="'+(q[1]+3.5)+'" fill="#122630" font-size="10" font-weight="700" text-anchor="middle">'+esc(badge)+'</text>');
    if(v.scale>1&&x.y>2)parts.push(label([q[0]+11,q[1]-7],Math.round(x.y)+"m","#becbd2",10));
    parts.push("</g>");
   }
   const player=this.player();
   if(live?.inMotherBase&&valid(player)&&!live.loading&&!live.activating){
    const q=project(player);
    parts.push('<path data-live-player="true" data-world-x="'+player.x+'" data-world-z="'+player.z+'" transform="translate('+q.join(" ")+') rotate('+heading(v,player)+')" d="M0 -11L7 7L0 3L-7 7Z" fill="#eaf8fb" stroke="#12232c" stroke-width="1.5"/>');
    if(v.scale>.5)parts.push(label([q[0]+12,q[1]+5],"Snake"));
   }
   // Heading is a world compass; the camera option rotates it with the map.
   parts.push('<g transform="translate('+(w-35)+' 35) rotate('+(v.yaw*180/Math.PI)+')"><path d="M0 -15L-5 5L0 1L5 5Z" fill="#b5d0dc"/></g>'+label([w-39,14],"N","#b5d0dc",11));
   const barMetres=[1,2,5,10,20,50,100,200,500,1000,2000].find(n=>n*v.scale>=50)||2000;
   parts.push('<path d="M22 '+(h-34)+'v6h'+(barMetres*v.scale)+'v-6" fill="none" stroke="#b5ceda"/>'+label([22,h-10],barMetres+" m","#b5ceda",11));
   if(this.scene.error&&!this.geometryUnavailable)parts.push(label([25,h/2],"Waiting for live map","#b5ceda",15));
   this.overlay.innerHTML=parts.join("");
  }
 }
 return {Viewport,assemble,extent,transform,heading,Dashboard};
});
