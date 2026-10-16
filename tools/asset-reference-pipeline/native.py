"""Reuse the authored static reader and native LOD audit; see dependency-provenance."""
import importlib.util
import json
from pathlib import Path
import struct
import zlib
from runtime import ManualReview, digest


def inspect_model(path, output, prepared=None):
    spec = importlib.util.spec_from_file_location('retained_fmdl_reader', Path(__file__).parent / 'decoder/FmdlReader.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    data = reader.read_fmdl(path)
    if data['unsupportedAttributes']:
        raise ManualReview('Unsupported native vertex attributes')
    if any(set(m['attributes']) - {'2', '8', '9', '10', '11', '12', '13', '14'} for m in data['meshes']):
        raise ManualReview('Only supported static-prop vertex layouts are enabled; character assembly is parked')
    if any('8' not in m['attributes'] or '2' not in m['attributes'] for m in data['meshes']):
        raise ManualReview('Require explicit UV0 and native normals')
    if any(g['hidden'] for g in data['meshGroups']):
        raise ManualReview('Hidden native groups need an explicitly reviewed assembly recipe')
    b = Path(path).read_bytes()
    table = struct.unpack_from('<Q', b, 8)[0]
    n0, n1, s0, l0, s1, l1 = struct.unpack_from('<6I', b, 32)
    a, z = {}, {}
    for i in range(n0):
        typ, n, off = struct.unpack_from('<HHI', b, table + i * 8)
        a[typ] = (n, s0 + off)
    for i in range(n1):
        typ, off, size = struct.unpack_from('<III', b, table + n0 * 8 + i * 12)
        z[typ] = (s1 + off, size)

    def entries(typ, fmt, stride):
        if typ not in a:
            return []
        n, off = a[typ]
        return [struct.unpack_from('<' + fmt, b, off + i * stride) for i in range(n)]

    offsets = entries(14, 'III', 16)
    face_base, face_bytes = z[2][0] + offsets[2][2], offsets[2][1]
    li, fi, mi = entries(16, 'Ifff', 16), entries(17, 'II', 8), entries(3, '4B4H4xIIQ', 48)
    if len(li) != 1 or not 1 <= li[0][0] <= 16:
        raise ManualReview('Missing/unsupported native LOD table')
    faces, quality = [], []
    for level in range(li[0][0]):
        level_faces = []
        for index, m in enumerate(mi):
            first, count, face_info = m[8:11]
            lo, n = fi[face_info + level]
            if lo % 3 or n % 3 or (first + lo + n) * 2 > face_bytes:
                raise ValueError('Invalid native LOD index-buffer range')
            indices = struct.unpack_from('<' + str(n) + 'H', b, face_base + (first + lo) * 2)
            if any(v >= m[7] for v in indices):
                raise ValueError('Native LOD vertex index outside mesh')
            triangles = [list(indices[j:j+3]) for j in range(0, n, 3)]
            if level == 0 and triangles != [list(f) for f in data['meshes'][index]['faces']]:
                raise ValueError('Native LOD0 differs from reused reader')
            faces.append({'meshIndex': index, 'level': level, 'faces': triangles})
            level_faces.append(triangles)
        quality.append({'nativeLod': level, 'triangles': sum(map(len, level_faces)),
                        'indicesSha256': digest(level_faces)})
    if prepared:
        old = json.loads(zlib.decompress(Path(prepared['cache']['file']).read_bytes()))
        old_lods = json.loads(zlib.decompress(Path(prepared['lodCache']['file']).read_bytes()))
        if digest(old) != digest(data) or digest(old_lods) != digest(faces):
            raise ManualReview('Prepared caches differ from direct native inspection')
    output = Path(output)
    (output / 'model.json.z').write_bytes(zlib.compress(json.dumps(data, separators=(',', ':')).encode(), 6))
    (output / 'lods.json.z').write_bytes(zlib.compress(json.dumps(faces, separators=(',', ':')).encode(), 6))
    return data, quality


def bind_materials(data, recipe, textures):
    """Recipes resolve hash-only sampler names; check every native identity."""
    materials = []
    for index, material in enumerate(data['materials']):
        choices = [t for t in recipe['baseTextures'] if t['materialIndex'] == index]
        if len(choices) != 1:
            raise ManualReview('One reviewed base binding per material is required')
        binding = choices[0]
        if binding['samplerName'] not in ('Base_Tex_SRGB', 'Base_Tex_LIN'):
            raise ManualReview('Only explicit base-color reference bindings are supported')
        if not str(binding['nativePathHash']).isdigit():
            raise ManualReview('String-path material bindings need a reviewed adapter; hash-only slice supported')
        native = [t for t in material['textures'] if t.get('pathHash') is not None and
                  str(t.get('pathHash') if t.get('pathHash') is not None else t.get('path')) == str(binding['nativePathHash'])
                  and (t.get('samplerName') == binding['samplerName'] or
                       (t.get('samplerNameHash') is not None and binding.get('samplerNameHash') is not None
                        and str(t['samplerNameHash']) == str(binding['samplerNameHash'])))]
        if len(native) != 1:
            raise ManualReview('Recipe base binding does not match original native material')
        tex = textures[str(index)]
        materials.append({**material, 'textures': [{**native[0], 'samplerName': binding['samplerName'],
                          'nativeHash': str(binding['nativePathHash']),
                          'ddsChoices': [{'dds': tex['file'], 'sha256': tex['sha256']}]}]})
    return {'nativeSha256': data['sha256'], 'nativeFmdlPath': recipe['model']['virtualPath'],
            'materials': materials, 'shaderRecords': data['shaderRecords']}
