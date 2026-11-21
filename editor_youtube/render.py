"""Usage: python3 render.py cards | scenes | final   (resumable: existing scene files are skipped)
Outputs: cards/NNN.png, scenes/NNN.mp4, out/video_silent.mp4"""
import sys, os, subprocess, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/project')
import cards, edl
P = '/home/claude/project'
V = P + '/assets/video/'
FILES = dict(RDR2=V + 'rdr2_horse_30fps.mp4', WANTED=V + 'gta6_gameplay_airbase_jet.mp4', DOG=V + 'gta6_dog_jetski.mp4', TREE=V + 'gta6_bigfoot_forest.mp4')
TR = [(V + 'trailer_launch.mp4', 20.6, 62.0), (V + 'trailer_launch.mp4', 2.0, 14.3), (V + 'trailer_preload.mp4', 2.0, 14.0)]
RUNS = [0, 1, 2]
SEG = sorted(edl.SEG, key=lambda x: x['t0'])
FPS = 30
for g in SEG:
    g['f0'], g['f1'] = round(g['t0'] * FPS), round(g['t1'] * FPS)
    g['n'] = g['f1'] - g['f0']
# trailer cursor assignment (deterministic)
ri, cur = 0, TR[0][1]
for g in SEG:
    if g['base'] and g['base'][0] == 'T':
        d = g['n'] / FPS
        while True:
            f, a, b = TR[ri % 3]
            if cur < a: cur = a
            if cur + d <= b: break
            ri += 1; cur = TR[ri % 3][1]
        g['src'] = (TR[ri % 3][0], round(cur, 3)); cur += d
    elif g['base'] and g['base'][0] == 'F':
        g['src'] = (FILES[g['base'][1]], g['base'][2])


def cardpath(i): return f'{P}/cards/{i:03d}.png'
def scenepath(i): return f'{P}/scenes/{i:03d}.mp4'
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '30', '-an']


def do_cards():
    for i, g in enumerate(SEG):
        spec = dict(g['card'])
        if g['base'] is None:
            spec['bg'] = 'dark'
        else:
            spec['bg'] = 'none'
            spec.setdefault('scrim', 120)
        cards.render(spec, cardpath(i))


def scene_cmd(i, g):
    out = scenepath(i); tmp = out[:-4] + '.part.mp4'
    n = g['n']
    if g['base'] is None:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', cardpath(i), '-vf', 'format=yuv420p,loop=-1:1:0,fade=in:0:5', '-frames:v', str(n)] + ENC + [tmp]
    else:
        src, ss = g['src']
        blur = len(g['base']) > 1 and g['base'][1] == 'blur'
        pre = ['-stream_loop', '-1'] if g['base'][0] == 'F' else []
        vf = 'fps=30,scale=1920:1080:flags=lanczos,setsar=1' + (',gblur=sigma=22,eq=brightness=-0.08' if blur else '')
        fc = f'[0:v]{vf}[b];[1:v]format=rgba,fade=in:st=0:d=0.2:alpha=1[o];[b][o]overlay=0:0,format=yuv420p[v]'
        cmd = ['ffmpeg', '-v', 'error', '-y'] + pre + ['-ss', str(ss), '-i', src, '-framerate', '30', '-loop', '1', '-i', cardpath(i), '-filter_complex', fc, '-map', '[v]', '-frames:v', str(n)] + ENC + [tmp]
    return cmd, tmp, out


def run_scene(ig):
    i, g = ig
    cmd, tmp, out = scene_cmd(i, g)
    if os.path.exists(out): return i, 'skip'
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: return i, 'FAIL ' + r.stderr[-400:]
    os.rename(tmp, out); return i, 'ok'


def do_scenes(only=None):
    todo = [(i, g) for i, g in enumerate(SEG) if only is None or i in only]
    with ThreadPoolExecutor(2) as ex:
        for i, s in ex.map(run_scene, todo):
            if s != 'ok' and s != 'skip': print(i, s)
    print('scenes done', sum(os.path.exists(scenepath(i)) for i in range(len(SEG))), '/', len(SEG))


def do_concat():
    lst = P + '/scenes/list.txt'
    open(lst, 'w').write(''.join(f"file '{scenepath(i)}'\n" for i in range(len(SEG))))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', P + '/out/video_silent.mp4'], check=True)


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'cards': do_cards()
    elif m == 'scenes': do_scenes()
    elif m == 'concat': do_concat()
    json.dump([{k: v for k, v in g.items() if k != 'card'} for g in SEG], open(P + '/notes/edl_resolved.json', 'w'), indent=1, default=str)
