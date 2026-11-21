"""v3 visual upgrade: replaces repetitive cards with the user-supplied real photos/screenshots/footage and adds pop-ups.
Imported by render.py; mutates edl.SEG. Image bases: ('I', key, crop|None, (z0,z1,fx,fy)); video: ('F','G5',in)."""
import edl
from edl import s, e, END, CREDIT
P = '/home/claude/project/assets/images/'
IMG = dict(
 BOX5=(P+'gta5_xbox360_box.jpg', None, .62), DISCS=(P+'gta5_discs.jpg', None, .55),
 HERO6=(P+'rockstar_store_gta6_hero.png', None, .92), CIB=(P+'rockstar_store_code_in_box.png', None, .92),
 ENG=(P+'engadget_gta_online_oct1.png', (300,30,800,250), .82), GGG=(P+'gamesgg_30fps.png', (480,0,860,720), .78),
 DEXH=(P+'dexerto_headline.png', None, .92), DEXPHOTO=(P+'dexerto_headline.png', (300,315,740,280), .8), DEXP=(P+'dexerto_paragraph.png', None, .8),
 MC=(P+'metacritic_gta6_page_nov20.png', None, .93), MCSCORE=(P+'metacritic_gta6_page_nov20.png', (1160,360,445,230), .75),
 MCBUY=(P+'metacritic_gta6_page_nov20.png', (1160,780,445,160), .8), MCUSER=(P+'metacritic_gta6_page_nov20.png', (1160,490,445,110), .8),
 OC=(P+'../reference_not_used_on_screen/opencritic_gta6_99.png', (160,0,760,580), .85), TPU=(P+'techpowerup_roundup.png', (200,180,1170,350), .93),
 TPUDATE=(P+'techpowerup_roundup.png', (200,180,1170,130), .93),
)
CRED = dict(
 BOX5='GTA 5 Xbox 360 box photo (supplied)', DISCS='GTA 5 discs photo (supplied)', HERO6='Rockstar Store: Grand Theft Auto VI page',
 CIB='Rockstar Store, Physical (Code-in-Box) listing', ENG='Engadget, Aug 15 2013 (headline)', GGG='Games.gg, updated Nov 16 2026',
 DEXH='Dexerto, Nov 15 2026 (headline)', DEXPHOTO='Dexerto, Nov 15 2026 (photo in article)', DEXP='Dexerto, Nov 15 2026',
 MC='Metacritic, PS5 page, captured Nov 20 2026', MCSCORE='Metacritic, captured Nov 20 2026', MCBUY='Metacritic "Where to Buy", Nov 20 2026', MCUSER='Metacritic, captured Nov 20 2026',
 OC='OpenCritic, GTA VI page', TPU='TechPowerUp, Nov 18 2026', TPUDATE='TechPowerUp, Nov 18 2026')
G5C = 'GTA 5 gameplay trailer (Rockstar Games, supplied by user)'
CREDIT['G5'] = G5C
EDL = edl.SEG

def find(t0):
    for g in EDL:
        if abs(g['t0'] - t0) < 0.011: return g
    raise KeyError(t0)

def img(t0, key, pops=(), z=(1.0, 1.10, .5, .5), t1=None, **card):
    g = find(t0)
    if t1 is not None: g['t1'] = t1
    g['base'] = ('I', key, z)
    card.setdefault('credit', CRED[key]); card.setdefault('bg', 'none'); card['scrim'] = 0
    card['blocks'] = []; card['pops'] = list(pops)
    g['card'] = card

def vid(t0, src, inp, pops=(), t1=None, **card):
    g = find(t0)
    if t1 is not None: g['t1'] = t1
    g['base'] = ('F', src, inp)
    card.setdefault('credit', G5C); card['scrim'] = 0; card['pops'] = list(pops); card.setdefault('blocks', [])
    g['card'] = card

def addpop(t0, *pops):
    g = find(t0); g['card'].setdefault('pops', []).extend(pops)

# pop = (start_offset, duration, text, color, sub, pos)
# --- cold open ---
img(0.0, 'BOX5', [(0.5, 3.2, '$59.99', 'ink', 'GTA 5 standard price at 2013 launch', 'tr')], z=(1.0, 1.12, .5, .45), chip='Context: Attack of the Fanboy')
img(s(1), 'HERO6', [(0.2, 2.2, '$79.99', 'pink', 'GTA 6 standard edition', 'tr')], z=(1.0, 1.10, .3, .4), status='CONFIRMED')
img(s(2), 'DISCS', [(0.3, 2.2, 'GTA 5: A DISC', 'ink', None, 'tr')], z=(1.0, 1.08, .5, .5))
img(s(3), 'CIB', [(0.4, 2.6, 'NO DISC INSIDE', 'pink', 'only a download code', 'tr')], z=(1.0, 1.15, .2, .5), status='CONFIRMED')
img(s(4), 'ENG', [(0.4, 2.6, 'ONLINE: OCT 1, 2013', 'teal', 'two weeks after launch', 'br')], z=(1.0, 1.10, .5, .5))
vid(s(6), 'G5', 152.0, [(0.3, 2.6, 'GTA 5: 30 FPS', 'ink', 'on console', 'tr')], chip='Context: Digital Foundry / Games.gg')
img(s(8), 'DEXH', [(0.3, 3.8, 'REPORTED', 'amber', 'Rockstar hasn\'t confirmed scale', 'br')], z=(1.0, 1.08, .35, .5), status='REPORTED')
img(s(9), 'MC', [(0.4, 2.8, '99 METASCORE', 'teal', 'based on 152 critic reviews', 'bl'), (3.2, 2.6, 'BEST-REVIEWED, TIED', 'ink', None, 'bl')], z=(1.0, 1.9, .84, .36), status='REPORTED')
img(s(11), 'TPU', [(0.4, 3.0, 'ZERO MIXED OR NEGATIVE', 'teal', 'at time of writing, per TechPowerUp', 'br'), (3.4, 2.8, '118 PERFECT SCORES', 'ink', 'of 147 on Metacritic (PS5)', 'br')], z=(1.0, 1.10, .5, .3), status='REPORTED')
# --- ch1 ---
img(s(25), 'GGG', [(0.3, 4.2, 'TARGETS 30 FPS', 'ink', 'PS5 and Xbox Series X|S', 'br'), (4.8, 4.8, 'NO 60 FPS MODE AT LAUNCH', 'amber', 'Dot Esports roundup: "disappointing" (reported)', 'br')], z=(1.0, 1.10, .5, .45), status='REPORTED')
# --- ch2 ---
img(s(38), 'MCBUY', [(0.2, 2.4, '$79.99', 'pink', 'standard edition, PS5 and Xbox', 'tr')], z=(1.0, 1.10, .5, .5), status='CONFIRMED')
# --- ch3 ---
img(s(52), 'CIB', [(0.4, 3.0, 'A DISC WILL NOT BE INCLUDED', 'pink', 'Rockstar Store wording', 'tr'), (3.8, 3.5, 'A BOX WITH A CODE IN IT', 'ink', None, 'tr')], z=(1.0, 1.25, .65, .45), status='CONFIRMED')
img(s(56), 'DEXPHOTO', [(0.4, 4.0, 'THE CODE HAS TO BE IN THE BOX', 'amber', 'photo from Dexerto\'s report', 'br')], z=(1.0, 1.18, .5, .5), status='REPORTED')
img(s(58), 'DEXH', [(0.5, 3.5, 'MISSING OR ALREADY-REDEEMED CODES', 'amber', 'reported by buyers, from Nov 13', 'bl'), (4.2, 3.6, 'DEXERTO · NOV 15', 'ink', 'citing Twisted Voxel', 'bl')], z=(1.0, 1.12, .5, .5), status='REPORTED')
img(s(59), 'DEXP', [(0.3, 1.8, 'GameStop', 'amber', 'named in the report', 'tr'), (1.7, 1.8, 'Best Buy', 'amber', 'named in the report', 'tr'), (3.1, 2.4, 'Rockstar\'s own store', 'amber', 'named in the report', 'tr')], z=(1.0, 1.06, .5, .5), status='REPORTED')
# --- ch4 ---
vid(s(71), 'G5', 276.0, [(0.3, 3.2, 'SEPT 17, 2013', 'ink', 'GTA 5 launches', 'tr'), (3.4, 3.4, 'OCT 1, 2013', 'teal', 'GTA Online, about 2 weeks later', 'tr'), (6.6, 3.0, 'RDR2 ONLINE', 'violet', 'followed about a month later', 'tr')], t1=s(74), status='CONFIRMED', chip='Context: Engadget, Trusted Reviews')
# --- ch5 ---
vid(s(86), 'G5', 248.0, [(2.5, 3.0, 'THE OLD CRITICISM', 'red', 'do exactly what the game wants', 'tr')], t1=s(88), caption='FOR YEARS: DO EXACTLY WHAT THE GAME WANTS, OR FAIL')
# --- ch8 ---
img(s(129), 'MCSCORE', [(0.2, 1.6, '99', 'teal', 'Metacritic · 152 reviews', 'tr')], z=(1.0, 1.12, .5, .5), status='REPORTED')
img(s(130), 'OC', [(0.2, 1.6, '99 · 100th percentile', 'teal', 'OpenCritic · 89 reviews', 'br')], z=(1.0, 1.10, .5, .4), status='REPORTED')
img(s(131), 'TPU', [(0.2, 2.6, 'TIED WITH OCARINA OF TIME', 'ink', 'per TechPowerUp (original, 99)', 'br')], z=(1.0, 1.10, .3, .25), status='REPORTED')
# split old 137-141 timeline into reviews-date and user-score screens
g = find(s(137)); g['t1'] = e(139) if False else s(140)
img(s(137), 'TPUDATE', [(0.3, 3.0, 'REVIEWS: NOV 18', 'ink', 'embargo lifted a day before launch', 'br'), (2.2, 3.0, 'LAUNCH: NOV 19', 'teal', None, 'bl')], z=(1.0, 1.08, .5, .5), t1=s(140), status='REPORTED')
nxt = dict(t0=s(140), t1=s(141), base=None, card={})
edl.SEG.append(nxt)
img(s(140), 'MCUSER', [(0.3, 4.0, 'USER SCORE: 5.2', 'amber', 'Mixed or average · 12,337 ratings', 'br')], z=(1.0, 1.12, .5, .5), status='REPORTED')
