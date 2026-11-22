"""v4 renderer. Usage: python3 render2.py prep|shots|concat|mix NAME [--win a-b,c-d]   (windows = sample mode; default full)"""
import sys, os, re, json, subprocess, random, math, wave
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/project'); sys.path.insert(0, '/home/claude/rockstar_video')
import cards
from plan2 import P, DUR, sents
W = '/home/claude/rockstar_video/work2'; FPS = 30
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '30', '-an']
COL = dict(teal='&HD4E027&', amber='&H20B0FF&', red='&H4B4BFF&', pink='&H8B4FFF&', violet='&HFF82A0&', ink='&HEAF1F4&', dim='&HBDB5AA&')
RGB = dict(teal=(39, 224, 212), amber=(255, 176, 32), red=(255, 75, 75), pink=(255, 79, 139), violet=(160, 130, 255), ink=(244, 241, 234))
STATUSCOL = {'CONFIRMED': 'teal', 'REPORTED': 'amber', 'ANALYSIS': 'violet', 'UNION CLAIM': 'amber', 'CLAIM': 'amber', 'ROCKSTAR RESPONSE': 'teal', 'DISPUTED': 'red', 'OPINION': 'violet', 'CONTEXT': 'dim'}
for p in P:
    p['f0'] = round(p['t'] * FPS); p['f1'] = round(p['end'] * FPS); p['n'] = p['f1'] - p['f0']
CW, CH = 2880, 1620

def prep(p):
    out = f"{W}/prep/{p['id']:03d}.png"
    if os.path.exists(out): return
    k = p['kind']
    if k == 'still':
        im = Image.open(p['img']).convert('RGB')
        if abs(im.width / im.height - 16 / 9) < 0.02: im.resize((CW, CH), Image.LANCZOS).save(out)
        else: cards.stage(p['img'], out, fit=0.9, canvas=(CW, CH), maxup=2.0)
    elif k == 'paper':
        pg = Image.open(N_PATH[p['key']]).convert('RGB')
        bg = pg.resize((CW // 4, CH // 4)).filter(ImageFilter.GaussianBlur(10)).resize((CW, CH), Image.BICUBIC).point(lambda v: int(v * 0.30))
        sc = 0.92; pw, ph = int(CW * sc), int(CH * sc); panel = pg.resize((pw, ph), Image.LANCZOS).point(lambda v: int(v * 0.93))
        if p.get('hl'):
            x, y, w, h = p['hl']; ov = Image.new('RGBA', panel.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            d.rounded_rectangle((x * pw, y * ph, (x + w) * pw, (y + h) * ph), 14, fill=(255, 214, 0, 70), outline=(255, 214, 0, 190), width=5)
            panel = Image.alpha_composite(panel.convert('RGBA'), ov).convert('RGB')
        x0, y0 = (CW - pw) // 2, (CH - ph) // 2
        sh = Image.new('RGBA', (pw + 200, ph + 200), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((100, 120, pw + 100, ph + 120), fill=(0, 0, 0, 220)); sh = sh.filter(ImageFilter.GaussianBlur(40))
        bg = bg.convert('RGBA'); bg.alpha_composite(sh, (x0 - 100, y0 - 100)); bg = bg.convert('RGB'); bg.paste(panel, (x0, y0)); bg.save(out)
    elif k == 'kin':
        base = cards.bgimg().resize((CW, CH), Image.LANCZOS); r, g, b = RGB[p['tint']]
        tint = Image.new('RGB', (CW, CH), (r // 5, g // 5, b // 5)); base = Image.blend(base, tint, 0.45)
        d = ImageDraw.Draw(base, 'RGBA'); rnd = random.Random(p['id'])
        for _ in range(7):  # soft light bars for depth
            x = rnd.randint(0, CW); d.rectangle((x, 0, x + rnd.randint(8, 30), CH), fill=(r, g, b, 14))
        base.filter(ImageFilter.GaussianBlur(3)).save(out)
N_PATH = __import__('plan2').N

def box_expr(b0, b1, n):
    cx0, cy0, s0 = b0; cx1, cy1, s1 = b1; N1 = max(1, n - 1)
    E = f"(st(0,min(1,on/{N1}))*0+ld(0)*ld(0)*(3-2*ld(0)))"
    lerp = lambda a, b: f"({a}+({b}-({a}))*{E})"
    S, CX, CY = lerp(s0, s1), lerp(cx0, cx1), lerp(cy0, cy1)
    punch = "(1+0.055*max(0,1-on/7))"
    z = f"{punch}/({S})"
    return z, f"({CX})*iw-iw/zoom/2", f"({CY})*ih-ih/zoom/2"

GRADE = "eq=contrast=1.05:saturation=1.10,vignette=angle=PI/5.5,format=yuv420p"
def tail(p):
    tr = p.get('tr', 'cut')
    if tr == 'dip': return ',fade=t=in:st=0:d=0.12'
    if tr == 'flash': return ',fade=t=in:st=0:d=0.10:color=white'
    return ''

def cmd(p):
    n = p['n']; out = f"{W}/shots/{p['id']:03d}.mp4"; tmp = out[:-4] + '.part.mp4'; k = p['kind']
    if k == 'clip':
        s0, s1 = p['z']; cx, cy = p['c']
        z, x, y = box_expr((cx, cy, s0), (cx, cy, s1), n)
        vf = f"fps=30,scale=2400:1350:flags=lanczos,unsharp=5:5:0.7,zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1920x1080:fps=30,{GRADE}{tail(p)}"
        c = ['ffmpeg', '-v', 'error', '-y', '-ss', str(p['ss']), '-t', f"{n / FPS + 0.3:.3f}", '-i', p['src'], '-vf', vf, '-frames:v', str(n)] + ENC + [tmp]
    else:
        z, x, y = box_expr(p['b0'], p['b1'], n) if k != 'kin' else box_expr((.5, .5, 1), (.46, .5, .86), n)
        vf = f"scale={CW}:{CH},zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1920x1080:fps=30,{GRADE}{tail(p)}"
        c = ['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-loop', '1', '-i', f"{W}/prep/{p['id']:03d}.png", '-vf', vf, '-frames:v', str(n)] + ENC + [tmp]
    return c, tmp, out

def run(i):
    c, tmp, out = cmd(P[i])
    if os.path.exists(out): return i, 'skip'
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: return i, 'FAIL ' + r.stderr[-400:]
    os.rename(tmp, out); return i, 'ok'

# ---------------- timeline selection (sample windows)
def windows(arg):
    if not arg: return [(0.0, DUR)]
    return sorted(tuple(float(x) for x in w.split('-')) for w in arg.split(','))
def in_win(t0, t1, wins): return any(t0 >= a - 0.01 and t1 <= b + 0.01 for a, b in wins)
def remap(t, wins):
    off = 0.0
    for a, b in wins:
        if a - 0.01 <= t <= b + 0.01: return off + (t - a)
        off += b - a
    return None

# ---------------- ASS overlays
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); return f'{h}:{m:02d}:{t%60:05.2f}'
def esc(s): return s.replace('{', '(').replace('}', ')')
def ass(wins, path):
    ev = []
    HDR = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2', '', '[V4+ Styles]',
           'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
           'Style: Cap,Inter Display,56,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,5,2,2,120,120,74,1',
           'Style: Big,Inter Display,118,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,7,3,8,100,100,95,1',
           'Style: Chip,Inter,27,&H00FFFFFF,&H000000FF,&H99101010,&H00000000,1,0,0,0,100,100,0,0,3,11,0,7,64,64,60,1', '', '[Events]',
           'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
    def E(layer, a, b, style, text, extra=''):
        ra, rb = remap(a, wins), remap(b, wins)
        if ra is None or rb is None or rb <= ra: return
        ev.append((ra, f'Dialogue: {layer},{ts(ra)},{ts(rb)},{style},,0,0,0,,{extra}{text}'))
    for p in P:
        if not in_win(p['t'], p['end'], wins): continue
        t0, t1 = p['t'], p['end']
        if p.get('status'):
            c = COL[STATUSCOL.get(p['status'], 'dim')]
            E(2, t0 + 0.05, t1, 'Chip', esc(p['status']), r'{\an1\pos(64,848)\3c' + c + r'\c&H101010&\fad(160,120)}')
        if p.get('credit'):
            E(2, t0 + 0.05, t1, 'Chip', esc(p['credit']), r'{\an1\pos(64,905)\fs24\fad(160,120)}')
        for co in p.get('co', []):
            a, b = t0 + co['a'], min(t0 + co['a'] + co['d'], t1 + (0.0 if not co.get('carry') else 3)); c = COL[co['c']]
            if co['k'] == 'big':
                big_sz = 118 if len(co['l1']) < 18 else (96 if len(co['l1']) < 30 else 74)
                txt = r'{\fs%d\c%s}%s' % (big_sz, c, esc(co['l1']))
                if co.get('l2'): txt += r'\N{\fs46\c&H00FFFFFF&\bord4}' + esc(co['l2'])
                E(3, a, b, 'Big', txt, r'{\an8\pos(960,%d)\fad(110,220)\fscx72\fscy72\t(0,170,\fscx100\fscy100)\blur0.6}' % (92 if big_sz >= 96 else 100))
            elif co['k'] == 'word':
                E(3, a, b, 'Big', r'{\fs210\c%s}%s' % (c, esc(co['l1'])), r'{\an5\pos(960,470)\fad(60,140)\fscx60\fscy60\t(0,140,\fscx100\fscy100)\bord9}')
            elif co['k'] == 'quote':
                E(3, a, b, 'Big', r'{\fs58\c&H00FFFFFF&}%s\N{\fs34\c%s}— %s' % (esc(co['l1']), c, esc(co['l2'])), r'{\an2\pos(960,885)\fad(140,200)\bord6\fscx92\fscy92\t(0,190,\fscx100\fscy100)}')
    # captions with word highlight
    words = json.load(open('/home/claude/rockstar_video/words.json')); wi = 0
    pe = 0.0
    for w in words:
        w['s'] = max(w['s'], pe); w['e'] = max(w['e'], w['s'] + 0.09); pe = w['e']
    for si, s in enumerate(sents):
        disp = s['text'].split(); toks = [w for w in words if w['sent'] == si]; ti = 0; items = []
        for d in disp:
            nt = max(1, len(re.findall(r"[a-z0-9']+", d.lower()))); seg = toks[ti:ti + nt] or toks[-1:]; ti += nt
            items.append((d, seg[0]['s'], seg[-1]['e']))
        chunks, cur = [], []
        for it in items:
            cur.append(it)
            if len(cur) >= 6 or (len(cur) >= 3 and it[0][-1] in ',;:.?!'): chunks.append(cur); cur = []
        if cur:
            if chunks and len(cur) < 3: chunks[-1] += cur
            else: chunks.append(cur)
        for ci, ch in enumerate(chunks):
            for k, (wd, a, b) in enumerate(ch):
                b2 = ch[k + 1][1] if k + 1 < len(ch) else (chunks[ci + 1][0][1] if ci + 1 < len(chunks) else b + 0.25)
                b2 = max(b2, a + 0.12)
                line = ' '.join((r'{\c&H00D7FF&\fscx108\fscy108}' + esc(w) + r'{\c&H00FFFFFF&\fscx100\fscy100}') if j == k else esc(w) for j, (w, _, _) in enumerate(ch))
                E(5, a, b2, 'Cap', line)
    ev.sort(key=lambda e: e[0])
    open(path, 'w').write('\n'.join(HDR + [e[1] for e in ev]) + '\n')

# ---------------- sound: soft whooshes on transitions/callouts
def sfx(wins, path):
    sr = 44100; total = sum(b - a for a, b in wins); n = int(sr * (total + 1)); L = np.zeros(n); rng = np.random.default_rng(5)
    def whoosh(t, amp=0.10, dur=0.45):
        a = int(t * sr); m = int(dur * sr); tt = np.arange(m) / sr; nz = rng.standard_normal(m)
        k = np.convolve(nz, np.ones(40) / 40, 'same') * np.sin(np.pi * tt / dur) ** 2 * amp
        e = min(m, n - a); L[a:a + e] += k[:e]
    def tick(t, amp=0.07):
        a = int(t * sr); m = int(0.18 * sr); tt = np.arange(m) / sr; s = np.sin(2 * np.pi * (760 + 600 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 22) * amp
        e = min(m, n - a); L[a:a + e] += s[:e]
    for p in P:
        if not in_win(p['t'], p['end'], wins): continue
        rt = remap(p['t'], wins)
        if p.get('tr') in ('dip', 'flash'): whoosh(max(0, rt - 0.12))
        for co in p.get('co', []):
            r = remap(p['t'] + co['a'], wins)
            if r is not None and co['k'] in ('big', 'word', 'quote'): tick(r)
    L = np.clip(L, -1, 1); x = (np.stack([L, L], 1) * 32767).astype('<i2')
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes()); w.close()

def build(name, wins, wintag):
    sel = [p for p in P if in_win(p['t'], p['end'], wins)]
    open(f'{W}/list_{wintag}.txt', 'w').write(''.join(f"file '{W}/shots/{p['id']:03d}.mp4'\n" for p in sel))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{W}/list_{wintag}.txt', '-c', 'copy', f'{W}/silent_{wintag}.mp4'], check=True)
    ass(wins, f'{W}/subs_{wintag}.ass'); sfx(wins, f'{W}/sfx_{wintag}.wav')
    R = '/home/claude/rockstar_video'
    # audio: voice + music windows (concatenated), then mix
    vparts = ''.join(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[v{i}];[2:a]atrim={a}:{b},asetpts=PTS-STARTPTS[m{i}];" for i, (a, b) in enumerate(wins))
    vc = ''.join(f'[v{i}]' for i in range(len(wins))) + f'concat=n={len(wins)}:v=0:a=1[voice];'
    mc = ''.join(f'[m{i}]' for i in range(len(wins))) + f'concat=n={len(wins)}:v=0:a=1[music];'
    fc = (f"[0:v]subtitles={W}/subs_{wintag}.ass:fontsdir=/usr/share/fonts/opentype/inter[v];" + vparts + vc + mc +
          "[music]volume=0.40[mu];[3:a]volume=0.9[fx];[voice][mu][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.85,volume=0.85[a]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{W}/silent_{wintag}.mp4', '-i', R + '/work/voice_norm.wav', '-i', R + '/work/music.wav', '-i', f'{W}/sfx_{wintag}.wav', '-filter_complex', fc,
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', R + '/out/' + name], check=True)

if __name__ == '__main__':
    m = sys.argv[1]; args = sys.argv[2:]
    wins = windows(next((a.split('=')[1] for a in args if a.startswith('--win=')), None))
    sel = [i for i, p in enumerate(P) if in_win(p['t'], p['end'], wins)]
    if m == 'prep':
        for i in sel: prep(P[i])
    elif m == 'shots':
        with ThreadPoolExecutor(3) as ex:
            for i, s in ex.map(run, sel):
                if s not in ('ok', 'skip'): print(i, s)
        print('shots', sum(os.path.exists(f"{W}/shots/{P[i]['id']:03d}.mp4") for i in sel), '/', len(sel))
    elif m == 'mix': build(args[0], wins, args[1])
