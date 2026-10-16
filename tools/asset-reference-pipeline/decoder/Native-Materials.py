"""Read just native FMDL material bindings; native references and originals remain authoritative."""
from pathlib import Path
import hashlib,struct
def read_materials(source):
 b=source if isinstance(source,bytes) else Path(source).read_bytes()
 def u(fmt,off):
  size=struct.calcsize('<'+fmt)
  if off<0 or off+size>len(b):raise ValueError('FMDL metadata read outside input')
  return struct.unpack_from('<'+fmt,b,off)
 if b[:4]!=b'FMDL':raise ValueError('Not FMDL')
 table=u('Q',8)[0];n0,n1,s0,l0,s1,l1=u('6I',32);a={};z={}
 for i in range(n0):
  typ,n,off=u('HHI',table+i*8);a[typ]=(n,s0+off)
 for i in range(n1):
  typ,off,size=u('III',table+n0*8+i*12);z[typ]=(s1+off,size)
 def entries(typ,fmt,stride):
  if typ not in a:return []
  n,off=a[typ];return [u(fmt,off+i*stride) for i in range(n)]
 strings=[]
 for section,length,off in entries(12,'HHI',8):
  start=z[section][0]+off;strings.append(b[start:start+length].decode('utf-8'))
 ph=[v[0] for v in entries(21,'Q',8)];sh=[v[0] for v in entries(22,'Q',8)]
 def string(i):return strings[i] if strings and i<len(strings) else None
 def h(i):return sh[i] if not strings and i<len(sh) else None
 textures=[{'name':string(n),'nameHash':h(n),'path':string(p),'pathHash':ph[p] if not strings and p<len(ph) else None}
  for n,p in entries(6,'HH',4)]
 params=entries(7,'HH',4);vectors=[]
 if 0 in z:
  off,size=z[0]
  if size%16:raise ValueError('Invalid vector section length')
  vectors=[u('4f',off+i*16) for i in range(size//16)]
 mats=[]
 for name,shader,ntex,nvec,firsttex,firstvec in entries(4,'H2xHBBHH4x',16):
  tex=[]
  for pi in range(firsttex,firsttex+ntex):
   n,r=params[pi];t=textures[r]
   tex.append({**t,'samplerName':string(n),'samplerNameHash':h(n),'parameterIndex':pi,'textureIndex':r})
  vv=[]
  for pi in range(firstvec,firstvec+nvec):
   n,r=params[pi];vv.append({'name':string(n),'nameHash':h(n),'vectorIndex':r,'value':vectors[r]})
  mats.append({'name':string(name),'nameHash':h(name),'materialIndex':shader,'textures':tex,
   'firstTextureParameter':firsttex,'firstParameter':firstvec,'parameterCount':nvec,'parameters':vv})
 shaders=[{'name':string(n),'type':string(t),'nameHash':h(n),'typeHash':h(t)} for n,t in entries(8,'HH',4)]
 return {'materialMetadataSchema':2,'sha256':hashlib.sha256(b).hexdigest(),'materials':mats,
  'textures':textures,'shaderRecords':shaders,'materialParameterReferences':params,'materialParameterVectors':vectors,
  'strings':strings,'pathHashes':ph,'stringHashes':sh}
