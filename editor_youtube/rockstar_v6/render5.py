"""Frame renderer: python3 render5.py frames T0 T1 OUTPREFIX  |  test T... """
import sys, json, os, subprocess, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
def open_page(p):
    b = p.chromium.launch(args=['--font-render-hinting=none', '--disable-lcd-text', '--force-device-scale-factor=1', '--allow-file-access-from-files', '--disable-web-security'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file://' + HERE + '/engine.html')
    spec = open(HERE + '/spec.json').read()
    pg.evaluate(f'build({spec})')
    return b, pg
def shot_frames(a, b_, out_mp4):
    """render frames [a,b_) seconds into one h264 file (no audio)."""
    n0, n1 = int(round(a * FPS)), int(round(b_ * FPS))
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), out_mp4 + '.tmp.mp4'], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = open_page(p)
        t_start = time.time()
        for n in range(n0, n1):
            pg.evaluate(f'draw({n / FPS:.4f})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
            if (n - n0) % 60 == 59: print(f'{a}-{b_}: {n - n0 + 1}/{n1 - n0} frames, {(time.time() - t_start) / (n - n0 + 1):.2f}s/frame', flush=True)
        b.close()
    ff.stdin.close(); ff.wait(); os.rename(out_mp4 + '.tmp.mp4', out_mp4)
def still(ts, outdir):
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b, pg = open_page(p)
        for t in ts:
            pg.evaluate(f'draw({t})'); pg.screenshot(path=f'{outdir}/{t:07.2f}.png'); 
        b.close()
if __name__ == '__main__':
    if sys.argv[1] == 'still': still([float(x) for x in sys.argv[3:]], sys.argv[2])
    elif sys.argv[1] == 'frames': shot_frames(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
