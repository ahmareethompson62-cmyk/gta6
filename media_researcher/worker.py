#!/usr/bin/env python3
"""Run ONE research job from a plan. Usage: worker.py PLAN.json JOB_ID OUT_DIR
Job types: web (Playwright page capture + extraction), youtube (metadata/captions/timestamps; downloads only CC-licensed),
commons (Wikimedia Commons API; downloads only openly licensed files). Never bypasses auth, CAPTCHA, paywalls or bot checks."""
import sys, os, json, re, subprocess, urllib.parse, time
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import requests

OFFICIAL = ('rockstargames.com', 'take2games.com', 'ir.take2games.com', 'playstation.com', 'xbox.com')

def log(*a): print('[worker]', *a, flush=True)

# ---------------------------------------------------------------- web
def job_web(job, out, res):
    from playwright.sync_api import sync_playwright
    kws = job.get('keywords', [])
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1920, 'height': 1080}, user_agent=UA, device_scale_factor=1)
        for n, url in enumerate(job.get('urls', [])):
            rec = dict(kind='page', original_url=url, job=job['id'], segment_ids=job.get('segment_ids', []))
            host = urllib.parse.urlparse(url).netloc.lower().removeprefix('www.')
            if not robots_ok(url):
                rec.update(download_status='inaccessible', reason='disallowed by robots.txt'); res.append(rec); continue
            polite(url)
            page = ctx.new_page()
            try:
                resp = page.goto(url, wait_until='domcontentloaded', timeout=35000)
                page.wait_for_timeout(2500)
                for label in ('Accept all', 'Accept All', 'I agree', 'Agree', 'Accept'):
                    try:
                        page.get_by_role('button', name=label, exact=True).first.click(timeout=700); break
                    except Exception: pass
                status = resp.status if resp else 0
                body = page.inner_text('body')[:200000] if status else ''
                if status >= 400 or BLOCK_PAT.search(body[:3000]):
                    rec.update(download_status='inaccessible', reason=f'http {status} or bot/consent wall'); res.append(rec); page.close(); continue
                meta = page.evaluate("""() => { const m=n=>{const e=document.querySelector(`meta[property="${n}"],meta[name="${n}"]`);return e?e.content:null};
                  const lic=document.querySelector('link[rel=license],a[rel=license]');
                  return {title:document.title, og_title:m('og:title'), og_image:m('og:image'), published:m('article:published_time')||m('date')||m('pubdate'), author:m('author')||m('article:author'), site:m('og:site_name'), license:lic?lic.href:null}}""")
                paras = page.evaluate("""() => { const root=document.querySelector('article')||document.querySelector('main')||document.body;
                  return Array.from(root.querySelectorAll('p')).map(p=>p.innerText.trim()).filter(t=>t.length>40).join('\\n')}""")
                imgs = page.evaluate("""() => Array.from(document.images).map(i=>({src:i.currentSrc||i.src,alt:i.alt,w:i.naturalWidth,h:i.naturalHeight,inArticle:!!i.closest('article,main')})).filter(i=>i.w>=700&&i.h>=350&&!/logo|avatar|icon|sprite/i.test(i.src))""")
                sc, hits = kw_score((meta.get('title') or '') + ' ' + paras, kws)
                shot = f"{out}/shots/{slug(job['id'])}_{n}.jpg"; os.makedirs(os.path.dirname(shot), exist_ok=True)
                page.screenshot(path=shot, type='jpeg', quality=85)
                rec.update(download_status='screenshot_only', screenshot=shot, title=meta.get('og_title') or meta.get('title'), source_name=meta.get('site') or host,
                           source_author=meta.get('author'), publication_date=meta.get('published'), relevance=round(sc, 2), keyword_hits=hits,
                           evidence=sentences_with(paras, kws), license_information=meta.get('license'), paywall_suspected=bool(PAYWALL_PAT.search(body[:6000])),
                           text_chars=len(paras))
                res.append(rec)
                # candidate images: download only when licence is machine-identifiable as open, or from the official-domain allowlist (flagged for usage check)
                cc = bool(meta.get('license') and 'creativecommons.org' in meta['license'])
                official = any(host == d or host.endswith('.' + d) for d in OFFICIAL)
                cands = ([dict(src=meta['og_image'], alt='og:image', w=0, h=0, inArticle=True)] if meta.get('og_image') else []) + [i for i in imgs if i['inArticle']][:6]
                seen = set()
                for k, im in enumerate(cands[:6]):
                    src = urllib.parse.urljoin(url, im['src'])
                    if src in seen: continue
                    seen.add(src)
                    irec = dict(kind='image', original_url=src, page_url=url, job=job['id'], segment_ids=job.get('segment_ids', []), alt=im.get('alt'),
                                source_name=rec['source_name'], source_author=rec['source_author'], publication_date=rec['publication_date'],
                                relevance=rec['relevance'], keyword_hits=hits, license_information=meta.get('license'))
                    if (cc or official) and robots_ok(src):
                        try:
                            polite(src, 1.0)
                            r = requests.get(src, headers={'User-Agent': UA, 'Referer': url}, timeout=30)
                            if r.ok and r.headers.get('content-type', '').startswith('image'):
                                ext = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}.get(r.headers['content-type'].split(';')[0], 'img')
                                fp = f"{out}/images/{slug(job['id'])}_{n}_{k}.{ext}"; os.makedirs(os.path.dirname(fp), exist_ok=True)
                                open(fp, 'wb').write(r.content)
                                irec.update(download_status='downloaded', file=fp, usage_permissions='CC licence on page' if cc else 'official source: promotional use not verified', )
                            else: irec.update(download_status='inaccessible', reason=f'http {r.status_code}')
                        except Exception as e: irec.update(download_status='inaccessible', reason=str(e)[:120])
                    else:
                        irec.update(download_status='link_only', usage_permissions='unknown: not downloaded (no open licence identified)')
                    res.append(irec)
            except Exception as e:
                rec.update(download_status='inaccessible', reason=str(e)[:160]); res.append(rec)
            finally:
                try: page.close()
                except Exception: pass
        b.close()

# ---------------------------------------------------------------- youtube
def yt(args, timeout=120):
    return subprocess.run(['yt-dlp', '--no-warnings', '--no-playlist-reverse'] + args if False else ['yt-dlp', '--no-warnings'] + args, capture_output=True, text=True, timeout=timeout)

def cue_ranges(json3_path, kws, pad=4):
    d = json.load(open(json3_path)); hits = []
    for ev in d.get('events', []):
        txt = ''.join(s.get('utf8', '') for s in ev.get('segs', []) if s).replace('\n', ' ')
        if txt and any(k.lower() in txt.lower() for k in kws):
            t = ev.get('tStartMs', 0) / 1000; hits.append((t, txt.strip()))
    rng = []
    for t, txt in hits:
        if rng and t - rng[-1][1] < pad * 2: rng[-1][1] = t + pad; rng[-1][2].append(txt)
        else: rng.append([max(0, t - pad), t + pad, [txt]])
    return [dict(start=round(a, 1), end=round(b, 1), caption_excerpt=' / '.join(x)[:160]) for a, b, x in rng[:5]]

def job_youtube(job, out, res):
    kws = job.get('keywords', []); blocked = False
    for q in job.get('queries', []):
        if blocked: break
        r = yt(['-J', '--flat-playlist', f"ytsearch{job.get('max_results', 5)}:{q}"])
        if 'Sign in to confirm' in r.stderr or 'bot' in r.stderr.lower():
            blocked = True; res.append(dict(kind='video_reference', job=job['id'], query=q, download_status='inaccessible', reason='YouTube bot check from runner IP; stopped per policy (no workaround)')); break
        if r.returncode:
            res.append(dict(kind='video_reference', job=job['id'], query=q, download_status='inaccessible', reason=r.stderr.strip()[-200:])); continue
        for e in json.loads(r.stdout).get('entries', [])[:job.get('max_results', 5)]:
            url = e.get('url') or f"https://www.youtube.com/watch?v={e['id']}"
            rec = dict(kind='video_reference', job=job['id'], segment_ids=job.get('segment_ids', []), query=q, original_url=url, title=e.get('title'), source_author=e.get('channel') or e.get('uploader'), duration=e.get('duration'), download_status='link_only')
            time.sleep(3)
            d = yt(['-J', '--skip-download', '--write-auto-subs', '--sub-langs', 'en.*', '--sub-format', 'json3', '-o', f"{out}/subs/%(id)s", url])
            if d.returncode == 0 and d.stdout.strip():
                info = json.loads(d.stdout)
                lic = info.get('license')
                rec.update(publication_date=info.get('upload_date'), duration=info.get('duration'), license_information=lic or 'standard YouTube licence (assumed; not stated)',
                           chapters=[dict(start=c['start_time'], title=c['title']) for c in info.get('chapters') or []][:20], description_excerpt=(info.get('description') or '')[:300])
                subs = [f for f in os.listdir(f'{out}/subs') if f.startswith(info['id']) and f.endswith('.json3')] if os.path.isdir(f'{out}/subs') else []
                if subs:
                    rec['relevant_ranges'] = cue_ranges(f'{out}/subs/{subs[0]}', kws)
                    rec['relevance'] = 1.0 if rec['relevant_ranges'] else 0.0
                if lic and 'creative commons' in lic.lower() and rec.get('relevant_ranges') and job.get('download_cc', True):
                    a = rec['relevant_ranges'][0]; fp = f"{out}/videos/{info['id']}.mp4"; os.makedirs(f'{out}/videos', exist_ok=True)
                    dl = yt(['-f', 'bv*[height<=1080]+ba/b', '--merge-output-format', 'mp4', '--download-sections', f"*{a['start']}-{a['end']+20}", '-o', fp, url], timeout=600)
                    if dl.returncode == 0 and os.path.exists(fp): rec.update(download_status='downloaded', file=fp, usage_permissions='Creative Commons (attribution required)')
                    else: rec['reason'] = 'CC download failed: ' + dl.stderr.strip()[-120:]
                else:
                    rec['usage_permissions'] = 'not downloaded: not CC-licensed; use link + timestamps or ask the creator'
            else:
                if 'Sign in to confirm' in d.stderr: blocked = True; rec['reason'] = 'bot check; stopped'
                else: rec['reason'] = 'metadata unavailable: ' + d.stderr.strip()[-120:]
            res.append(rec)
            if blocked: break

# ---------------------------------------------------------------- commons
def job_commons(job, out, res):
    api = 'https://commons.wikimedia.org/w/api.php'
    for q in job.get('queries', []):
        r = requests.get(api, params=dict(action='query', generator='search', gsrnamespace=6, gsrsearch=q, gsrlimit=job.get('limit', 8), prop='imageinfo',
                         iiprop='url|size|mime|extmetadata', iiurlwidth=1920, format='json'), headers={'User-Agent': UA}, timeout=30)
        for pg in (r.json().get('query', {}).get('pages', {}) or {}).values():
            ii = (pg.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
            lic = (md.get('LicenseShortName') or {}).get('value', ''); artist = re.sub('<[^>]+>', '', (md.get('Artist') or {}).get('value', ''))
            desc = re.sub('<[^>]+>', '', (md.get('ImageDescription') or {}).get('value', ''))
            if not ii.get('mime', '').startswith('image/'): continue   # skip pdf/audio/etc
            rec = dict(kind='image', job=job['id'], segment_ids=job.get('segment_ids', []), query=q, title=pg.get('title'), original_url=ii.get('descriptionurl'),
                       source_name='Wikimedia Commons', source_author=artist, license_information=lic, resolution=f"{ii.get('width')}x{ii.get('height')}", alt=desc[:200])
            sc, hits = kw_score(pg.get('title', '') + ' ' + desc, job.get('keywords', [])); rec.update(relevance=round(sc, 2), keyword_hits=hits)
            ok_lic = bool(re.search(r'(CC[ -]|public domain|PD)', lic, re.I))
            if ok_lic and ii.get('width', 0) >= job.get('min_width', 1000) and ii.get('mime', '').startswith('image'):
                try:
                    polite(api, 1.0); u = ii.get('thumburl') or ii['url']; img = requests.get(u, headers={'User-Agent': UA}, timeout=60)
                    ext = 'png' if 'png' in ii['mime'] else 'jpg'; fp = f"{out}/images/{slug(pg['title'])}.{ext}"; os.makedirs(os.path.dirname(fp), exist_ok=True)
                    open(fp, 'wb').write(img.content); rec.update(download_status='downloaded', file=fp, usage_permissions=f'{lic}; attribution to {artist or "author"}')
                except Exception as e: rec.update(download_status='inaccessible', reason=str(e)[:100])
            else: rec.update(download_status='link_only', usage_permissions=f'not downloaded (licence "{lic}" / size)')
            res.append(rec)

def main():
    plan, jid, out = sys.argv[1:4]; plan = json.load(open(plan))
    job = next(j for j in plan['jobs'] if j['id'] == jid); os.makedirs(out, exist_ok=True); res = []
    t0 = time.time()
    try: {'web': job_web, 'youtube': job_youtube, 'commons': job_commons}[job['type']](job, out, res)
    except Exception as e: res.append(dict(kind='error', job=jid, reason=repr(e)[:300]))
    json.dump(dict(job=jid, type=job['type'], seconds=round(time.time() - t0, 1), results=res), open(f'{out}/results.json', 'w'), indent=1)
    log(jid, len(res), 'records in', round(time.time() - t0), 's')

if __name__ == '__main__': main()
