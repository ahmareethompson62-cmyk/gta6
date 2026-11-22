#!/usr/bin/env python3
"""Fetch official press-kit zips (publisher-provided downloads) on the runner. Usage: press.py PLAN.json OUT_DIR
Plan: {"sources":[{"label","zip_url","page_url","creator","approval"}]}. Respects robots.txt. Records the approval text verbatim in the manifest.
Images wider than 1920 px are downscaled to 1920 (JPEG q90); videos >90 MB are re-encoded to <=1080p CRF 20 so they fit GitHub's per-file limit."""
import sys, os, json, zipfile, subprocess, hashlib, shutil, requests
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from common import UA, robots_ok
plan = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out + '/images', exist_ok=True); os.makedirs(out + '/videos', exist_ok=True); os.makedirs(out + '/sheets', exist_ok=True)
man = []; IMG = ('.jpg', '.jpeg', '.png', '.webp'); VID = ('.mp4', '.mov', '.m4v', '.webm')
def sha(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()
def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height,r_frame_rate:format=duration', '-of', 'json', p], capture_output=True, text=True)
    try: j = json.loads(r.stdout); s = j['streams'][0]; return s['codec_name'], s['width'], s['height'], round(float(j['format']['duration']), 1), s['r_frame_rate']
    except Exception: return None
for s in plan['sources']:
    lab = s['label']; url = s['zip_url']
    if not robots_ok(url): print('robots disallows', url); man.append(dict(label=lab, status='inaccessible', reason='disallowed by robots.txt', zip_url=url)); continue
    zp = f'/tmp/{lab}.zip'
    try:
        with requests.get(url, headers={'User-Agent': UA, 'Referer': s.get('page_url', '')}, stream=True, timeout=120) as r:
            print(lab, r.status_code, r.headers.get('content-length'))
            if not r.ok: man.append(dict(label=lab, status='inaccessible', reason=f'http {r.status_code}', zip_url=url)); continue
            with open(zp, 'wb') as f:
                for ch in r.iter_content(1 << 20): f.write(ch)
        z = zipfile.ZipFile(zp); xd = f'/tmp/x_{lab}'; z.extractall(xd)
    except Exception as e:
        man.append(dict(label=lab, status='inaccessible', reason=repr(e)[:200], zip_url=url)); continue
    n = 0
    for root, _, fs in os.walk(xd):
        for fn in sorted(fs):
            p = os.path.join(root, fn); ext = os.path.splitext(fn)[1].lower(); rel = os.path.relpath(p, xd)
            if '__MACOSX' in rel or fn.startswith('.'): continue
            n += 1; aid = f'{lab}_{n:03d}'
            base = dict(asset_id=aid, label=lab, zip_url=url, page_url=s.get('page_url'), inner_path=rel, creator=s.get('creator', 'Rockstar Games'),
                        usage_permissions=f"approved by {s['approval']}", license_note='Official publisher press-kit download; the page states no usage terms.')
            if ext in IMG:
                try:
                    im = Image.open(p); w0, h0 = im.size
                    if w0 < 700: continue
                    im = im.convert('RGB')
                    if w0 > 1920: im = im.resize((1920, round(h0 * 1920 / w0)), Image.LANCZOS)
                    fp = f'{out}/images/{aid}.jpg'; im.save(fp, quality=90)
                    man.append(dict(base, kind='image', filename=os.path.relpath(fp, out), orig_size=f'{w0}x{h0}', size=f'{im.size[0]}x{im.size[1]}', sha1=sha(fp), status='collected'))
                except Exception as e: man.append(dict(base, kind='image', status='unreadable', reason=repr(e)[:100]))
            elif ext in VID:
                pr = probe(p)
                if not pr: man.append(dict(base, kind='video', status='unreadable')); continue
                fp = f'{out}/videos/{aid}.mp4'
                if os.path.getsize(p) > 90e6 or pr[0] != 'h264' or pr[2] > 1080 or ext != '.mp4':
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', "scale='min(1920,iw)':-2", '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', fp], check=False)
                    if os.path.exists(fp) and os.path.getsize(fp) > 95e6:
                        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', "scale='min(1920,iw)':-2", '-c:v', 'libx264', '-crf', '25', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', fp])
                else: shutil.copy(p, fp)
                if not os.path.exists(fp): man.append(dict(base, kind='video', status='transcode_failed')); continue
                q = probe(fp)
                man.append(dict(base, kind='video', filename=os.path.relpath(fp, out), orig=f'{pr[1]}x{pr[2]} {pr[0]} {pr[4]}', size=f'{q[1]}x{q[2]}' if q else None, duration=q[3] if q else None, bytes=os.path.getsize(fp), sha1=sha(fp), status='collected'))
    print(lab, 'files', n)
# contact sheets (for choosing assets): images 6x5, videos 8 frames each
from PIL import ImageDraw
ims = [m for m in man if m.get('kind') == 'image' and m.get('filename')]
for k in range(0, len(ims), 30):
    ch = ims[k:k + 30]; W, H = 320, 180; sh = Image.new('RGB', (W * 6, H * 5), (0, 0, 0)); d = ImageDraw.Draw(sh)
    for j, m in enumerate(ch):
        im = Image.open(f"{out}/{m['filename']}").convert('RGB'); im.thumbnail((W, H)); sh.paste(im, ((j % 6) * W, (j // 6) * H)); d.rectangle(((j % 6) * W, (j // 6) * H, (j % 6) * W + 150, (j // 6) * H + 14), fill=(0, 0, 0)); d.text(((j % 6) * W + 2, (j // 6) * H + 1), m['asset_id'], fill=(255, 255, 0))
    sh.save(f'{out}/sheets/images_{k // 30:02d}.jpg', quality=80)
for m in man:
    if m.get('kind') == 'video' and m.get('filename'):
        sp = f"{out}/sheets/{m['asset_id']}.jpg"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f"{out}/{m['filename']}", '-vf', f"fps={8 / max(m['duration'], 8):.4f},scale=320:-1,tile=4x2", '-frames:v', '1', sp])
json.dump(dict(project=plan.get('project'), assets=man), open(out + '/press_manifest.json', 'w'), indent=1)
print('collected', sum(1 for m in man if m.get('status') == 'collected'), 'of', len(man))
