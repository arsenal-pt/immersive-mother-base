/** Pure query/state functions shared by the browser and real-catalogue contract tests. */
export const UNKNOWN = 'Unknown';
export function hydrateRows(index) {
  return index.rows.map(row=>({...row,search:typeof row.search==='string'?row.search:row.searchTokens.map(id=>index.searchDictionary[id]).join(' ')}));
}

export const DEFAULT = Object.freeze({q:'', category:'', source:'', character:'', moveset:'', status:'', minFrames:'', maxFrames:'', sort:'name', dir:'asc', size:25, page:1, columns:'', detail:''});
export const SORT_KEYS = ['name','filename','category','source','frames','duration','character','moveset','status','id'];
export const FILTER_KEYS = ['category','source','character','moveset','status'];
export function readState(search='') {
  const params = new URLSearchParams(search), s={...DEFAULT};
  for (const k of Object.keys(s)) if(params.has(k)) s[k]=params.get(k);
  s.size=[25,50,100].includes(Number(s.size))?Number(s.size):25;
  s.page=/^[1-9]\d*$/.test(String(s.page))?Math.min(Number(s.page),100000):1;
  s.sort=SORT_KEYS.includes(s.sort)?s.sort:'name'; s.dir=s.dir==='desc'?'desc':'asc';
  for (const k of ['minFrames','maxFrames']) s[k]=s[k]!==''&&Number.isFinite(Number(s[k]))&&Number(s[k])>=0?String(Number(s[k])):'';
  for (const k of ['q',...FILTER_KEYS,'columns','detail']) s[k]=String(s[k]).slice(0,2000);
  return s;
}
export function writeState(s) {
  const p=new URLSearchParams();
  for(const k of Object.keys(DEFAULT)) if(String(s[k])!==String(DEFAULT[k])) p.set(k,s[k]);
  return p.toString();
}
export function changeState(s,patch) {
  const reset=Object.keys(patch).some(k=>!['page','columns','detail'].includes(k));
  return readState(writeState({...s,...(reset?{page:1,detail:''}:{}),...patch}));
}
export function queryRows(rows,s) {
  const terms=s.q.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  const result=rows.filter(r=>terms.every(t=>r.search.includes(t))&&FILTER_KEYS.every(k=>!s[k]||r[k]===s[k])&&(s.minFrames===''||r.frames!==null&&r.frames>=Number(s.minFrames))&&(s.maxFrames===''||r.frames!==null&&r.frames<=Number(s.maxFrames)));
  const collator=new Intl.Collator('en',{numeric:true,sensitivity:'base'});
  result.sort((a,b)=>{
    const x=a[s.sort],y=b[s.sort],missing=v=>v===null||v===undefined||v===''||v===UNKNOWN;
    if(missing(x)!==missing(y)) return missing(x)?1:-1;
    let cmp=typeof x==='number'&&typeof y==='number'?x-y:collator.compare(String(x??''),String(y??''));
    return (s.dir==='desc'?-cmp:cmp)||collator.compare(a.id,b.id);
  });
  const pages=Math.max(1,Math.ceil(result.length/s.size)), page=Math.min(s.page,pages),start=(page-1)*s.size;
  return {rows:result.slice(start,start+s.size),total:result.length,pages,page,start,end:Math.min(start+s.size,result.length)};
}
export function mediaFor(row,mode) {return mode==='gif'?row.gif:row.still;}
export function formatDuration(value) {return value===null?'Unknown':`${(value/1000).toLocaleString('en',{maximumFractionDigits:3})} s`;}
