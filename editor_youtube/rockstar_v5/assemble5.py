"""python3 assemble5.py NAME [a-b,c-d,...]   (no windows = full video)"""
import sys, os, json, subprocess, numpy as np, wave
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000
spec = json.load(open('spec.json')); DUR = spec['dur']
def tone(f0, f1, d, amp=1.0, decay=8):
    n = int(SR * d); t = np.arange(n) / SR; f = f0 + (f1 - f0) * t / d
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-decay * t)
def noise(d, lo, hi, amp=1.0, decay=6, seed=1):
    n = int(SR * d); r = np.random.default_rng(seed).normal(0, 1, n)
    F = np.fft.rfft(r); fr = np.fft.rfftfreq(n, 1 / SR); F[(fr < lo) | (fr > hi)] = 0
    x = np.fft.irfft(F, n); x /= (np.abs(x).max() + 1e-9); t = np.arange(n) / SR
    return amp * x * np.exp(-decay * t)
def sweepn(d, a, b, amp=.8):
    x = noise(d, 300, 6000, 1, 0, 5); t = np.arange(len(x)) / SR
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    return amp * x * env
def mixs(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
SFX = {
 'pop': lambda: mixs(.5 * tone(520, 880, .09, 1, 28), .25 * noise(.05, 1500, 5000, 1, 60)),
 'whoosh': lambda: sweepn(.32, 0, 0, .55),
 'stamp': lambda: mixs(tone(110, 55, .28, 1, 11), .6 * noise(.08, 300, 3000, 1, 40)),
 'drop': lambda: mixs(tone(150, 60, .22, .9, 12), .35 * noise(.06, 200, 2500, 1, 50)),
 'sweep': lambda: sweepn(.75, 0, 0, .9),
 'flip': lambda: mixs(sweepn(.25, 0, 0, .45), .2 * tone(700, 300, .12, 1, 25)),
}
MAP = {'pop': 'pop', 'slide': 'whoosh', 'stamp': 'stamp', 'drop': 'drop', 'flip': 'flip', 'zoom': 'whoosh', 'grow': 'pop'}
def make_sfx(path):
    out = np.zeros(int((DUR + 3) * SR)); cache = {}
    last = {}
    for e in spec['els']:
        k = 'sweep' if e.get('z') == 2000 else MAP.get(e.get('in', 'pop'))
        if not k: continue
        t0 = e['t0']
        if last.get(k, -9) > t0 - 0.06: continue   # avoid machine-gun
        last[k] = t0
        if k not in cache: cache[k] = SFX[k]()
        s = int(t0 * SR); x = cache[k] * (.55 if k in ('pop', 'whoosh') else .8)
        out[s:s + len(x)] += x[:len(out) - s]
    out /= max(1, np.abs(out).max()) * 1.0
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767 * .9).astype('<i2').tobytes())
def pieces(wins):
    if wins is None:
        a = 0; P = []
        while a < DUR - .01: P.append((a, min(a + 15, round(DUR, 2)))); a += 15
        return P
    return wins
def render_piece(ab):
    a, b = ab; f = f'chunks/{a:.2f}_{b:.2f}.mp4'
    if os.path.exists(f): return f
    os.makedirs('chunks', exist_ok=True)
    subprocess.run(['python3', 'render5.py', 'frames', str(a), str(b), f], check=True, stdout=subprocess.DEVNULL)
    return f
if __name__ == '__main__':
    name = sys.argv[1]
    wins = None if len(sys.argv) < 3 else [tuple(float(x) for x in w.split('-')) for w in sys.argv[2].split(',')]
    P = pieces(wins)
    if not os.path.exists('sfx.wav') or os.path.getmtime('sfx.wav') < os.path.getmtime('spec.json'): make_sfx('sfx.wav')
    with ThreadPoolExecutor(2) as ex: files = list(ex.map(render_piece, P))
    open('concat.txt', 'w').write(''.join(f"file '{os.path.abspath(f)}'\n" for f in files))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'tmp_video.mp4'], check=True)
    # audio: voice + music + sfx, trimmed to the same windows
    W = wins or [(0, DUR)]
    segs = ''.join(f'[a{i}]' for i in range(len(W)))
    trims = ';'.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[v{i}];[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[m{i}];[2:a]atrim={a}:{b},asetpts=PTS-STARTPTS[s{i}];[v{i}][m{i}][s{i}]amix=inputs=3:weights=1 .32 .55:normalize=0:duration=first[a{i}]' for i, (a, b) in enumerate(W))
    fc = trims + f';{segs}concat=n={len(W)}:v=0:a=1,alimiter=limit=0.9[aout]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '../work/voice_norm.wav', '-i', '../work/music.wav', '-i', 'sfx.wav', '-i', 'tmp_video.mp4', '-filter_complex', fc,
                    '-map', '3:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', f'../out/{name}'], check=True)
    print('done', name)
