"""Focused metadata organization contract checks; no game or image files used."""
from copy import deepcopy
import csv
import importlib.util
import io
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('organizer', Path(__file__).with_name('organize-library.py'))
org = importlib.util.module_from_spec(spec)
spec.loader.exec_module(org)

def entry(i, directory='/Assets/tpp/motion/enet/enetasr'):
    stem = 'motion_' + str(i)
    media = {'path': 'media/animation-previews/existing/' + stem + '.gif', 'sha256': str(i % 10) * 64, 'bytes': 100, 'width': 480, 'height': 614}
    return {'id': 'id-' + str(i), 'title': '<motion | ' + str(i) + '>', 'shortIdentifier': stem, 'group': 'stock-soldier', 'detailPage': org.LIB + '/clips/' + stem + '.md', 'media': {'fullGif': deepcopy(media), 'animatedThumbnail': deepcopy(media), 'stillThumbnail': dict(media, path=media['path'].replace('.gif', '.png'))}, 'locations': {'ganiDirectory': directory, 'ganiVirtualPath': directory + '/' + stem + '.gani' if directory else None, 'archiveFile': 'Soldier_common.mtar'}, 'category': {'label': 'Unchanged category'}, 'tags': ['source-only'], 'description': {'text': 'Action interpretation unverified <test> | exact'}, 'rawFrameCount': 400, 'previewDurationMilliseconds': 13330, 'nativeFrameRate': None, 'evidence': {'perClipVisualReviewPending': True}}

def data(entries):
    catalogue = {'entryCount': len(entries), 'groups': [{'id': 'stock-soldier', 'title': 'Stock source'}], 'entries': entries}
    csv_raw = ('id\n' + '\n'.join(e['id'] for e in entries) + '\n').encode()
    readme = b'# Library\n\n## Browse by section\nold rows\n\n## Metadata columns\nkeep credits, confidence and unknowns\n\n## Credits and scope\noriginal credits\n'
    return catalogue, csv_raw, readme

class Contract(unittest.TestCase):
    def test_all_ids_once_source_immutable_and_legacy_paths_not_outputs(self):
        c, csv_raw, readme = data([entry(i) for i in range(1, 7)])
        before = deepcopy(c)
        outputs, report = org.build(c, csv_raw, readme, 6)
        nav = json.loads(outputs[org.LIB + '/browse/navigation.json'])
        self.assertEqual({e['id'] for e in nav['entries']}, {'id-' + str(i) for i in range(1, 7)})
        self.assertEqual(len(nav['entries']), 6)
        self.assertEqual(c, before)
        self.assertNotIn(org.CATALOGUE, outputs)
        self.assertNotIn(org.CSV, outputs)
        self.assertFalse(any('/clips/' in p or p.startswith('media/') for p in outputs))
        self.assertEqual(report['maxPreviewsPerPage'], 4)
        self.assertFalse(report['mediaReadOrChanged'])
    def test_family_is_exact_directory_and_unknown_is_explicit(self):
        a = entry(1)
        self.assertEqual(org.family(a)[0], a['locations']['ganiDirectory'])
        a['locations']['ganiDirectory'] = None
        self.assertEqual(org.family(a), ('Unrecorded source directory', 'unrecorded'))
    def test_duplicate_or_missing_csv_identity_refused(self):
        c, raw, readme = data([entry(1), entry(2)])
        with self.assertRaises(ValueError): org.build(c, b'id\nid-1\nid-1\n', readme, 2)
        c['entries'][1]['id'] = 'id-1'
        with self.assertRaises(ValueError): org.build(c, raw, readme, 2)
    def test_media_bytes_pack_without_truncating_or_skipping(self):
        es = [entry(i) for i in range(1, 7)]
        for e in es: e['media']['animatedThumbnail']['bytes'] = 6 * 1024 * 1024
        pages = org.pack(es)
        self.assertEqual([len(p) for p in pages], [2, 2, 2])
        es[0]['media']['animatedThumbnail']['bytes'] = 20 * 1024 * 1024
        pages = org.pack(es)
        self.assertEqual(len(pages[0]), 1)
        self.assertEqual(sum(len(p) for p in pages), 6)
    def test_no_gif_loaded_in_still_mode_and_html_escaped(self):
        c, raw, readme = data([entry(1)])
        outputs, report = org.build(c, raw, readme, 1)
        still = next(v.decode() for p, v in outputs.items() if p.endswith('-stills.md'))
        self.assertIn('.png"', still)
        self.assertNotIn('.gif"', still)
        self.assertNotIn('<motion', still)
        self.assertIn('&lt;test&gt;', still)
        self.assertIn('native rate unknown', still)
    def test_selected_mode_uses_own_aspect_and_rejects_bad_dimensions(self):
        c, raw, readme = data([entry(1)])
        c['entries'][0]['media']['stillThumbnail'].update(width=200, height=400)
        outputs, report = org.build(c, raw, readme, 1)
        still = next(v.decode() for p, v in outputs.items() if p.endswith('-stills.md'))
        animated = next(v.decode() for p, v in outputs.items() if '/tables/' in p and not p.endswith('-stills.md'))
        self.assertIn('height="320"', still)
        self.assertIn('height="205"', animated)
        for name in ('animatedThumbnail', 'stillThumbnail'):
            for bad in (0, -1, True, None, float('nan'), float('inf')):
                broken = deepcopy(c)
                broken['entries'][0]['media'][name]['width'] = bad
                with self.assertRaises(ValueError): org.build(broken, raw, readme, 1)
    def test_path_traversal_and_baseline_change_refused(self):
        for bad in ('/absolute', '../escape', 'media/../escape', 'C:/raw', 'media\\raw'):
            with self.assertRaises(ValueError): org.safe_path(bad)
        c, raw, readme = data([entry(1)])
        with self.assertRaises(ValueError): org.build(c, raw, readme, 2)
        c['entries'][0]['media']['fullGif']['path'] = '../private.gif'
        with self.assertRaises(ValueError): org.build(c, raw, readme, 1)
    def test_deterministic_output_and_zero_image_indexes(self):
        c, raw, readme = data([entry(2), entry(1)])
        a = org.build(c, raw, readme, 2)[0]
        b = org.build(c, raw, readme, 2)[0]
        self.assertEqual(a, b)
        for p, contents in a.items():
            if p == org.README or '/browse/' in p and p.endswith('.md'):
                self.assertNotIn('<img', contents.decode())
                self.assertNotIn('![', contents.decode())
        self.assertIn('original credits', a[org.README].decode())

if __name__ == '__main__':
    unittest.main()
