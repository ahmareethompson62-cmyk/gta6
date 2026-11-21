"""Original synthesized ambient bed + accents (no third-party music). Output out/music.wav (44.1k stereo)."""
import numpy as np, wave, json
sr = 44100; D = 514.2; n = int(sr * D); t = np.arange(n) / sr
rng = np.random.default_rng(6)
S = json.load(open('/home/claude/project/notes/sents.json'))
def s(i): return S[i]['start']
chords = [[57,60,64],[53,57,60],[55,59,62],[52,55,59]]  # Am F G Em (MIDI)
def f(m): return 440 * 2 ** ((m - 69) / 12)
L = np.zeros(n); R = np.zeros(n)
per = 12.0
for k in range(int(D / per) + 1):
    ch = chords[k % 4]; a = int(k * per * sr); b = min(n, int((k + 1) * per * sr + 3 * sr))
    tt = t[a:b] - k * per
    env = np.clip(tt / 4, 0, 1) * np.clip((per + 3 - tt) / 4, 0, 1)
    for j, m in enumerate(ch):
        for det, pan in [(-0.4, 0.3), (0.4, 0.7)]:
            fr = f(m - 12) * 2 ** (det / 1200 * 5)
            sig = (np.sin(2 * np.pi * fr * tt) + .35 * np.sin(2 * np.pi * 2 * fr * tt + j)) * env * 0.05
            L[a:b] += sig * (1 - pan); R[a:b] += sig * pan
    sub = np.sin(2 * np.pi * f(ch[0] - 24) * tt) * env * 0.09
    L[a:b] += sub; R[a:b] += sub
# slow tremolo pulse
lfo = .85 + .15 * np.sin(2 * np.pi * t / 7.5); L *= lfo; R *= lfo
def hit(at, amp=1.0, low=48):
    a = int(at * sr); m = int(2.2 * sr); tt = np.arange(m) / sr
    h = np.sin(2 * np.pi * (f(low) * (1 + 1.5 * np.exp(-tt * 9))) * tt) * np.exp(-tt * 2.4) * amp * .45
    nz = rng.standard_normal(m) * np.exp(-tt * 18) * amp * .05
    sg = h + nz; e = min(n - a, m); L[a:a+e] += sg[:e]; R[a:a+e] += sg[:e]
for at in [s(21), s(22), s(38), s(56), s(71), s(86), s(99), s(118), s(128), s(144)]: hit(at, 1.0)
for i in range(149, 155): hit(s(i), .6, 55)
for i in [155, 156, 157]: hit(s(i), .5, 50)
# gain automation: base, duck dips, silences
g = np.ones(n) * 0.9
def ramp(t0, t1, v, fi=.6, fo=1.2):
    a, b = int(t0 * sr), int(t1 * sr)
    g[max(0, a - int(fi * sr)):a] = np.minimum(g[max(0, a - int(fi * sr)):a], np.linspace(g[a - 1], v, len(g[max(0, a - int(fi * sr)):a])))
    g[a:b] = np.minimum(g[a:b], v)
    e = min(n, b + int(fo * sr)); g[b:e] = np.minimum(g[b:e], np.linspace(v, 1, e - b) * 0 + np.linspace(v, 0.9, e - b))
ramp(24.0, 28.36, 0.0, .5, 1.5)        # silence on the 'code already used' reveal
ramp(283.4, 286.0, 0.3, .5, .6)        # 'later' dip
ramp(491.3, 497.0, 0.0, .8, 2.5)       # 5 s silence before easter eggs
ramp(0, 3, 0.5, 0.01, 2.0)
fade = np.clip((D - t) / 4, 0, 1); g *= fade
L *= g; R *= g
m = np.stack([L, R], 1); m = m / np.abs(m).max() * 0.8
w = wave.open('/home/claude/project/out/music.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((m * 32767).astype('<i2').tobytes()); w.close(); print('music ok')
