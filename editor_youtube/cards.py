"""Card renderer for GTA6 documentary. All cards are original typeset graphics (no third-party designs).
spec keys: bg ('dark'|'none'), scrim (0-255 alpha when bg none), blocks[], chip (source label), status (stamp tag top-left),
credit (bottom-right pill), tag (bottom-left chapter chip)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
F = '/usr/share/fonts/opentype/inter/Inter'
FD = '/usr/share/fonts/opentype/inter/InterDisplay'
W, H = 1920, 1080
COL = dict(ink=(244, 241, 234), dim=(170, 170, 182), pink=(255, 79, 139), teal=(39, 224, 212),
           amber=(255, 176, 32), red=(255, 75, 75), violet=(160, 130, 255), green=(90, 220, 130), bg=(10, 11, 16))
STATUS = {'CONFIRMED': 'teal', 'REPORTED': 'amber', 'NOT CONFIRMED': 'amber', 'RUMOUR': 'red', 'ANALYSIS': 'violet',
          'PREDICTION': 'violet', 'EXPLANATORY GRAPHIC': 'dim', 'LOW-RELIABILITY': 'red', 'PRE-LAUNCH CLAIM': 'violet',
          'CONTEXT': 'dim', 'NOT IN REVIEWS': 'dim'}
_fc = {}


def font(w, s, disp=True):
    k = (w, s, disp)
    if k not in _fc:
        _fc[k] = ImageFont.truetype((FD if disp else F) + '-' + w + '.otf', s)
    return _fc[k]


def col(c):
    return COL.get(c, c) if isinstance(c, str) else c


def bgimg():
    im = Image.new('RGB', (W, H), COL['bg'])
    px = ImageDraw.Draw(im)
    # soft vice-city glow bottom
    g = Image.new('RGB', (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse((-300, 700, 1000, 1500), fill=(70, 18, 60))
    gd.ellipse((900, 800, 2300, 1600), fill=(10, 60, 70))
    g = g.filter(ImageFilter.GaussianBlur(160))
    return Image.blend(im, Image.eval(g, lambda v: v), 0.0) if False else Image.composite(g, im, Image.new('L', (W, H), 255)).point(lambda v: min(255, v)) if False else Image.fromarray(__import__('numpy').clip(__import__('numpy').asarray(im).astype(int) + __import__('numpy').asarray(g).astype(int), 0, 255).astype('uint8'))


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def block_h(d, b, maxw):
    k = b[0]
    if k == 'gap':
        return b[1]
    if k == 'text':
        _, s, size, wt, c = b[:5]
        f = font(wt, size)
        return len(wrap(d, s, f, maxw)) * int(size * 1.12)
    if k == 'stamp':
        return int(b[2] * 1.5) if len(b) > 2 else 90
    if k == 'rows':
        return len(b[1]) * b[2]
    if k == 'cols':
        return max(sum(block_h(d, x, maxw // 2 - 40) for x in b[1]), sum(block_h(d, x, maxw // 2 - 40) for x in b[2]))
    return 0


def draw_block(im, d, b, x, y, maxw, align='center'):
    k = b[0]
    if k == 'gap':
        return y + b[1]
    if k == 'text':
        _, s, size, wt, c = b[:5]
        f = font(wt, size)
        for ln in wrap(d, s, f, maxw):
            w = d.textlength(ln, font=f)
            tx = x + (maxw - w) / 2 if align == 'center' else x
            d.text((tx + 3, y + 4), ln, font=f, fill=(0, 0, 0))
            d.text((tx, y), ln, font=f, fill=col(c))
            y += int(size * 1.12)
        return y
    if k == 'stamp':
        s, c = b[1], col(b[3] if len(b) > 3 else 'amber')
        size = b[2]
        f = font('Black', size)
        w = d.textlength(s, font=f)
        pad = int(size * .45)
        tx = x + (maxw - w) / 2 if align == 'center' else x
        d.rounded_rectangle((tx - pad, y, tx + w + pad, y + int(size * 1.35)), 14, outline=c, width=7, fill=(0, 0, 0, 90))
        d.text((tx, y + int(size * .12)), s, font=f, fill=c)
        return y + int(size * 1.5)
    if k == 'rows':  # (label, value, color)
        _, rows, rh = b
        for lab, val, c in rows:
            d.text((x + 10, y), lab, font=font('Bold', int(rh * .55)), fill=col('ink'))
            f = font('Black', int(rh * .55))
            d.text((x + maxw - 10 - d.textlength(val, font=f), y), val, font=f, fill=col(c))
            d.line((x, y + rh - 8, x + maxw, y + rh - 8), fill=(70, 70, 82), width=2)
            y += rh
        return y
    if k == 'cols':
        _, L, R = b
        hw = maxw // 2 - 40
        yl = y
        for x2 in L:
            yl = draw_block(im, d, x2, x, yl, hw)
        yr = y
        for x2 in R:
            yr = draw_block(im, d, x2, x + maxw // 2 + 40, yr, hw)
        d.line((x + maxw // 2, y, x + maxw // 2, max(yl, yr)), fill=(90, 90, 104), width=3)
        return max(yl, yr)
    return y


def pill(d, xy_right_bottom, text, c='dim', size=24):
    f = font('Medium', size, False)
    w = d.textlength(text, font=f)
    xr, yb = xy_right_bottom
    box = (xr - w - 36, yb - size - 22, xr, yb)
    d.rounded_rectangle(box, 22, fill=(0, 0, 0, 170), outline=(120, 120, 135), width=2)
    d.text((box[0] + 18, box[1] + 9), text, font=f, fill=col(c) if c != 'dim' else (200, 200, 210))


def render(spec, path):
    bg = spec.get('bg', 'dark')
    if bg == 'dark':
        im = bgimg().convert('RGBA')
    else:
        im = Image.new('RGBA', (W, H), (0, 0, 0, spec.get('scrim', 140)))
    d = ImageDraw.Draw(im, 'RGBA')
    blocks = spec.get('blocks', [])
    mx = spec.get('maxw', 1500)
    tot = sum(block_h(d, b, mx) for b in blocks)
    y = spec.get('y', (H - tot) // 2 - 10)
    x = (W - mx) // 2
    for b in blocks:
        y = draw_block(im, d, b, x, y, mx)
    if spec.get('caption'):
        f = font('Black', 46)
        w = min(d.textlength(spec['caption'], font=f), 1760)
        d.rectangle((0, 800, W, 930), fill=(0, 0, 0, 190))
        for k, ln in enumerate(wrap(d, spec['caption'], f, 1760)[:2]):
            d.text(((W - d.textlength(ln, font=f)) / 2, 815 + k * 52), ln, font=f, fill=COL['ink'])
    st = spec.get('status')
    if st:
        c = STATUS.get(st, 'dim')
        f = font('Black', 34)
        w = d.textlength(st, font=f)
        d.rounded_rectangle((80, 70, 80 + w + 44, 70 + 62), 12, fill=(0, 0, 0, 150), outline=col(c), width=4)
        d.text((102, 80), st, font=f, fill=col(c))
    if spec.get('kicker'):
        d.text((84, 150), spec['kicker'], font=font('Bold', 30, False), fill=(215, 215, 225))
    if spec.get('chip'):
        pill(d, (W - 80, H - 150), spec['chip'])
    if spec.get('tag'):
        f = font('Black', 30)
        w = d.textlength(spec['tag'], font=f)
        d.rounded_rectangle((80, H - 130, 80 + w + 44, H - 68), 12, fill=(255, 79, 139, 235))
        d.text((102, H - 121), spec['tag'], font=f, fill=(255, 255, 255))
    if spec.get('credit'):
        pill(d, (W - 80, H - 60), spec['credit'], size=22)
    im.save(path)


# ---------- v3 additions: staged photos/screenshots + pop-ups ----------
def stage(path, out, crop=None, fit=0.86, canvas=(2880, 1620), maxup=3.0):
    """Place a real photo/screenshot on a blurred, darkened copy of itself (no distortion, no fabrication)."""
    im = Image.open(path).convert('RGB')
    if crop: im = im.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
    cw, ch = canvas
    bgc = im.copy()
    r = max(cw / bgc.width, ch / bgc.height)
    bgc = bgc.resize((int(bgc.width * r) + 1, int(bgc.height * r) + 1), Image.BICUBIC)
    bgc = bgc.crop(((bgc.width - cw) // 2, (bgc.height - ch) // 2, (bgc.width - cw) // 2 + cw, (bgc.height - ch) // 2 + ch))
    bgc = bgc.filter(ImageFilter.GaussianBlur(60)).point(lambda v: int(v * 0.35))
    s = min(cw * fit / im.width, ch * fit / im.height, maxup)
    fg = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x, y = (cw - fg.width) // 2, (ch - fg.height) // 2
    sh = Image.new('RGBA', (fg.width + 120, fg.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((60, 70, fg.width + 60, fg.height + 70), fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    bgc = bgc.convert('RGBA'); bgc.alpha_composite(sh, (x - 60, y - 60)); bgc = bgc.convert('RGB')
    bgc.paste(fg, (x, y))
    bgc.save(out, quality=95)
    return out, (x / cw, y / ch, fg.width / cw, fg.height / ch)


def pop(text, out, color='teal', sub=None, size=46):
    f = font('Black', size)
    f2 = font('Medium', int(size * .62), False)
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    w = max(d0.textlength(text, font=f), d0.textlength(sub or '', font=f2)) + 70
    h = int(size * 1.55) + (int(size * .9) if sub else 0)
    im = Image.new('RGBA', (int(w) + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 12, w + 10, h + 12), 18, fill=(0, 0, 0, 120))
    d.rounded_rectangle((6, 6, w + 6, h + 6), 18, fill=(14, 15, 22, 238), outline=col(color), width=4)
    d.rounded_rectangle((6, 6, 26, h + 6), 10, fill=col(color))
    d.text((46, 6 + int(size * .22)), text, font=f, fill=COL['ink'])
    if sub: d.text((46, 6 + int(size * 1.2)), sub, font=f2, fill=(200, 200, 212))
    im.save(out)
    return im.size
