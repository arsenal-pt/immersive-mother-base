// Offline DOM fixture: actual map module and controls, no network/game access.
const assert=require("node:assert/strict"),path=require("node:path"),fs=require("node:fs"),vm=require("node:vm");
const root=path.resolve(__dirname,"../companion"),controls=new Map();
const element=()=>({innerHTML:"",textContent:"",style:{},dataset:{},attributes:{},
 setAttribute(k,v){this.attributes[k]=v},addEventListener(){},focus(){},setPointerCapture(){},
 getBoundingClientRect(){return {width:600,height:430,left:0,top:0}},classList:{add(){},remove(){}}});
global.document={getElementById(id){if(!controls.has(id))controls.set(id,element());return controls.get(id)}};
global.ResizeObserver=class {observe(){}};
global.fetch=async()=>({ok:false});
const api=require(path.join(root,"base-map.js"));
const svg=element(),layers=new Map();
svg.querySelector=q=>{if(!layers.has(q))layers.set(q,element());return layers.get(q)};
const caption=element(),selection=element(),map=new api.Dashboard(svg,caption,selection);
const status={realTime:100,actors:[{id:1,index:1,label:"Offline fixture",state:"ROAMING",x:10,y:0,z:20}],
 player:{x:0,z:0,y:0},baseMap:{realTime:100,inMotherBase:true,complete:true,feedAgeSeconds:0}};
map.update(status,null);
setImmediate(()=>{
 map.update(status,null);
 assert.equal(map.geometryUnavailable,true);
 assert.match(caption.textContent,/Deck geometry unavailable/);
 assert.equal(svg.dataset.platformCount,"0");
 assert.equal(layers.get("[data-map-native]").innerHTML,"");
 assert.match(layers.get("[data-map-overlay]").innerHTML,/Offline fixture/);
 const old=map.view.scale;
 controls.get("mapzoomIn").onclick();
 assert.ok(map.view.scale>old);
 const before=map.view.x;
 map.view.pan(20,0);map.render();
 assert.notEqual(map.view.x,before);
 map.pick(map.view.project(status.actors[0]));
 assert.match(selection.textContent,/Offline fixture/);
 const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
 const inline=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
 assert.equal(inline.length,1);
 new vm.Script(inline[0][1]);
 assert.match(html,/Location unverified/);
 assert.doesNotMatch(html,/IHStaff|ihstaff|ih-staff|inspection/);
 console.log(JSON.stringify({passed:true,checks:9,scope:"actual map fallback, pan, zoom, selection and dashboard JS syntax",nativeGameplay:false}));
});
