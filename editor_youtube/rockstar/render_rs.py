"""Rockstar video renderer (reuses the existing editor's cards.py). Usage: python3 render_rs.py cards|scenes|concat|mix"""
import sys, os, json, subprocess, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/project'); sys.path.insert(0, '/home/claude/rockstar_video')
import cards
cards.STATUS.update({'ROCKSTAR RESPONSE': 'teal', 'UNION CLAIM': 'amber', 'CLAIM': 'amber', 'DISPUTED': 'red'})
from scenes_def import S
P = '/home/claude/rockstar_video'; FPS = 30
sents = json.load(open(P + '/sents.json')); sil = json.load(open(P + '/audio/sil.json'))
DUR = 293.25
def snap(t):
    best = min(((abs((a + b) / 2 - t), (a + b) / 2) for a, b in sil), default=(9, t))
    return best[1] if best[0] <= 0.6 else t
starts = [0.0] + [snap(sents[s[0]]['start']) for s in S[1:]]
ends = starts[1:] + [DUR]
FR = [round(e * FPS) for e in ends]; F0 = [0] + FR[:-1]
N = [b - a for a, b in zip(F0, FR)]
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-g', '30', '-an']
def cp(i, k): return f'{P}/cards/{i:02d}_{k}.png'
def sp(i): return f'{P}/scenes/{i:02d}.mp4'

def do_cards():
    for i, (s0, kind, d, pops) in enumerate(S):
        deco = dict(bg='none', scrim=0, status=d.get('status'), credit=d.get('credit'), tag=d.get('tag'), kicker=d.get('kicker'))
        cards.render(deco, cp(i, 'deco'))
        if kind == 'card':
            cards.render(dict(bg='dark', blocks=d['blocks'], maxw=1500, y=None) if False else dict(bg='dark', blocks=d['blocks'], maxw=1500, **({} )), cp(i, 'base'))
        elif kind == 'still':
            cards.stage(d['img'], cp(i, 'base'), crop=d.get('crop'), fit=0.86)
        for j, (ts, text, col, sub, dur) in enumerate(pops):
            cards.pop(text, cp(i, f'pop{j}'), col, sub, 46)

def cmd(i):
    s0, kind, d, pops = S[i]; n = N[i]; sec = n / FPS; out = sp(i); tmp = out[:-4] + '.part.mp4'
    ins, fc = [], []
    if kind == 'foot':
        ins += ['-ss', str(d['ss']), '-t', f'{sec+0.2:.3f}', '-i', d['src']]
        fc.append('[0:v]fps=30,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p[b]')
    else:
        ins += ['-framerate', '30', '-loop', '1', '-i', cp(i, 'base')]
        fc.append(f"[0:v]scale=2880:1620,zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,format=yuv420p[b]")
    ins += ['-framerate', '30', '-loop', '1', '-i', cp(i, 'deco')]
    fc.append('[1:v]format=rgba,fade=in:st=0:d=0.25:alpha=1[dc];[b][dc]overlay=0:0[v1]')
    last = 'v1'
    for j, (ts, text, col, sub, dur) in enumerate(pops):
        ins += ['-framerate', '30', '-loop', '1', '-i', cp(i, f'pop{j}')]
        k = j + 2; te = ts + dur
        fc.append(f"[{last}][{k}:v]overlay=x='W-w-60+pow(1-min(1,(t-{ts})/0.3),2)*560':y=200:enable='between(t,{ts},{te})':format=auto[v{j+2}]")
        last = f'v{j+2}'
    return ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-frames:v', str(n)] + ENC + [tmp], tmp, out

def run(i):
    c, tmp, out = cmd(i)
    if os.path.exists(out): return i, 'skip'
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: return i, 'FAIL ' + r.stderr[-500:]
    os.rename(tmp, out); return i, 'ok'

def do_scenes(only=None):
    todo = [i for i in range(len(S)) if only is None or i in only]
    with ThreadPoolExecutor(3) as ex:
        for i, s in ex.map(run, todo):
            if s not in ('ok', 'skip'): print(i, s)
    print('scenes', sum(os.path.exists(sp(i)) for i in range(len(S))), '/', len(S))

def do_concat():
    open(P + '/scenes/list.txt', 'w').write(''.join(f"file '{sp(i)}'\n" for i in range(len(S))))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', P + '/scenes/list.txt', '-c', 'copy', P + '/out/video_silent.mp4'], check=True)

def ass():
    def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); return f'{h}:{m:02d}:{t%60:05.2f}'
    out = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', '', '[V4+ Styles]',
           'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
           'Style: D,Inter Display,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,1,2,160,160,132,1', '', '[Events]',
           'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
    for k, s in enumerate(sents):
        t0 = s['start']; t1 = min(s['end'], sents[k + 1]['start'] - 0.02) if k + 1 < len(sents) else DUR
        t1 = max(t1, t0 + 0.4)
        words = s['text'].replace('\n', ' ').split()
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= 7 or (len(cur) >= 4 and w[-1] in ',;:'): chunks.append(cur); cur = []
        if cur:
            if chunks and len(cur) < 3: chunks[-1] += cur
            else: chunks.append(cur)
        tot = sum(len(' '.join(c)) for c in chunks); a = t0
        for c in chunks:
            b = a + (t1 - t0) * len(' '.join(c)) / tot
            out.append(f'Dialogue: 0,{ts(a)},{ts(b)},D,,0,0,0,,{" ".join(c)}'); a = b
    open(P + '/work/subs.ass', 'w').write('\n'.join(out) + '\n')

def do_mix(name):
    ass()
    v = P + '/work/voice_norm.wav'
    if not os.path.exists(v):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P + '/audio/narration.mp3', '-af', 'aformat=sample_rates=44100:channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=9', v], check=True)
    fc = "[0:v]subtitles=work/subs.ass:fontsdir=/usr/share/fonts/opentype/inter[v];[2:a]volume=0.40[m];[1:a][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85,volume=0.85[a]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P + '/out/video_silent.mp4', '-i', v, '-i', P + '/work/music.wav', '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', P + '/out/' + name], check=True, cwd=P)

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'cards': do_cards()
    elif m == 'scenes': do_scenes([int(x) for x in sys.argv[2:]] or None)
    elif m == 'concat': do_concat()
    elif m == 'mix': do_mix(sys.argv[2])
    elif m == 'info':
        for i in range(len(S)): print(i, S[i][1], round(starts[i], 2), N[i], round(N[i] / 30, 2))
