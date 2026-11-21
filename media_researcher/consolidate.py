#!/usr/bin/env python3
"""Merge worker outputs into one research package. Usage: consolidate.py PLAN.json RESULTS_DIR OUT_DIR
Produces OUT/asset_manifest.json, OUT/report.md, and organised OUT/assets/research/{images,videos,screenshots}/.
QC: file opens, min size, dedupe (sha1 + average-hash), relevance score. Never invents licence/permission fields."""
import sys, os, json, glob, shutil, subprocess, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import sha1_file
from PIL import Image

def ahash(p):
    im = Image.open(p).convert('L').resize((8, 8)); px = list(im.getdata()); m = sum(px) / 64
    return sum((1 << i) for i, v in enumerate(px) if v > m)

def ffprobe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height:format=duration', '-of', 'json', p], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout); s = (j.get('streams') or [{}])[0]; return dict(w=s.get('width'), h=s.get('height'), codec=s.get('codec_name'), dur=float(j['format']['duration']))
    except Exception: return None

def main():
    plan_p, rdir, out = sys.argv[1:4]; plan = json.load(open(plan_p)); segs = {s['id']: s for s in plan.get('segments', [])}
    recs = []
    for f in sorted(glob.glob(f'{rdir}/**/results.json', recursive=True)):
        d = json.load(open(f)); base = os.path.dirname(f)
        for r in d['results']:
            for k in ('file', 'screenshot'):
                if r.get(k):
                    # worker paths are relative to the runner workspace; re-anchor to the downloaded artifact folder
                    rel = r[k].split('/', 1)[1] if '/' in r[k] and not os.path.exists(r[k]) else r[k]
                    cand = [r[k], os.path.join(base, os.path.relpath(r[k], r[k].split('/')[0]) if False else os.path.basename(os.path.dirname(r[k])) + '/' + os.path.basename(r[k])),
                            os.path.join(base, 'images', os.path.basename(r[k])), os.path.join(base, 'shots', os.path.basename(r[k])), os.path.join(base, 'videos', os.path.basename(r[k]))]
                    r[k] = next((c for c in cand if os.path.exists(c)), None)
            recs.append(r)
    for sub in ('images', 'videos', 'screenshots'): os.makedirs(f'{out}/assets/research/{sub}', exist_ok=True)
    manifest, seen_sha, seen_ah, rejected = [], {}, [], []
    stats = collections.Counter()
    for i, r in enumerate(recs):
        kind = r.get('kind'); aid = f"A{i+1:03d}"
        if kind == 'error': stats['worker_errors'] += 1; continue
        entry = dict(asset_id=aid, filename=None, asset_type={'page': 'article', 'image': 'image', 'video_reference': 'video'}.get(kind, kind), original_url=r.get('original_url'),
                     source_name=r.get('source_name'), source_author=r.get('source_author'), publication_date=r.get('publication_date'), title=r.get('title'),
                     chapter=None, narration_segment=r.get('segment_ids'), suggested_timestamp=r.get('relevant_ranges'), relevance_reason=None, relevance_score=r.get('relevance'),
                     resolution=r.get('resolution'), duration=r.get('duration'), license_information=r.get('license_information'), usage_permissions=r.get('usage_permissions'),
                     download_status=r.get('download_status'), verification_status='unverified', used_in_final_video=False, reason=r.get('reason'),
                     evidence=r.get('evidence'), page_url=r.get('page_url'))
        if r.get('segment_ids'): entry['chapter'] = sorted({segs[s]['chapter'] for s in r['segment_ids'] if s in segs and 'chapter' in segs[s]}) or None
        if r.get('keyword_hits'): entry['relevance_reason'] = 'keyword matches: ' + ', '.join(r['keyword_hits'])
        elif r.get('relevant_ranges'): entry['relevance_reason'] = 'caption cues mention plan keywords'
        # collected files: QC then place
        fp = r.get('file'); sp = r.get('screenshot')
        for path, sub, label in ((fp, 'images' if kind == 'image' else 'videos', 'file'), (sp, 'screenshots', 'screenshot')):
            if not path: continue
            ent = dict(entry); ent['asset_id'] = aid + ('s' if label == 'screenshot' else ''); ent['asset_type'] = 'screenshot' if label == 'screenshot' else entry['asset_type']
            if label == 'screenshot': ent['download_status'] = 'captured (page screenshot; usage unverified)'
            sha = sha1_file(path)
            if sha in seen_sha: ent.update(verification_status='rejected', reason=f'duplicate of {seen_sha[sha]}'); rejected.append(ent); stats['rejected_duplicate'] += 1; manifest.append(ent); continue
            ok, why = True, None
            if sub in ('images', 'screenshots'):
                try:
                    with Image.open(path) as im: im.verify()
                    im = Image.open(path); w, h = im.size; ent['resolution'] = f'{w}x{h}'
                    if w < (700 if label == 'file' else 1200): ok, why = False, f'too small ({w}x{h})'
                    elif label == 'file':
                        ah = ahash(path)
                        for a2, id2 in seen_ah:
                            if bin(ah ^ a2).count('1') <= 4: ok, why = False, f'near-duplicate of {id2}'; break
                        if ok: seen_ah.append((ah, ent['asset_id']))
                except Exception as e: ok, why = False, f'cannot open: {e}'
            else:
                pr = ffprobe(path)
                if not pr or not pr['w']: ok, why = False, 'video unreadable'
                else: ent['resolution'] = f"{pr['w']}x{pr['h']}"; ent['duration'] = round(pr['dur'], 1)
            if ok and (ent.get('relevance_score') is not None) and ent['relevance_score'] < 0.2 and not (ent.get('usage_permissions') or '').startswith('official'):
                ok, why = False, f"low relevance to plan keywords ({ent['relevance_score']})"
            if not ok: ent.update(verification_status='rejected', reason=why); rejected.append(ent); stats['rejected_qc'] += 1; manifest.append(ent); continue
            seen_sha[sha] = ent['asset_id']
            dest = f"{out}/assets/research/{sub}/{ent['asset_id']}_{os.path.basename(path)}"; shutil.copy(path, dest)
            ent['filename'] = os.path.relpath(dest, out)
            rel = (ent.get('relevance_score') or 0)
            ent['verification_status'] = 'file_ok_relevance_keyword_match_needs_human_check' if rel >= 0.4 else 'file_ok_low_relevance_needs_human_check'
            if not (ent.get('usage_permissions') or '').strip(): ent['usage_permissions'] = 'unknown'
            manifest.append(ent); stats[{'images': 'images', 'videos': 'videos', 'screenshots': 'screenshots'}[sub]] += 1
        if not fp and not sp:
            if entry['download_status'] == 'inaccessible': stats['inaccessible'] += 1
            elif entry['asset_type'] in ('video', 'article', 'image'): stats['link_only'] += 1
            manifest.append(entry)
    awaiting = sum(1 for m in manifest if m['filename'] and (m.get('usage_permissions') or 'unknown').startswith(('unknown', 'official source')))
    json.dump(dict(project=plan.get('project'), topic=plan.get('topic'), assets=manifest), open(f'{out}/asset_manifest.json', 'w'), indent=1)
    L = [f"# Research report: {plan.get('topic')}", '', f"Records discovered: {len(manifest)}", f"- Images collected: {stats['images']}", f"- Videos collected: {stats['videos']}", f"- Page screenshots: {stats['screenshots']}",
         f"- Link/reference only (not downloaded): {stats['link_only']}", f"- Rejected by QC/dedupe: {stats['rejected_qc'] + stats['rejected_duplicate']}", f"- Inaccessible sources: {stats['inaccessible']}",
         f"- Collected files awaiting usage/permission verification: {awaiting}", f"- Worker errors: {stats['worker_errors']}", '', '## Inaccessible / failed']
    for m in manifest:
        if m['download_status'] == 'inaccessible': L.append(f"- {m.get('original_url') or m.get('title')}: {m.get('reason')}")
    L += ['', '## Rejected']
    for m in rejected: L.append(f"- {m['asset_id']} {m.get('original_url')}: {m.get('reason')}")
    L += ['', '## Videos: sources and timestamps (reference)']
    for m in manifest:
        if m['asset_type'] == 'video': L.append(f"- {m.get('title')} ({m.get('source_author')}) {m.get('original_url')} dur={m.get('duration')} ranges={m.get('suggested_timestamp')} [{m['download_status']}]")
    open(f'{out}/report.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:14]))

if __name__ == '__main__': main()
