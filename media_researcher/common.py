"""Shared helpers for media_researcher workers (stdlib + requests only)."""
import json, os, re, time, hashlib, urllib.robotparser, urllib.parse
UA = 'media-researcher/0.1 (research tool; respects robots.txt)'
_last = {}
_robots = {}

def polite(url, gap=2.0):
    host = urllib.parse.urlparse(url).netloc
    wait = _last.get(host, 0) + gap - time.time()
    if wait > 0: time.sleep(wait)
    _last[host] = time.time()

def robots_ok(url, fetch=None):
    """True if robots.txt permits UA to fetch url. Unreachable robots.txt = allowed (standard behaviour)."""
    u = urllib.parse.urlparse(url); base = f'{u.scheme}://{u.netloc}'
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            import requests
            r = requests.get(base + '/robots.txt', headers={'User-Agent': UA}, timeout=15)
            if r.status_code == 200: rp.parse(r.text.splitlines())
            else: rp.allow_all = True
        except Exception:
            rp.allow_all = True
        _robots[base] = rp
    return _robots[base].can_fetch(UA, url)

BLOCK_PAT = re.compile(r'(verify you are (a )?human|captcha|access denied|are you a robot|unusual traffic|enable javascript and cookies|attention required|just a moment)', re.I)
PAYWALL_PAT = re.compile(r'(subscribe to (continue|read)|sign in to (continue|read)|this content is for subscribers)', re.I)

def kw_score(text, keywords):
    t = text.lower(); hits = [k for k in keywords if k.lower() in t]
    return len(hits) / max(1, len(keywords)), hits

def sentences_with(text, keywords, n=2, maxw=25):
    out = []
    for s in re.split(r'(?<=[.!?])\s+', text):
        if any(k.lower() in s.lower() for k in keywords):
            w = s.split()
            out.append(' '.join(w[:maxw]) + ('…' if len(w) > maxw else ''))
        if len(out) >= n: break
    return out

def slug(s, n=40):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:n] or 'x'

def sha1_file(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
