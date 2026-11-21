"""v3 renderer. Usage: python3 render3.py bootstrap | cards | scenes | concat
bootstrap: record signatures of existing v2 scenes so unchanged scenes are not re-rendered.
Scenes re-render only if their signature (segment spec + card/stage/pop images + source) changed."""
import sys, os, subprocess, json, hashlib, copy
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/project')
import cards, edl
P = '/home/claude/project'; V = P + '/assets/video/'
FILES = dict(RDR2=V+'rdr2_horse_30fps.mp4', WANTED=V+'gta6_gameplay_airbase_jet.mp4', DOG=V+'gta6_dog_jetski.mp4', TREE=V+'gta6_bigfoot_forest.mp4', G5=V+'gta5_gameplay_trailer.mp4')
TR = [(V+'trailer_launch.mp4', 20.6, 62.0), (V+'trailer_launch.mp4', 2.0, 14.3), (V+'trailer_preload.mp4', 2.0, 14.0)]
FPS = 30
W, H = 1920, 1080

def prep(seg):
    seg.sort(key=lambda x: x['t0'])
    for g in seg:
        g['f0'], g['f1'] = round(g['t0'] * FPS), round(g['t1'] * FPS); g['n'] = g['f1'] - g['f0']
def assign_T(seg):
    ri, cur, out = 0, TR[0][1], {}
    for g in seg:
        if g['base'] and g['base'][0] == 'T':
            d = g['n'] / FPS
            while True:
                f, a, b = TR[ri % 3]
                if cur < a: cur = a
                if cur + d <= b: break
                ri += 1; cur = TR[ri % 3][1]
            out[round(g['t0'], 3)] = (TR[ri % 3][0], round(cur, 3)); cur += d
    return out

V2 = copy.deepcopy(edl.SEG); prep(V2); T2 = assign_T(V2)   # v2 footage assignment (kept stable)
BOOT = len(sys.argv) > 1 and sys.argv[1] == 'bootstrap'
if BOOT:
    SEG = V2
else:
    import edl_v3
    SEG = edl.SEG; prep(SEG)
for g in SEG:
    b = g['base']
    if b and b[0] == 'T': g['src'] = T2[round(g['t0'], 3)]
    elif b and b[0] == 'F': g['src'] = (FILES[b[1]], b[2])

def cardpath(i): return f'{P}/cards/{i:03d}.png'
def scenepath(i): return f'{P}/scenes/{i:03d}.mp4'
def stagepath(i): return f'{P}/cards/stage_{i:03d}.jpg'
def poppath(i, k): return f'{P}/cards/pop_{i:03d}_{k}.png'
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '30', '-an']

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else '-'
def sig(i, g):
    h = hashlib.md5(json.dumps({k: g[k] for k in ('f0', 'n', 'base', 'src') if k in g}, default=str).encode())
    for p in [cardpath(i), stagepath(i)] + [poppath(i, k) for k in range(len(g['card'].get('pops', [])))]: h.update(md5(p).encode())
    return h.hexdigest()

def do_cards():
    for i, g in enumerate(SEG):
        spec = dict(g['card']); b = g['base']
        pops = spec.pop('pops', [])
        if b is None: spec['bg'] = 'dark'
        else:
            spec['bg'] = 'none'
            if b[0] == 'I': spec['scrim'] = 0
            else: spec.setdefault('scrim', 120)
        cards.render(spec, cardpath(i))
        if b and b[0] == 'I':
            pth, crop, fit = edl_v3.IMG[b[1]]
            cards.stage(pth, stagepath(i), crop, fit)
        g['popsize'] = []
        for k, p in enumerate(pops):
            g['popsize'].append(cards.pop(p[2], poppath(i, k), p[3], p[4]))

def scene_cmd(i, g):
    out = scenepath(i); tmp = out[:-4] + '.part.mp4'; n = g['n']; b = g['base']
    pops = g['card'].get('pops', [])
    ins, fc = [], []
    if b is None:
        ins += ['-framerate', '30', '-loop', '1', '-i', cardpath(i)]; fc.append('[0:v]format=rgba,fade=in:0:5[b0]')
        nxt = 1
    elif b[0] == 'I':
        z0, z1, fx, fy = b[2]; N = max(n, 1)
        ins += ['-framerate', '30', '-loop', '1', '-i', stagepath(i), '-framerate', '30', '-loop', '1', '-i', cardpath(i)]
        zx = f"{z0}+({z1}-{z0})*on/{N}"
        fc.append(f"[0:v]zoompan=z='{zx}':x='max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))':d=1:s=1920x1080:fps=30,setsar=1[bz]")
        fc.append('[1:v]format=rgba,fade=in:st=0:d=0.2:alpha=1[c1];[bz][c1]overlay=0:0[b0]')
        nxt = 2
    else:
        src, ss = g['src']; blur = len(b) > 1 and b[1] == 'blur' and b[0] == 'T'
        if b[0] == 'F': ins += ['-stream_loop', '-1']
        ins += ['-ss', str(ss), '-i', src, '-framerate', '30', '-loop', '1', '-i', cardpath(i)]
        vf = 'fps=30,scale=1920:1080:flags=lanczos,setsar=1' + (',gblur=sigma=22,eq=brightness=-0.08' if blur else '')
        fc.append(f'[0:v]{vf}[bv];[1:v]format=rgba,fade=in:st=0:d=0.2:alpha=1[c1];[bv][c1]overlay=0:0[b0]')
        nxt = 2
    cur = 'b0'
    for k, p in enumerate(pops):
        ts, d, text, color, sub, pos = p
        pw, ph = g['popsize'][k] if 'popsize' in g and k < len(g['popsize']) else cards.pop(text, poppath(i, k), color, sub)
        ins += ['-framerate', '30', '-loop', '1', '-i', poppath(i, k)]
        idx = nxt + k
        right = pos in ('tr', 'br'); y = {'tr': 170, 'tl': 170, 'br': 640, 'bl': 640}[pos]
        xf = (W - pw - 80) if right else 80
        sl = f"pow(1-min(1,(t-{ts})/0.3),2)*420"
        xe = f"{xf}+{sl}" if right else f"{xf}-{sl}"
        fc.append(f"[{idx}:v]format=rgba,fade=in:st={ts}:d=0.25:alpha=1,fade=out:st={ts+d-0.25}:d=0.25:alpha=1[p{k}];[{cur}][p{k}]overlay=x='{xe}':y={y}:enable='between(t,{ts},{ts+d})'[o{k}]")
        cur = f'o{k}'
    fc.append(f'[{cur}]format=yuv420p[v]')
    return ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-frames:v', str(n)] + ENC + [tmp], tmp, out

def run_scene(ig):
    i, g = ig; out = scenepath(i); sp = out[:-4] + '.sig'; s_ = sig(i, g)
    if os.path.exists(out) and os.path.exists(sp) and open(sp).read() == s_: return i, 'skip'
    cmd, tmp, out = scene_cmd(i, g)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: return i, 'FAIL ' + r.stderr[-600:]
    os.replace(tmp, out); open(sp, 'w').write(s_); return i, 'ok'

def do_scenes(only=None):
    todo = [(i, g) for i, g in enumerate(SEG) if only is None or i in only]
    res = {'ok': 0, 'skip': 0}
    with ThreadPoolExecutor(2) as ex:
        for i, s in ex.map(run_scene, todo):
            if s in res: res[s] += 1
            else: print(i, s)
    print(res)

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'bootstrap':
        # existing v2 scenes: sig computed from v2 EDL + v2 cards (cards must be v2 pngs: run before regenerating cards)
        for i, g in enumerate(SEG):
            if os.path.exists(scenepath(i)): open(scenepath(i)[:-4] + '.sig', 'w').write(sig(i, g))
        print('bootstrapped')
    else:
        if m == 'cards': do_cards()
        if m in ('scenes',): do_cards(); do_scenes()
        if m == 'concat':
            lst = P + '/scenes/list.txt'
            open(lst, 'w').write(''.join(f"file '{scenepath(i)}'\n" for i in range(len(SEG))))
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', P + '/out/video_silent_v3.mp4'], check=True)
        json.dump([{k: v for k, v in g.items() if k != 'card'} for g in SEG], open(P + '/notes/edl_resolved_v3.json', 'w'), indent=1, default=str)
