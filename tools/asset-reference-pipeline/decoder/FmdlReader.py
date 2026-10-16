"""Read-only native FMDL reader for editable static mesh preparation.
Layout checked against the installed FMDL Studio v2 reader. Originals remain authoritative.
"""
from pathlib import Path
import hashlib, math, struct, importlib.util
spec=importlib.util.spec_from_file_location('native_materials',Path(__file__).parent/'Native-Materials.py')
native_materials=importlib.util.module_from_spec(spec);spec.loader.exec_module(native_materials)
def read_fmdl(path):
 b=Path(path).read_bytes()
 def u(fmt,off):
  size=struct.calcsize('<'+fmt)
  if off<0 or off+size>len(b):raise ValueError('FMDL read outside input')
  return struct.unpack_from('<'+fmt,b,off)
 if b[:4]!=b'FMDL':raise ValueError('Not FMDL')
 table=u('Q',8)[0];n0,n1,s0,l0,s1,l1=u('6I',32)
 a={};z={}
 for i in range(n0):
  typ,n,off=u('HHI',table+i*8);a[typ]=(n,s0+off)
 for i in range(n1):
  typ,off,size=u('III',table+n0*8+i*12);z[typ]=(s1+off,size)
 def entries(typ,fmt,stride):
  if typ not in a:return []
  n,off=a[typ];return [u(fmt,off+i*stride) for i in range(n)]
 strings=[]
 for section,length,off in entries(12,'HHI',8):
  start=z[section][0]+off
  strings.append(b[start:start+length].decode('utf-8'))
 pathhash=[v[0] for v in entries(21,'Q',8)]
 strhash=[v[0] for v in entries(22,'Q',8)]
 def string(i):
  return strings[i] if strings and i<len(strings) else None
 def shash(i):
  return strhash[i] if not strings and i<len(strhash) else None
 textures=[{'name':string(n),'nameHash':shash(n),'path':string(p),
   'pathHash':pathhash[p] if not strings and p<len(pathhash) else None} for n,p in entries(6,'HH',4)]
 metadata=native_materials.read_materials(b);materials=metadata['materials']
 offsets=entries(14,'III',16);formats=entries(10,'BBBBI',8);infos=entries(9,'BBBBHH',8)
 vformats=entries(11,'BBH',4);meshinfo=entries(3,'4B4H4xIIQ',48)
 meshes=[];unknown=set()
 for i,m in enumerate(meshinfo):
  nv=m[7];first,nf=m[8:10];info=infos[i];f=formats[info[4]]
  if f[2]!=12:raise ValueError('Unexpected position stride '+repr(f))
  start=z[2][0]+offsets[f[0]][2]+f[4]
  vs=[u('fff',start+j*12) for j in range(nv)]
  if any(not math.isfinite(v) for p in vs for v in p):raise ValueError('Nonfinite positions')
  attrs={};unsupported=[]
  if info[0]>1:
   ff=formats[info[4]+1];base=z[2][0]+offsets[ff[0]][2]+ff[4]
   for typ,data,off in vformats[info[5]:info[5]+info[1]]:
    if typ==0:continue
    fmt={1:'4B',2:'4e',3:'4B',7:'4B',8:'2e',9:'2e',10:'2e',11:'2e',12:'4B',13:'4H',14:'4e'}.get(typ)
    if fmt is None:unknown.add((typ,data));unsupported.append([typ,data,off]);continue
    attrs[str(typ)]=[u(fmt,base+j*ff[2]+off) for j in range(nv)]
  start=z[2][0]+offsets[2][2]+first*2
  inds=u(str(nf)+'H',start)
  if nf%3 or any(j>=nv for j in inds):raise ValueError('Invalid indices')
  meshes.append({'vertices':vs,'faces':[inds[j:j+3] for j in range(0,nf,3)],
   'attributes':attrs,'material':m[4],'boneGroup':m[5],'nativeIndex':m[6],
   'alpha':m[0],'shadow':m[1],'unsupportedAttributes':unsupported})
 groups=[{'name':string(n),'nameHash':shash(n),'hidden':hidden,'parent':parent,'unknown':unk}
  for n,hidden,parent,unk in entries(1,'HHhh',8)]
 groupentries=[list(x) for x in entries(2,'4xHHHH4xH',32)]
 shader=[{'name':string(n),'type':string(t),'nameHash':shash(n),'typeHash':shash(t)} for n,t in entries(8,'HH',4)]
 vectors=entries(7,'HH',4)
 bounds=[[min(v[k] for m in meshes for v in m['vertices']) for k in range(3)],
         [max(v[k] for m in meshes for v in m['vertices']) for k in range(3)]] if any(m['vertices'] for m in meshes) else None
 return {'sha256':hashlib.sha256(b).hexdigest(),'meshes':meshes,'materials':materials,
  'textures':textures,'shaderRecords':shader,'materialParameterReferences':vectors,
  'materialParameterVectors':metadata['materialParameterVectors'],'materialMetadataSchema':2,
  'meshGroups':groups,'meshGroupEntries':groupentries,'strings':strings,
  'pathHashes':pathhash,'stringHashes':strhash,'bounds':bounds,
  'unsupportedAttributes':sorted(unknown),'renderingEquivalent':False}
