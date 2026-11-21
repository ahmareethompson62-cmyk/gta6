#!/usr/bin/env python3
"""Verify a consolidated package and stage ONLY usable files for an editor.
Usage: stage.py MANIFEST.json DEST [--editor-dir DIR] [--allow-unapproved]
- Checks each file exists, opens (PIL/ffprobe), meets minimum size; optionally runs the editor's own image stager (cards.stage) as a real usability test.
- Gating: editor_eligible (open licence or human-approved). Everything else goes to blocked[] with the reason; never silently dropped.
- Writes DEST/research_assets.json (usable) and prints exact counts: candidates vs files present vs usable."""
import sys, os, json, shutil, subprocess, tempfile
from PIL import Image

def check_image(p, editor_dir):
    try:
        with Image.open(p) as im: im.verify()
        im = Image.open(p); w, h = im.size
    except Exception as e: return False, f'cannot open: {e}', None
    if w < 700: return False, f'too small {w}x{h}', (w, h)
    if editor_dir:
        sys.path.insert(0, editor_dir)
        try:
            import cards
            out = tempfile.mktemp(suffix='.jpg'); cards.stage(p, out); os.remove(out)
        except Exception as e: return False, f'editor stager failed: {e}', (w, h)
    return True, 'ok', (w, h)

def check_video(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-frames:v', '1', '-f', 'null', '-'], capture_output=True, text=True)
    pr = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', p], capture_output=True, text=True)
    try: j = json.loads(pr.stdout); s = j['streams'][0]; return r.returncode == 0, ('ok' if r.returncode == 0 else r.stderr[-100:]), (s['width'], s['height'], round(float(j['format']['duration']), 1))
    except Exception: return False, 'ffprobe failed', None

def main():
    man_p, dest = sys.argv[1:3]; args = sys.argv[3:]
    editor_dir = args[args.index('--editor-dir') + 1] if '--editor-dir' in args else None; allow = '--allow-unapproved' in args
    man = json.load(open(man_p)); root = os.path.dirname(os.path.abspath(man_p)); os.makedirs(f'{dest}/research', exist_ok=True)
    usable, blocked = [], []; cand = len(man['assets']); present = 0
    for a in man['assets']:
        if a.get('verification_status', '').startswith('rejected'): blocked.append(dict(asset_id=a['asset_id'], reason=a.get('reason') or 'rejected')); continue
        if not a.get('filename'): blocked.append(dict(asset_id=a['asset_id'], url=a.get('original_url'), reason=f"no file ({a.get('download_status')}): {a.get('reason') or 'link/reference only'}")); continue
        p = os.path.join(root, a['filename'])
        if not os.path.exists(p): blocked.append(dict(asset_id=a['asset_id'], reason=f"file missing on disk: {a['filename']} (media is in the workflow artifact, not fetched)")); continue
        present += 1
        ok, why, dims = check_video(p) if a['asset_type'] == 'video' else check_image(p, editor_dir)
        if not ok: blocked.append(dict(asset_id=a['asset_id'], reason=why)); continue
        if not a.get('editor_eligible') and not allow: blocked.append(dict(asset_id=a['asset_id'], url=a.get('original_url'), reason=a.get('eligibility_reason') or 'needs permission')); continue
        tgt = f"{dest}/research/{os.path.basename(p)}"; shutil.copy(p, tgt)
        credit = ' · '.join(x for x in [a.get('source_name'), a.get('source_author')] if x) or a.get('original_url')
        usable.append(dict(asset_id=a['asset_id'], path=os.path.abspath(tgt), type=a['asset_type'], dims=dims, credit=credit, url=a.get('original_url') or a.get('page_url'), license=a.get('license_information'),
                           usage=a.get('usage_permissions'), segment_ids=a.get('narration_segment') or [], relevance=a.get('relevance_score'), suggested_timestamp=a.get('suggested_timestamp'), eligibility=a.get('eligibility_reason'),
                           verified=dict(exists=True, opens=True, editor_stager=bool(editor_dir))))
    json.dump(dict(source_manifest=os.path.abspath(man_p), usable=usable, blocked=blocked), open(f'{dest}/research_assets.json', 'w'), indent=1)
    print(f'candidates {cand} | files present {present} | verified+eligible usable {len(usable)} | blocked {len(blocked)}')
    for b in blocked[:15]: print('  blocked', b['asset_id'], '-', b['reason'][:110])

if __name__ == '__main__': main()
