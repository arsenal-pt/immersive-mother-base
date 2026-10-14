"""Adapt one owned GANI2 body segment to Soldier2 precision; never install game files.

Requires installed fox_engine_mtar_tools_blender utilities. Shared MTAR layouts,
motion-point/event sidecars and every other body segment remain caller-owned inputs.
"""
from pathlib import Path
import hashlib,importlib.util,io,math,struct

def _layout(path):
    data=Path(path).read_bytes()
    units,segments,*_=struct.unpack_from('<IIHBBII',data,16)
    offsets=struct.unpack_from('<'+str(units)+'I',data,36)
    rows=[]
    for i,offset in enumerate(offsets):
        at=16+offset
        name,count,flags,_=struct.unpack_from('<IBBH',data,at)
        for j in range(count):
            _,ms_id,packed,bits=struct.unpack_from('<ihBB',data,at+8+j*8)
            rows.append((i,name,ms_id,packed,flags,bits))
    if len(rows)!=segments:
        raise ValueError('Inconsistent layout segment count')
    return units,segments,rows

def normalize_body(source,player_layout,soldier_layout,output,utility_directory):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve() or output.exists():
        raise ValueError('Output must be a new file')
    units,segments,native=_layout(soldier_layout)
    pu,ps,player=_layout(player_layout)
    if (units,segments)!=(pu,ps) or [x[:4] for x in native]!=[x[:4] for x in player]:
        raise ValueError('Ordered track binding/layout mismatch')
    changed=[i for i in range(segments) if native[i][-1]!=player[i][-1]]
    if len(changed)!=1:
        raise ValueError('Only one known precision difference is supported')
    k=changed[0]
    unit,_,ms_id,packed,_,bits=native[k]
    if ms_id!=3 or packed&15!=3 or bits!=16 or player[k][-1]!=32:
        raise ValueError('Unexpected precision target')
    utilities={}
    for name in ('util_binary_read','util_binary_write'):
        path=Path(utility_directory)/(name+'.py')
        spec=importlib.util.spec_from_file_location(name,path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        utilities[name]=(module,hashlib.sha256(path.read_bytes()).hexdigest())
    reader=utilities['util_binary_read'][0];writer=utilities['util_binary_write'][0]
    original=source.read_bytes()
    frames,params=struct.unpack_from('<II',original)
    at=(8+params*8+units+3)&~3
    flags=original[8+params*8:8+params*8+units]
    if original[at+k*4]!=32:
        raise ValueError('Expected 32-bit per-clip target')
    starts=[at+i*4+int.from_bytes(original[at+i*4+1:at+i*4+4],'little') for i in range(segments)]
    if starts!=sorted(set(starts)) or starts[0]<at+segments*4:
        raise ValueError('Unsupported overlapping or nonordered curve blocks')
    ends=starts[1:]+[len(original)]
    blobs=[original[a:b] for a,b in zip(starts,ends)]
    blob=blobs[k];offset=0;vector,offset=reader.read_vector3(blob,offset,32)
    values=[(0,vector)];accumulated=0
    if not flags[unit]&4:
        while accumulated<frames:
            delta=blob[offset];offset+=1
            if not 1<=delta<=255:raise ValueError('Invalid frame delta')
            accumulated+=delta
            vector,offset=reader.read_vector3(blob,offset,32);values.append((delta,vector))
        if accumulated!=frames:raise ValueError('Unexpected frame-count overshoot')
    if len(blob)-offset>1 or any(blob[offset:]):
        raise ValueError('Unexpected segment trailing data')
    if not all(math.isfinite(v) for _,vec in values for v in vec):
        raise ValueError('Nonfinite curve value')
    stream=io.BytesIO()
    for i,(delta,vector) in enumerate(values):
        if i:stream.write(bytes([delta]))
        writer.write_vector3(stream,vector,16)
    writer.align_buffer(stream,2);encoded=stream.getvalue()
    offset=0;decoded=[]
    for i,(delta,vector) in enumerate(values):
        if i:
            if encoded[offset]!=delta:raise ValueError('Frame delta changed')
            offset+=1
        vector,offset=reader.read_vector3(encoded,offset,16);decoded.append(vector)
    error=max(abs(a-b) for (_,v),d in zip(values,decoded) for a,b in zip(v,d))
    if error>=.01:raise ValueError('Precision loss exceeded component tolerance')
    result=bytearray(original[:starts[0]])
    for i,blob in enumerate(blobs):
        relative=len(result)-(at+i*4)
        if not 0<=relative<1<<24:raise ValueError('Relative curve offset overflow')
        result[at+i*4]=16 if i==k else original[at+i*4]
        result[at+i*4+1:at+i*4+4]=relative.to_bytes(3,'little')
        result.extend(encoded if i==k else blob)
    if result[:at]!=original[:at]:raise ValueError('Mini-header changed')
    for i in range(segments):
        begin=at+i*4+int.from_bytes(result[at+i*4+1:at+i*4+4],'little')
        end=at+(i+1)*4+int.from_bytes(result[at+(i+1)*4+1:at+(i+1)*4+4],'little') if i+1<segments else len(result)
        if result[begin:end]!=(encoded if i==k else blobs[i]):
            raise ValueError('Unexpected curve payload change')
    padding=(-len(result))%16;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(result+bytes(padding))
    return {'segment':k,'unit':unit,'msId':ms_id,'sourceBits':32,'targetBits':16,
            'frameCount':frames,'keyframes':len(values),'maximumComponentError':error,
            'unchangedSegmentPayloads':segments-1,'miniHeaderPreserved':True,
            'differentDefaultFlagSegments':sum(a[4]!=b[4] for a,b in zip(native,player)),
            'perClipFlagsPreserved':True,
            'archiveAlignmentPadding':padding,'nativeCompatibilityInferred':False,
            'utilityHashes':{k:v[1] for k,v in utilities.items()},
            'sourceSha256':hashlib.sha256(original).hexdigest(),
            'candidateSha256':hashlib.sha256(output.read_bytes()).hexdigest()}