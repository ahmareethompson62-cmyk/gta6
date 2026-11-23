"""Component library for the paper-cutout explainer style. All coordinates are in 1920x1080 stage pixels."""
import json, math, random, os, re, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sents = json.load(open('/home/claude/rockstar_video/sents.json'))
WORDS = json.load(open('/home/claude/rockstar_video/words.json'))
DUR = 293.25
EL = []          # all elements
CUR = dict(t0=0, t1=DUR, n=0)
COL = dict(cream='#efe8d6', tan='#c19a63', mint='#b6dfae', teal='#2bb5a2', org='#e8602c', yel='#f2b82e', pink='#e8559b', red='#d93a2b', blue='#6aa7d9', vio='#8a5be0', ink='#1d1b19', paper='#f4f1e8')

# ---------------- timing helpers (from the real narration alignment)
def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())
def sw(i):  # words of sentence i
    return [w for w in WORDS if w['sent'] == i]
def wt(i, k=0):  # start time of kth word in sentence i
    ws = sw(i); return ws[min(k, len(ws) - 1)]['s']
def ph(i, phrase):
    """(start,end,tokens) of a phrase inside sentence i (matched on the aligned words)."""
    ws = sw(i); toks = [norm(x) for x in phrase.replace('-', ' ').split()]
    for a in range(len(ws)):
        ok = True
        for b, tk in enumerate(toks):
            if a + b >= len(ws) or not norm(ws[a + b]['w']).startswith(tk[:4]): ok = False; break
        if ok: return ws[a]['s'], ws[a + len(toks) - 1]['e'], ws[a:a + len(toks)]
    # fallback: slice of the actually spoken words between the first and last phrase word
    def find(tk, start=0):
        for n in range(start, len(ws)):
            if norm(ws[n]['w']).startswith(tk[:4]): return n
        return None
    a = find(toks[0]); b = find(toks[-1], a or 0) if a is not None else None
    if a is not None and b is not None and b >= a and b - a < len(toks) + 4:
        return ws[a]['s'], ws[b]['e'], ws[a:b + 1]
    raise KeyError(f'phrase {phrase!r} not found in sentence {i}: {[w["w"] for w in ws]}')
def pt(i, phrase): return ph(i, phrase)[0]

def scene(a, b, t0=None, t1=None):
    """Scene spans sentences a..b. Starts just before the first word; ends where the next scene starts."""
    CUR['t0'] = max(0, (sents[a]['start'] - 0.12)) if t0 is None else t0
    CUR['t1'] = (sents[b]['end'] + 0.12) if t1 is None else t1
    CUR['n'] = 0
    return CUR['t0']

def el(html, x, y, w, h, t0=None, t1=None, **k):
    CUR['n'] += 1
    d = dict(html=html, x=x, y=y, w=w, h=h, t0=CUR['t0'] if t0 is None else t0, t1=CUR['t1'] if t1 is None else t1, z=k.pop('z', CUR['n']))
    d.update(k)
    if 'drift' not in d and d.get('z') != 2000 and d.get('in') != 'draw' and 'pan' not in d: d['drift'] = 0.018
    if 'od' not in d: d['od'] = 'lrud'[len(EL) % 4] if d.get('out', 'fly') == 'fly' else 'r'
    EL.append(d); return d

# ---------------- shapes
def torn(w, h, seed=1, j=6, step=42):
    r = random.Random(seed); P = []
    def jit(): return r.uniform(0, j)
    n = max(3, int(w / step))
    for i in range(n): P.append((w * i / n, jit()))
    m = max(3, int(h / step))
    for i in range(m): P.append((w - jit(), h * i / m))
    for i in range(n): P.append((w * (n - i) / n, h - jit()))
    for i in range(m): P.append((jit(), h * (m - i) / m))
    return 'polygon(' + ','.join(f'{x:.1f}px {y:.1f}px' for x, y in P) + ')'

def tapes(corners=('tl', 'br'), seed=3):
    r = random.Random(seed); s = ''
    pos = dict(tl=('left:-46px;top:-12px', -35), tr=('right:-46px;top:-12px', 35), bl=('left:-46px;bottom:-12px', 35), br=('right:-46px;bottom:-12px', -35), tc=('left:calc(50% - 75px);top:-24px', r.uniform(-4, 4)), bc=('left:calc(50% - 75px);bottom:-24px', r.uniform(-4, 4)))
    for c in corners:
        p, rot = pos[c]; s += f'<div class="tape t" style="{p};transform:rotate({rot + r.uniform(-5, 5):.1f}deg)"></div>'
    return s

def card(inner, w, h, color='cream', seed=1, tp=('tl', 'br'), pad=0, cls='', style=''):
    c = COL.get(color, color)
    return (f'<div class="fill sh"><div class="fill pp {cls}" style="--c:{c};clip-path:{torn(w, h, seed)};padding:{pad}px;box-sizing:border-box;{style}">{inner}</div>{tapes(tp, seed) if tp else ""}</div>')

def ransom(i, phrase, hl=(), cls='', cols=None, sz=''):
    """Ransom-note tiles for words of `phrase` in sentence i; each tile pops at its spoken time. Returns (html, t_first, t_last)."""
    a, b, toks = ph(i, phrase) if isinstance(phrase, str) else phrase
    raw = phrase.replace('-', ' ').split() if isinstance(phrase, str) else [t['w'] for t in toks]
    if len(raw) != len(toks): raw = [t['w'] for t in toks]
    palette = cols or ['w', 'k', 'w', 'w', 'k', 'w']
    out = []
    for n, (tk, word) in enumerate(zip(toks, raw)):
        c = 'o' if (n in hl or word.lower().strip('.,?!"') in [str(x).lower().replace('-', ' ').split()[0] for x in hl]) else palette[n % len(palette)]
        out.append(f'<i class="{c}" data-t="{tk["s"] - 0.04:.3f}" style="opacity:0">{word}</i>')
    return f'<div class="ran {cls} {sz}">' + ''.join(out) + '</div>', a, b

def cap(i, phrase, x, y, w=1500, hl=(), cls='', sz='', cols=None, **k):
    html, a, b = ransom(i, phrase, hl, cls, cols, sz)
    t0 = k.pop('t0', a - 0.06)
    return el(f'<div class="c fill">{html}</div>', x, y, w, 260, t0=t0, **{'in': 'fade', 'din': 0.1, **k})

def tile(text, x, y, c='w', w=900, sz='', t0=None, t1=None, **k):
    """Ransom tile(s) that appear as a whole at t0 (for static callouts)."""
    t0 = CUR['t0'] if t0 is None else t0
    words = ''.join(f'<i class="{c if n != 1 else c}" data-t="{t0 + n * 0.12:.3f}" style="opacity:0">{wd}</i>' for n, wd in enumerate(text.split()))
    return el(f'<div class="c fill"><div class="ran {sz}">{words}</div></div>', x, y, w, 220, t0=t0, t1=t1, **{'in': 'fade', 'din': 0.05, **k})

def stamp(text, x, y, t0, color='red', rot=-7, size=46, w=None, **k):
    w = w or int(len(text) * size * .62 + 70)
    col = COL.get(color, color)
    return el(f'<div class="stamp" style="border-color:{col};color:{col};font-size:{size}px;position:relative;text-align:center;transform:none">{text}</div>', x, y, w, size + 40, t0=t0, r=rot, **{'in': 'stamp', 'din': .22, **k})

def label(text, x, y, t0, w=None, size=24, **k):
    w = w or int(len(text) * size * .62 + 40)
    return el(f'<div class="lab" style="font-size:{size}px">{text}</div>', x, y, w, size + 24, t0=t0, **{'in': 'slide', 'id': 'l', **k})

def src(text, t0=None, x=40, y=34, **k):
    """Small credit chip, bottom-left like a lower-third source tag."""
    w = int(len(text) * 13.6 + 30)
    return el(f'<div class="src">{text}</div>', x + w / 2, y, w, 38, t0=(CUR['t0'] + 0.5) if t0 is None else t0, z=900, **{'in': 'slide', 'id': 'l', 'din': .3, **k})

def sticker(text, x, y, t0, c='yel', size=40, rot=-3, **k):
    w = int(len(text) * size * .6 + 50)
    return el(f'<div class="c fill A" style="background:{COL.get(c, c)};color:{"#1d1b19" if c in ("yel","mint","cream","tan") else "#fff"};font-size:{size}px;box-shadow:0 6px 9px rgba(0,0,0,.45);padding-top:4px">{text}</div>', x, y, w, size + 30, t0=t0, r=rot, **{'in': 'pop', **k})

# ---------------- media
def clipref(srcp, ss, dur, name=None, scale=None):
    key = hashlib.md5(f'{srcp}{ss}{dur}'.encode()).hexdigest()[:10]
    d = f'frames/{key}'; full = os.path.join(HERE, d)
    n = int(dur * 30)
    if not os.path.exists(full + '/done'):
        os.makedirs(full, exist_ok=True)
        sc = f',scale={scale}:-2' if scale else ''
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', srcp, '-vf', f'fps=30{sc}', '-q:v', '3', full + '/%05d.jpg'], check=True)
        open(full + '/done', 'w').write('1')
    n = len([f for f in os.listdir(full) if f.endswith('.jpg')])
    return dict(dir=d, n=n)

def media_html(m, fit='cover'):
    if m.get('clip'): return f'<div class="clipw"><img class="fr{" crop" if m.get("crop") else ""}" alt=""></div>'
    return f'<div class="clipw"><div class="ph" style="background-image:url(\'{m["img"]}\');background-position:{m.get("pos","center")}"></div></div>'

def M_img(path, pos='center'): return dict(img=path, pos=pos)
def M_clip(srcp, ss, dur, scale=None): return dict(clip=clipref(srcp, ss, dur, scale=scale), crop=('gta5' in srcp))

def polaroid(m, x, y, w, h, t0=None, cap_text='', rot=-3, color='paper', **k):
    pw, ph_ = w - 36, h - (88 if cap_text else 50)
    inner = (f'<div style="position:absolute;left:18px;top:18px;width:{pw}px;height:{ph_}px;overflow:hidden;background:#222">{media_html(m)}</div>'
             f'<div class="cp">{cap_text}</div>')
    html = f'<div class="fill sh"><div class="fill pol" style="background:{COL.get(color, color)};padding:0">{inner}</div>{tapes(("tc",), int(x))}</div>'
    d = el(html, x, y, w, h, t0=t0, r=rot, **k)
    if m.get('clip'): d['clip'] = m['clip']
    return d

def tv(m, x, y, w, t0=None, rot=-2, color='teal', cap_text='', **k):
    h = int(w * 9 / 16) + 90
    sw_, sh_ = w - 150, int(w * 9 / 16) - 20
    inner = (f'<div class="fill tvf" style="background:{COL.get(color, color)}"></div>'
             f'<div style="position:absolute;left:34px;top:34px;width:{sw_}px;height:{sh_}px;border-radius:28px;overflow:hidden;background:#000;box-shadow:0 0 0 8px #1d1b19">{media_html(m)}</div>'
             f'<div class="knob" style="right:34px;top:{sh_ // 2 - 40}px"></div><div class="knob" style="right:34px;top:{sh_ // 2 + 30}px;background:#efe8d6"></div>'
             f'<div style="position:absolute;left:{w // 2 - 160}px;bottom:8px;width:320px;height:44px;background:#1d1b19;border-radius:0 0 22px 22px;color:#efe8d6;font:700 22px Mono,monospace;display:flex;align-items:center;justify-content:center;letter-spacing:.1em">{cap_text}</div>')
    d = el(f'<div class="fill sh">{inner}</div>', x, y, w, h, t0=t0, r=rot, **k)
    if m.get('clip'): d['clip'] = m['clip']
    return d

# ---------------- article crops with camera pans & highlighter
SHOT = '/home/claude/rr11/package/assets/research/screenshots/'
NEWS = dict(aj=SHOT + 'A037s_w-aj_0.jpg', gr=SHOT + 'A040s_w-gr_0.jpg', gx=SHOT + 'A044s_w-gx_0.jpg', pcg1=SHOT + 'A058s_w-pcg1_0.jpg', pcg2=SHOT + 'A060s_w-pcg2_0.jpg', sj=SHOT + 'A063s_w-sj_0.jpg', tr=SHOT + 'A070s_w-tr_0.jpg', wccf=SHOT + 'A072s_w-wccf_0.jpg')
REG = dict(
 gx=dict(wide=(.5,.5,1), head=(.40,.20,.42), date=(.35,.27,.30), logo=(.40,.57,.45)),
 aj=dict(wide=(.5,.5,1), head=(.37,.46,.38), sub=(.40,.53,.30)),
 gr=dict(wide=(.5,.5,1), head=(.41,.51,.38), quote=(.41,.64,.30)),
 pcg1=dict(wide=(.5,.5,1), head=(.42,.56,.42), by=(.40,.70,.30), sub=(.42,.73,.30)),
 pcg2=dict(wide=(.5,.5,1), head=(.41,.52,.40), date=(.38,.72,.30), prot=(.41,.90,.35)),
 sj=dict(wide=(.5,.5,1), head=(.475,.27,.42), left=(.29,.80,.26), mid=(.50,.84,.24), right=(.70,.80,.26)),
 tr=dict(wide=(.5,.5,1), head=(.41,.55,.40), sub=(.41,.68,.30)),
 wccf=dict(wide=(.5,.5,1), head=(.50,.33,.50), img=(.50,.60,.45), cap=(.40,.86,.30)))
HLR = dict(gx=(.17,.14,.46,.10), aj=(.19,.40,.36,.11), gr=(.25,.44,.32,.14), pcg1=(.25,.43,.33,.24), pcg2=(.25,.43,.33,.18), sj=(.30,.19,.35,.15), tr=(.25,.47,.33,.15), wccf=(.20,.27,.60,.11))
PW, PH = 1920, 1080
def view(key, reg, w, h):
    cx, cy, sz = REG[key][reg] if isinstance(reg, str) else reg
    S = w / (sz * PW)
    S = max(S, w / PW, h / PH)
    tx = w / 2 - cx * PW * S; ty = h / 2 - cy * PH * S
    tx = min(0, max(w - PW * S, tx)); ty = min(0, max(h - PH * S, ty))
    return dict(tx=tx, ty=ty, S=S)

def article(key, reg, x, y, w, h, t0=None, reg2=None, pan=None, hl=None, rot=-2, color='paper', **k):
    """Screenshot card whose camera pans smoothly reg -> reg2; optional highlighter wipe at time hl."""
    pad = 14; iw, ih = w - 2 * pad, h - 2 * pad
    t0 = CUR['t0'] if t0 is None else t0
    a = view(key, reg, iw, ih)
    kf = None
    if reg2:
        b = view(key, reg2, iw, ih); p0, p1 = pan if pan else (t0 + .6, t0 + 2.4)
        kf = [[t0, a], [p0, a], [p1, b]]
    else: kf = [[t0, a], [t0 + 8, a]]
    hlhtml = ''
    if hl is not None:
        hx, hy, hw, hh = HLR[key]; hlhtml = f'<div class="hlm" data-w="{hl:.3f}" data-wd="0.6" style="left:{hx * PW}px;top:{hy * PH}px;width:{hw * PW}px;height:{hh * PH}px;clip-path:inset(0 100% 0 0)"></div>'
    inner = (f'<div style="position:absolute;left:{pad}px;top:{pad}px;width:{iw}px;height:{ih}px;overflow:hidden;background:#fff"><div class="pn" style="position:absolute;left:0;top:0;width:{PW}px;height:{PH}px;transform-origin:0 0;background:url(\'{NEWS[key]}\') 0 0/{PW}px {PH}px no-repeat">{hlhtml}</div></div>')
    html = f'<div class="fill sh"><div class="fill" style="background:{COL.get(color, color)}">{inner}</div>{tapes(("tl", "br"), int(y))}</div>'
    return el(html, x, y, w, h, t0=t0, r=rot, pan=kf, **k)

# ---------------- people
SIL = '<svg viewBox="0 0 100 120" width="100%" height="100%" style="position:absolute;inset:0"><rect width="100" height="120" fill="#cfc7b5"/><circle cx="50" cy="42" r="21" fill="#8d8675"/><path d="M8 125c2-30 18-46 42-46s40 16 42 46z" fill="#8d8675"/></svg>'
def person(x, y, w, name, role='', photo=None, t0=None, rot=-2, pos='center 22%', **k):
    h = int(w * 1.22)
    face = (f'<div class="ph" style="background-image:url(\'{photo}\');background-position:{pos}"></div>' if photo else SIL)
    inner = (f'<div class="fill sh"><div class="fill" style="background:#f4f1e8;border-radius:22px"></div>'
             f'<div style="position:absolute;left:14px;top:14px;right:14px;bottom:{70 if role else 54}px;border-radius:14px;overflow:hidden;background:#cfc7b5">{face}</div>'
             f'<div class="c A" style="position:absolute;left:0;right:0;bottom:{26 if role else 8}px;font-size:{int(w * .115)}px;color:#1d1b19;height:{int(w * .15)}px">{name}</div>'
             + (f'<div class="c M" style="position:absolute;left:0;right:0;bottom:6px;font-size:{int(w * .062)}px;font-weight:700;color:#555;height:{int(w * .09)}px">{role}</div>' if role else '') + '</div>')
    return el(inner, x, y, w, h, t0=t0, r=rot, **k)

# ---------------- icons (svg strings, viewBox 0 0 100 100)
def svg(body, s=120, vb='0 0 100 100', style=''): return f'<svg viewBox="{vb}" width="{s}" height="{s}" style="{style}">{body}</svg>'
def I(name, c='#efe8d6', c2='#1d1b19'):
    sk = f'stroke="{c2}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
    if name == 'gear':
        t = ''.join(f'<rect x="43" y="4" width="14" height="22" rx="3" fill="{c}" {sk} transform="rotate({a} 50 50)"/>' for a in range(0, 360, 45))
        return t + f'<circle cx="50" cy="50" r="30" fill="{c}" {sk}/><circle cx="50" cy="50" r="12" fill="{c2}"/>'
    if name == 'doc': return f'<path d="M22 8h40l18 18v66H22z" fill="{c}" {sk}/><path d="M62 8v18h18" fill="none" {sk}/>' + ''.join(f'<path d="M32 {y}h36" {sk}/>' for y in (44, 56, 68, 80))
    if name == 'mag': return f'<circle cx="42" cy="42" r="26" fill="rgba(255,255,255,.25)" stroke="{c}" stroke-width="9"/><path d="M62 62l28 28" stroke="{c}" stroke-width="12" stroke-linecap="round"/>'
    if name == 'gavel': return f'<g transform="rotate(-35 50 40)"><rect x="22" y="18" width="46" height="26" rx="6" fill="{c}" {sk}/><rect x="42" y="42" width="8" height="46" fill="{c}" {sk}/></g><rect x="14" y="84" width="72" height="10" rx="3" fill="{c}" {sk}/>'
    if name == 'clock': return f'<circle cx="50" cy="50" r="42" fill="{c}" {sk}/>' + ''.join(f'<path d="M50 14v8" {sk} transform="rotate({a} 50 50)"/>' for a in range(0, 360, 30))
    if name == 'hand': return f'<path d="M50 52V20" stroke="{c2}" stroke-width="7" stroke-linecap="round"/><path d="M50 52l18 8" stroke="{c2}" stroke-width="6" stroke-linecap="round"/><circle cx="50" cy="52" r="6" fill="{c2}"/>'
    if name == 'bubble': return f'<path d="M14 18h72a8 8 0 0 1 8 8v36a8 8 0 0 1-8 8H48L28 90V70H14a8 8 0 0 1-8-8V26a8 8 0 0 1 8-8z" fill="{c}" {sk}/>'
    if name == 'mega': return f'<path d="M12 40h22l40-22v64L34 60H12z" fill="{c}" {sk}/><path d="M34 60l8 26h12L48 62" fill="{c}" {sk}/><path d="M84 36q8 14 0 28" fill="none" {sk}/>'
    if name == 'person': return f'<circle cx="50" cy="28" r="16" fill="{c}" {sk}/><path d="M18 92c0-26 12-40 32-40s32 14 32 40z" fill="{c}" {sk}/>'
    if name == 'x': return f'<path class="dr" pathLength="1" d="M14 14L86 86M86 14L14 86" fill="none" stroke="{c}" stroke-width="11" stroke-linecap="round"/>'
    if name == 'check': return f'<path class="dr" pathLength="1" d="M14 54L40 80L88 20" fill="none" stroke="{c}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
    if name == 'balance': return f'<path d="M50 20V88M30 90h40" {sk} stroke-width="6"/><g class="beam"><path d="M10 26h80" {sk} stroke-width="6"/><path d="M10 26L2 54h16zM90 26L82 54h16z" fill="{c}" {sk}/></g>'
    if name == 'pin': return f'<path d="M50 94C28 66 20 52 20 38a30 30 0 0 1 60 0c0 14-8 28-30 56z" fill="{c}" {sk}/><circle cx="50" cy="38" r="11" fill="{c2}"/>'
    if name == 'burst': return f'<polygon points="50,2 61,26 86,14 78,40 98,50 78,60 86,86 61,74 50,98 39,74 14,86 22,60 2,50 22,40 14,14 39,26" fill="{c}" {sk}/>'
    if name == 'ballot': return f'<rect x="14" y="44" width="72" height="48" rx="4" fill="{c}" {sk}/><path d="M36 58h28" {sk} stroke-width="7"/><path d="M32 40V12h36v28z" fill="#fff" {sk}/><path d="M40 24h20M40 32h14" {sk} stroke-width="3"/>'
    if name == 'cup': return f'<path d="M16 28h54v32a24 24 0 0 1-24 24h-6a24 24 0 0 1-24-24z" fill="{c}" {sk}/><path d="M70 36h8a10 10 0 0 1 0 22h-8" fill="none" {sk}/><path d="M32 8q6 8 0 14M48 8q6 8 0 14" fill="none" {sk}/>'
    if name == 'radio': return f'<rect x="8" y="30" width="84" height="58" rx="8" fill="{c}" {sk}/><circle cx="34" cy="60" r="16" fill="{c2}"/><path d="M60 50h22M60 62h22M60 74h22" {sk}/><path d="M24 30L60 6" {sk}/>'
    if name == 'sign': return f'<rect x="8" y="12" width="84" height="46" rx="3" fill="{c}" {sk}/><path d="M30 58v36M70 58v36" {sk}/><path d="M20 30h60M20 42h40" {sk}/>'
    if name == 'mic': return f'<rect x="36" y="8" width="28" height="50" rx="14" fill="{c}" {sk}/><path d="M24 44a26 26 0 0 0 52 0M50 70v20M34 92h32" fill="none" {sk}/>'
    if name == 'teeth': return f'<path d="M6 40q44-34 88 0-4 34-44 38-40-4-44-38z" fill="#c33" {sk}/><path d="M12 46l7 12 7-12 7 12 7-12 7 12 7-12 7 12 7-12 7 12 7-12" fill="#fff" {sk} stroke-width="3"/>'
    if name == 'cross': return f'<circle cx="50" cy="50" r="34" fill="none" stroke="{c}" stroke-width="7"/><path d="M50 4v30M50 66v30M4 50h30M66 50h30" stroke="{c}" stroke-width="7"/><circle cx="50" cy="50" r="5" fill="{c}"/>'
    if name == 'star': return f'<polygon points="50,6 62,38 96,38 68,58 79,92 50,71 21,92 32,58 4,38 38,38" fill="{c}" {sk}/>'
    if name == 'folder': return f'<path d="M8 24h30l8 10h46v52H8z" fill="{c}" {sk}/>'
    if name == 'cal': return f'<rect x="10" y="16" width="80" height="74" rx="6" fill="{c}" {sk}/><rect x="10" y="16" width="80" height="20" fill="#d93a2b" {sk}/>'
    if name == 'laugh': return f'<circle cx="50" cy="50" r="42" fill="{c}" {sk}/><path d="M26 40q6-8 12 0M62 40q6-8 12 0" fill="none" {sk}/><path d="M24 58q26 34 52 0z" fill="#fff" {sk}/>'
    if name == 'fist': return f'<rect x="22" y="30" width="56" height="46" rx="12" fill="{c}" {sk}/><path d="M34 30v22M46 30v22M58 30v22" {sk}/><rect x="30" y="74" width="40" height="18" rx="4" fill="{c}" {sk}/>'
    if name == 'discord': return f'<rect x="6" y="14" width="88" height="64" rx="16" fill="#5865f2" {sk}/><circle cx="34" cy="46" r="9" fill="#fff"/><circle cx="66" cy="46" r="9" fill="#fff"/><path d="M26 86l12-10h24l12 10" fill="#5865f2" {sk}/>'
    raise KeyError(name)
def ico(name, s=120, c='#efe8d6', c2='#1d1b19', cls=''): return f'<svg viewBox="0 0 100 100" width="{s}" height="{s}" class="{cls}">{I(name, c, c2)}</svg>'

def icon(name, x, y, s, t0=None, c='#efe8d6', c2='#1d1b19', rot=0, **k):
    return el(f'<div class="fill sh">{ico(name, s, c, c2)}</div>', x, y, s, s, t0=t0, r=rot, **k)

def crossout(x, y, s, t0, c='#d93a2b', **k):
    return el(f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{I("x", c)}</svg>', x, y, s, s, t0=t0, **{'in': 'draw', 'din': .05, 'dd': .35, **k})
def checkmark(x, y, s, t0, c='#2bb5a2', **k):
    return el(f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{I("check", c)}</svg>', x, y, s, s, t0=t0, **{'in': 'draw', 'din': .05, 'dd': .4, **k})

# ---------------- paper blocks
def calendar(month, day, x, y, t0, year='', w=230, rot=-3, **k):
    h = int(w * 1.0)
    return el(f'<div class="fill sh"><div class="cal" style="width:100%;height:100%;border-radius:10px;overflow:hidden"><div class="m" style="font-size:{int(w*.15)}px;padding:{int(w*.04)}px 0">{month}</div><div class="d" style="font-size:{int(w*.5)}px;line-height:1.0;margin-top:{int(w*.03)}px">{day}</div><div class="y" style="font-size:{int(w*.11)}px">{year}</div></div></div>', x, y, w, h, t0=t0, r=rot, **k)

def note(title, lines, x, y, w, h, t0=None, color='cream', rot=-1.5, seed=5, **k):
    body = ''.join(f'<div class="E" style="font-size:34px;color:#1d1b19;border-bottom:2px solid rgba(60,50,30,.25);padding:6px 0">{l}</div>' for l in lines)
    inner = f'<div class="M" style="font-size:22px;font-weight:700;color:#7a6a4a;letter-spacing:.1em;text-transform:uppercase">{title}</div>{body}'
    return el(card(inner, w, h, color, seed, pad=26), x, y, w, h, t0=t0, r=rot, **k)

def textcard(text, x, y, w, h, t0=None, color='paper', fs=44, cls='P', rot=-1.5, seed=9, tp=('tl', 'br'), fc='#1d1b19', **k):
    return el(card(f'<div class="c fill {cls}" style="padding:30px 40px;box-sizing:border-box;font-size:{fs}px;color:{fc};line-height:1.2;text-transform:none">{text}</div>', w, h, color, seed, tp), x, y, w, h, t0=t0, r=rot, **k)

def typed(text, x, y, w, h, t0, cps=26, title='', fs=38, color='cream', rot=-1.2, seed=11, **k):
    inner = (f'<div class="M" style="font-size:22px;font-weight:700;color:#7a6a4a;letter-spacing:.1em;text-transform:uppercase">{title}</div>' if title else '') + f'<div class="E typ" data-text="{text}" style="font-size:{fs}px;color:#1d1b19;line-height:1.28;margin-top:12px"></div>'
    return el(card(inner, w, h, color, seed, pad=34), x, y, w, h, t0=t0, r=rot, cps=cps, **{'in': 'pop', **k})

def chat(lines, x, y, w, h, t0, title='#general', **k):
    body = ''.join(f'<div class="chat" data-t="{t0 + .5 + n * .9:.2f}" style="opacity:0">{l}</div>' for n, l in enumerate(lines))
    return el(f'<div class="fill sh"><div class="win fill"><div class="bar"><b style="background:#ff5f57"></b><b style="background:#febc2e"></b><b style="background:#28c840"></b><span class="M" style="margin-left:14px;font-size:20px;opacity:.6">{title}</span></div>{body}</div></div>', x, y, w, h, t0=t0, **k)

def counter(to, x, y, t0, size=170, pre='', suf='', c='#efe8d6', dec=0, d=1.2, fmt='', cls='A', rot=0, **k):
    return el(f'<div class="c fill {cls}" style="font-size:{size}px;color:{c};text-shadow:0 8px 12px rgba(0,0,0,.5)"><span data-from="0" data-to="{to}" data-dec="{dec}" data-d="{d}" data-pre="{pre}" data-suf="{suf}" data-fmt="{fmt}">0</span></div>', x, y, int(size * 5), int(size * 1.3), t0=t0, r=rot, **{'in': 'pop', **k})

def sweep(t, color='org', seed=4, dur=.7):
    """Torn-paper wipe across the whole frame (used only at section changes)."""
    W, H = 2600, 1300
    d = el(f'<div class="fill sh"><div class="fill pp" style="--c:{COL.get(color, color)};clip-path:{torn(W, H, seed, 26, 90)}"></div></div>', 960, 540, W, H, t0=t - dur / 2 - .15, t1=t + dur / 2, z=2000, **{'in': 'cut', 'out': 'none', 'din': .01, 'dout': .01})
    d['kf'] = [[t - dur / 2 - .15, dict(x=2900)], [t - .02, dict(x=0)], [t + .02, dict(x=0)], [t + dur / 2, dict(x=-2900)]]
    return d

def bar(x, y, w, h, frac, t0, color='teal', label='', **k):
    """Animated progress/bar (paper strip growing from left)."""
    inner = (f'<div class="fill sh"><div class="fill" style="background:#151515;border:5px solid #efe8d6"></div>'
             f'<div style="position:absolute;left:8px;top:8px;bottom:8px;width:{int((w - 16) * frac)}px;background:{COL.get(color, color)}" data-w="{t0 + .3:.3f}" data-wd="1.1"></div></div>')
    return el(inner, x, y, w, h, t0=t0, **k)

def arrow(x1, y1, x2, y2, t0, c='#efe8d6', sw=9, **k):
    x0, y0 = min(x1, x2) - 30, min(y1, y2) - 30; w, h = abs(x2 - x1) + 60, abs(y2 - y1) + 60
    ang = math.atan2(y2 - y1, x2 - x1); ah = 26
    hx = [(x2 - x0 - ah * math.cos(ang - .5), y2 - y0 - ah * math.sin(ang - .5)), (x2 - x0, y2 - y0), (x2 - x0 - ah * math.cos(ang + .5), y2 - y0 - ah * math.sin(ang + .5))]
    body = (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path class="dr" pathLength="1" d="M{x1 - x0} {y1 - y0}L{x2 - x0} {y2 - y0}M{hx[0][0]} {hx[0][1]}L{hx[1][0]} {hx[1][1]}L{hx[2][0]} {hx[2][1]}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return el(body, x0 + w / 2, y0 + h / 2, w, h, t0=t0, **{'in': 'draw', 'dd': .5, 'din': .05, **k})

def tabrow(text, x, y, t0, **k):
    w = int(len(text) * 22 + 120)
    return el(f'<div class="fill sh"><div class="arrowtab c" style="height:100%">{text}</div></div>', x, y, w, 64, t0=t0, **{'in': 'slide', 'id': 'l', **k})

def spec_json(path='spec.json'):
    EL.sort(key=lambda e: (e['t0'], e['z']))
    json.dump(dict(els=EL, dur=DUR), open(os.path.join(HERE, path), 'w'))
    return len(EL)
