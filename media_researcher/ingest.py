#!/usr/bin/env python3
"""Hand a consolidated research package to the existing editor (edl_v3.py / render3.py) without changing them.
Usage: ingest.py MANIFEST.json PROJECT_ASSET_DIR   -> copies usable assets to PROJECT_ASSET_DIR/research/ and writes research_overrides.json
research_overrides.json maps narration segment ids -> ranked asset candidates (path, credit text, licence, suggested pops).
In edl_v3.py-style code: for each override, register IMG[key]=(path, crop, fit) and call img(t0, key, pops, credit=...)."""
import sys, os, json, shutil
man = json.load(open(sys.argv[1])); dest = sys.argv[2]; root = os.path.dirname(os.path.abspath(sys.argv[1]))
os.makedirs(f'{dest}/research', exist_ok=True); by_seg = {}; copied = 0
for a in man['assets']:
    if not a.get('filename') or a['verification_status'].startswith('rejected'): continue
    src = os.path.join(root, a['filename']); tgt = f"{dest}/research/{os.path.basename(a['filename'])}"
    if os.path.exists(src): shutil.copy(src, tgt); copied += 1
    credit = ' · '.join(x for x in [a.get('source_name'), a.get('source_author'), a.get('publication_date')] if x)
    cand = dict(asset_id=a['asset_id'], path=tgt, type=a['asset_type'], credit=credit or a.get('original_url'), url=a.get('original_url') or a.get('page_url'),
                license=a.get('license_information'), usage=a.get('usage_permissions'), relevance=a.get('relevance_score'), needs_human_check=True)
    for s in (a.get('narration_segment') or ['unassigned']): by_seg.setdefault(s, []).append(cand)
for s in by_seg: by_seg[s].sort(key=lambda c: -(c['relevance'] or 0))
json.dump(by_seg, open(f'{dest}/research_overrides.json', 'w'), indent=1); print('copied', copied, 'assets;', len(by_seg), 'segments with candidates')
