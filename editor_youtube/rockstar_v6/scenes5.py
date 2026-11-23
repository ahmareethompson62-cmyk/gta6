from lib5 import *
import re
V = '/home/claude/project/assets/video/'
G5, L, PRE = V + 'gta5_gameplay_trailer.mp4', V + 'trailer_launch.mp4', V + 'trailer_preload.mp4'
BF, DJ, AJ, RDR = V + 'gta6_bigfoot_forest.mp4', V + 'gta6_dog_jetski.mp4', V + 'gta6_gameplay_airbase_jet.mp4', V + 'rdr2_horse_30fps.mp4'
PR = '/home/claude/press/run-44970113516/images/'
def shot(n): return f'{PR}vi-shots_{n:03d}.jpg'
def art(n): return f'{PR}vi-art_{n:03d}.jpg'
STAT0 = '/home/claude/rr9/staged/research/A003_file-statue-of-liberty-ny-jpg.jpg'
HOUSER = HERE + '/assets/houser.jpg'
CG5 = 'GTA V trailer · Rockstar Games'; CL = 'GTA VI trailer · Rockstar Games'; CP = 'GTA VI press kit · Rockstar Games'
CGP = 'GTA VI gameplay clip · supplied by you (uploader unknown)'

def tvc(srcp, ss, x, y, w, t0=None, dur=None, cap_text='', **k):
    t0 = CUR['t0'] if t0 is None else t0
    d = dur or (CUR['t1'] - t0 + 0.6)
    return tv(M_clip(srcp, ss, d, scale=1280 if srcp in (L, PRE) else None), x, y, w, t0=t0, cap_text=cap_text, **k)

def S(a, b=None, **k): return scene(a, a if b is None else b, **k)
S0 = 0.0
# =============================================================== A. COLD OPEN
S(0, t0=0.0, t1=3.4)
tvc(G5, 16, 960, 600, 1180, t0=0.05, rot=-1.5, cap_text='GTA V', **{'in': 'slide', 'id': 'l'}, drift=.03)
cap(0, 'dared you to be offended', 960, 150, hl=['offended'])
stamp('OFFENDED?', 1560, 840, pt(0, 'offended') + .1, rot=-8)
sticker('ROCKSTAR USED TO…', 340, 330, 0.6, 'yel', 44, -5)
src(CG5, t0=0.3)

S(1, t0=3.4, t1=4.35)
polaroid(M_img(shot(50)), 1130, 560, 900, 640, t0=3.4, cap_text='NOW?', rot=3, **{'in': 'slide', 'id': 'r'})
tile('NOW?', 760, 470, 'o', 700, 'xl', t0=3.5)
src(CP, t0=3.5)

S(2, t0=4.35, t1=11.7)
article('gx', 'wide', 780, 590, 1180, 660, t0=4.45, reg2='head', pan=(5.2, 7.0), hl=pt(2, 'halloween') + .1, rot=-1.5, **{'in': 'slide', 'id': 'l'})
cap(2, 'Halloween promo', 1000, 150, hl=['promo'], z=50)
tile('DRIVERLESS CAR', 1410, 330, 'k', 700, 'sm', t0=pt(2, 'driverless'))
for n, (txt, yy, rr) in enumerate([('GTA NEWS?', 560, 4), ('ANY GTA NEWS?', 700, -3), ('WHERE’S GTA?', 840, 3)]):
    el(f'<div class="bubble c" style="height:100%">{txt}</div>', 1540, yy, 440, 90, t0=pt(2, 'fans') + n * .55, r=rr, **{'in': 'pop'})
label('illustration of the reported replies, not quotes', 1540, 925, pt(2, 'fans') + 1.9, size=21)
src('Gameranx · Todd Black · 10 Oct 2025 · REPORTED', t0=4.6)

S(3, t0=11.7, t1=16.4)
cap(3, 'what happened', 960, 150, hl=['happened'])
sticker('THE STUDIO', 330, 560, 12.2, 'teal', 54, -4)
arrow(480, 575, 700, 575, pt(3, 'once') - .3)
textcard('ITS OWN SCANDAL', 880, 575, 330, 190, t0=pt(3, 'scandal') - .2, cls='A', fs=48, rot=2, **{'in': 'drop'})
arrow(1060, 575, 1270, 575, pt(3, 'statue') - .5)
article('sj', 'mid', 1560, 585, 560, 400, t0=pt(3, 'statue') - .2, rot=3, hl=None, **{'in': 'pop'})
src('SUPERJUMP · J. Barnes · 11 Dec 2025 · ANALYSIS', t0=13)

S(4, t0=16.4, t1=17.8)
sweep(16.45, 'org', 4)
icon('clock', 960, 560, 440, 16.5, c='#efe8d6', **{'in': 'pop'})
el(f'<svg viewBox="0 0 100 100" width="440" height="440">{I("hand")}</svg>', 960, 560, 440, 440, t0=16.5, z=30, **{'in': 'cut', 'din': .01}, kf=[[16.5, dict(r=0)], [17.8, dict(r=-540)]])
cap(4, "let's go back", 960, 160)

# =============================================================== B. THE OLD ROCKSTAR
S(5, t0=17.8, t1=25.7)
note('GRAND THEFT AUTO III · 2001', ['real estate tycoon', 'a Trump parody?', '…with a cannibalism habit'], 450, 400, 560, 330, t0=18.0, **{'in': 'slide', 'id': 'l'})
person(260, 770, 280, 'DONALD LOVE', 'fictional · GTA III', t0=pt(5, 'donald') - .1, rot=-3)
article('sj', 'left', 1260, 600, 900, 560, t0=pt(5, 'real') - .2, rot=2, **{'in': 'slide', 'id': 'r'})
cap(5, 'real estate tycoon', 960, 150, hl=['tycoon'], t1=pt(5, 'critics'))
cap(5, 'Trump parody', 960, 150, hl=['parody'], sz='xl', t1=pt(5, 'cannibalism') - .1)
cap(5, 'cannibalism habit', 960, 150, hl=['cannibalism'], cols=['k', 'p'])
stamp('CRITICS & FANS READ IT SO', 1330, 940, pt(5, 'critics'), 'amber', rot=-3, size=32)
src('SUPERJUMP · Donald Love in GTA · J. Barnes · 11 Dec 2025 · ANALYSIS', t0=18.4)

S(6, t0=25.7, t1=34.0)
polaroid(M_img(shot(29)), 540, 600, 760, 540, t0=25.9, cap_text='VICE CITY (GTA VI context, not the 2002 game)', rot=-3, **{'in': 'slide', 'id': 'l'})
cap(6, 'three times as much talk radio', 1000, 150, hl=['three'], sz='sm', w=1700)
tile('GTA III', 1090, 500, 'w', 400, t0=pt(6, 'about'))
bar(1580, 500, 420, 60, .33, pt(6, 'about') + .1, 'teal')
tile('VICE CITY', 1090, 640, 'o', 400, t0=pt(6, 'three') - .2)
bar(1580, 640, 420, 60, 1.0, pt(6, 'three') - .1, 'org')
counter(3, 1560, 800, pt(6, 'three'), size=170, suf='×', c='#f2b82e', d=.7)
icon('mic', 1000, 880, 160, pt(6, 'lazlow') - .5, c='#efe8d6', rot=-6)
tile('LAZLOW JONES', 1260, 900, 'k', 520, 'sm', t0=pt(6, 'lazlow'))
src('Vice City still: GTA VI press kit (context) · SUPERJUMP analysis', t0=26.4)

S(7, t0=34.0, t1=46.5)
T_more, T_dan = pt(7, 'more'), pt(7, 'dan')
cap(7, 'eleven radio stations', 960, 150, hl=['eleven'], t1=T_more)
for n in range(11):
    icon('radio', 270 + n * 138, 560, 118, pt(7, 'eleven') + n * .17, c=['#efe8d6', '#f2b82e', '#2bb5a2', '#e8559b'][n % 4], rot=[-4, 3, -2, 5][n % 4], t1=T_more - .05, **{'in': 'drop'})
counter(11, 960, 800, pt(7, 'eleven') + .2, size=200, c='#2bb5a2', d=1.2, t1=T_more - .05)
cap(7, 'in-game commercials', 960, 150, hl=['commercials'], t1=T_dan - .1, t0=T_more)
for n in range(6):
    icon('sign', 360 + n * 240, 560, 190, T_more + .15 + n * .2, c=['#e8602c', '#f2b82e', '#2bb5a2'][n % 3], rot=[-3, 4, -2][n % 3], t1=T_dan - .1, **{'in': 'pop'})
counter(3, 960, 840, pt(7, 'commercials') - .5, size=190, suf='×+', c='#f2b82e', t1=T_dan - .1, d=.8)
label('vs GTA III · per Wikipedia', 1500, 920, T_more + 1.2, t1=T_dan - .1)
person(300, 640, 330, 'DAN HOUSER', 'ROCKSTAR CO-FOUNDER', photo=HOUSER, t0=T_dan - .1, rot=-3, pos='center 20%', **{'in': 'slide', 'id': 'l'})
cap(7, 'broader weirdness', 1240, 250, w=1000, hl=['weirdness'], sz='sm', t0=pt(7, 'broader') - .2) if False else None
html, a_, b_ = ransom(7, 'broader weirdness of american consumerism and action movies', hl=['weirdness', 'consumerism'], sz='sm')
el(f'<div class="c fill">{html}</div>', 1230, 560, 1050, 360, t0=a_ - .1, **{'in': 'fade', 'din': .1})
src('Dan Houser on the San Andreas target · Wikipedia: GTA San Andreas · REPORTED', t0=T_dan)

S(8, t0=46.5, t1=47.6)
article('sj', 'mid', 960, 600, 1000, 640, t0=46.5, rot=-1.5, **{'in': 'zoom'})
tile('GTA IV', 960, 230, 'o', 800, 'xl', t0=46.6)
src('SUPERJUMP · GTA IV’s “Statue of Happiness” · ANALYSIS', t0=46.7)

S(9, t0=47.6, t1=55.9)
person(520, 610, 360, 'TOM GOLDBERG', 'lawyer in GTA IV · fictional', t0=pt(9, 'tom') - .1, rot=-4, **{'in': 'slide', 'id': 'l'})
person(1400, 610, 360, 'JACK THOMPSON', 'real-life lawyer', t0=pt(9, 'jack') - .1, rot=4, **{'in': 'slide', 'id': 'r'})
arrow(760, 560, 1180, 560, pt(9, 'jab') - .1, c='#e8602c', sw=14)
sticker('A JAB AT', 960, 470, pt(9, 'jab'), 'org', 56, -5)
cap(9, 'a lawyer named Tom Goldberg', 960, 150, sz='sm', hl=['Goldberg'], t1=pt(9, 'written') + .2)
tile('YEARS GOING AFTER VIDEO GAMES', 960, 880, 'k', 1400, 'sm', t0=pt(9, 'years') - .2)
icon('gavel', 960, 640, 120, pt(9, 'years') + .6, rot=8)
src('SUPERJUMP · J. Barnes · 11 Dec 2025 · ANALYSIS', t0=48.2)

S(10, t0=55.9, t1=59.4)
tv(M_img(shot(38)), 1330, 590, 780, t0=56.0, rot=2, cap_text='GTA IV', **{'in': 'slide', 'id': 'r'})
d = person(430, 620, 340, 'JACK THOMPSON', 'real-life lawyer', t0=56.0, rot=-3, z=30, **{'in': 'cut', 'din': .01})
d['kf'] = [[56.0, dict(x=0, y=0, s=1)], [pt(10, 'put') - .1, dict(x=0, y=0, s=1)], [pt(10, 'put') + .7, dict(x=905, y=-30, s=.5, r=8)], [59.2, dict(x=905, y=-30, s=.5, r=8)]]
cap(10, 'put him in the game', 960, 150, hl=['game'])
stamp('IN THE GAME', 1330, 900, pt(10, 'game') - .1, 'org', rot=-5, size=52)

S(11, t0=59.4, t1=62.1)
textcard('PERMISSION SLIP', 960, 580, 760, 420, t0=59.5, cls='A', fs=96, rot=-2, color='cream', **{'in': 'drop'})
crossout(960, 580, 520, pt(11, 'permission') + .1, rot=0)
cap(11, 'not a studio asking for permission', 960, 150, sz='sm', hl=['permission'], w=1700)

S(12, t0=62.1, t1=70.4)
T2 = pt(12, 'rockstar')
note('THE HOT COFFEE SCANDAL', ['politicians pulled in', 'hearings · headlines'], 560, 520, 640, 330, t0=62.3, t1=T2 - .1, **{'in': 'slide', 'id': 'l'})
icon('cup', 560, 780, 170, 62.6, t1=T2 - .1, rot=-6)
for n in range(3): icon('person', 1130 + n * 170, 560, 150, pt(12, 'politicians') + n * .3, c=['#6aa7d9', '#e8559b', '#f2b82e'][n], t1=T2 - .1, rot=[-4, 3, -2][n])
cap(12, 'Hot Coffee scandal', 960, 150, hl=['coffee'], t1=T2 - .1)
article('sj', 'mid', 780, 590, 1000, 640, t0=T2, rot=-2, **{'in': 'slide', 'id': 'l'})
icon('cup', 1380, 760, 220, pt(12, 'coffee', ) if False else T2 + 2.8, rot=8) if False else None
cap(12, 'Statue of Liberty parody', 960, 150, hl=['parody'], t0=T2 + .8)
polaroid(M_img(STAT0), 1560, 640, 480, 420, t0=pt(12, 'liberty') - .1, cap_text='the real statue (context)', rot=5, **{'in': 'slide', 'id': 'r'})
icon('cup', 1250, 860, 190, pt(12, 'holding'), rot=10)
src('SUPERJUMP · GTA IV “Statue of Happiness” · Photo: William Warby · Wikimedia Commons · CC BY 2.0 (context)', t0=T2 + .3)

S(13, t0=70.4, t1=72.2)
article('sj', 'mid', 960, 620, 1100, 700, t0=70.4, rot=2, **{'in': 'zoom'})
stamp('SUBTLE?', 960, 330, 70.6, 'pink', rot=-6, size=120, w=640)
crossout(1320, 360, 240, 71.1)

S(14, t0=72.2, t1=78.8)
tvc(G5, 200, 820, 610, 1180, rot=-2, cap_text='JOCK CRANLEY', **{'in': 'slide', 'id': 'l'}, drift=.03)
cap(14, 'Jock Cranley', 960, 150, hl=['Cranley'], t1=pt(14, 'a') + 99 if False else 76.2)
sticker('WASHED-UP ACTION STAR', 1590, 400, pt(14, 'washed-up'), 'yel', 44, -4)
sticker('RUNNING FOR GOVERNOR', 1590, 560, pt(14, 'running'), 'teal', 44, 3)
stamp('SCHWARZENEGGER PARODY (ANALYSIS)', 1530, 800, pt(14, 'schwarzenegger'), 'red', rot=-4, size=30, w=640)
src(CG5 + ' · parody reading: SUPERJUMP analysis', t0=72.8)

S(15, t0=78.8, t1=83.6)
article('sj', 'right', 700, 590, 1000, 640, t0=79.0, rot=-2, **{'in': 'slide', 'id': 'l'})
cap(15, 'LifeInvader', 1300, 150, hl=['LifeInvader'], w=900, t1=pt(15, 'facebook') - .1)
tile('FACEBOOK', 1560, 360, 'o', 600, t0=pt(15, 'facebook'))
note('SERIAL NO.', ['FB-2004-0001'], 1560, 640, 520, 190, t0=pt(15, 'serial'), rot=3)
crossout(1560, 680, 330, pt(15, 'filed'), c='#d93a2b')
stamp('FILED OFF', 1500, 880, pt(15, 'filed') + .2, 'red', rot=-6, size=56)
src('SUPERJUMP · LifeInvader in GTA V · ANALYSIS', t0=79.4)

S(16, t0=83.6, t1=85.0)
for n, (reg, lab) in enumerate([('left', 'GTA III'), ('mid', 'GTA IV'), ('right', 'GTA V')]):
    article('sj', reg, 400 + n * 560, 600, 470, 340, t0=83.8 + n * .35, rot=[-3, 2, -2][n], **{'in': 'pop'})
    tile(lab, 400 + n * 560, 830, ['w', 'o', 'k'][n], 400, 'sm', t0=83.9 + n * .35)
arrow(650, 600, 700, 600, 84.5, sw=10) if False else None
icon('mag', 960, 330, 200, 84.2, rot=-10)
cap(16, 'Notice the pattern', 960, 150, hl=['pattern'])

S(17, t0=85.0, t1=88.0)
tvc(G5, 156, 880, 600, 1120, rot=2, cap_text='NOBODY SAFE', **{'in': 'slide', 'id': 'r'})
cap(17, 'Nobody was safe', 960, 150, hl=['safe'], t1=pt(17, 'including') - .1)
cap(17, 'including Rockstar itself', 960, 150, hl=['Rockstar'], t0=pt(17, 'including') - .1)
stamp('NO EXCEPTIONS', 1560, 880, pt(17, 'rockstar'), 'red', rot=-6, size=46)
src(CG5, t0=85.3)

S(18, t0=88.0, t1=91.5)
tvc(G5, 188, 700, 600, 1000, rot=-2, cap_text='', **{'in': 'slide', 'id': 'l'})
cap(18, 'picked a target', 960, 150, hl=['target'], t1=pt(18, 'aimed') - .1)
cap(18, 'aimed', 960, 150, hl=['aimed'], sz='xl', t0=pt(18, 'aimed') - .1, t1=pt(18, 'fired') - .1)
cap(18, 'and fired', 960, 150, hl=['fired'], sz='xl', t0=pt(18, 'fired') - .1)
icon('cross', 1570, 560, 280, pt(18, 'aimed') - .1, c='#d93a2b', **{'in': 'pop'})
icon('burst', 1570, 560, 380, pt(18, 'fired'), c='#f2b82e', rot=6, **{'in': 'stamp'})
src(CG5, t0=88.3)

S(19, t0=91.5, t1=94.9)
tvc(G5, 216, 760, 600, 1100, rot=2, **{'in': 'slide', 'id': 'r'})
cap(19, 'personality', 960, 150, hl=['personality'], t1=pt(19, 'teeth') - .15)
cap(19, 'teeth', 960, 150, hl=['teeth'], sz='xl', t0=pt(19, 'teeth') - .15)
icon('teeth', 1560, 560, 340, pt(19, 'teeth'), rot=-6, **{'in': 'stamp'})
src(CG5, t0=91.8)

S(20, t0=94.9, t1=97.0)
sweep(94.95, 'tan', 8)
polaroid(M_img(shot(38)), 960, 590, 1000, 680, t0=95.1, cap_text='ROCKSTAR NOW', rot=-2)
cap(20, 'the modern Rockstar', 960, 150, hl=['modern'])
src(CP, t0=95.3)

# =============================================================== C. MODERN ROCKSTAR
S(21, t0=97.0, t1=102.7)
person(330, 620, 360, 'DAN HOUSER', '2018', photo=HOUSER, t0=97.1, rot=-3, pos='center 20%', **{'in': 'slide', 'id': 'l'})
icon('clock', 800, 620, 280, 97.4, rot=-4)
el(f'<svg viewBox="0 0 100 100" width="280" height="280">{I("hand")}</svg>', 800, 620, 280, 280, t0=97.6, z=40, **{'in': 'pop'}, kf=[[97.6, dict(r=0)], [102.5, dict(r=1440)]])
counter(100, 1290, 560, pt(21, '100-hour') - .3, size=230, suf='h', c='#f2b82e', d=1.1)
tile('EVERY WEEK', 1290, 760, 'o', 700, t0=pt(21, 'weeks') - .1)
tvc(RDR, 0, 1630, 800, 400, t0=pt(21, 'worked'), dur=5.8, rot=3, cap_text='RDR2', **{'in': 'slide', 'id': 'r'})
cap(21, 'senior writing team', 960, 150, hl=['senior'], sz='sm', t1=pt(21, 'worked') - .05)
cap(21, '100-hour weeks', 960, 150, hl=['100-hour'], t0=pt(21, 'worked') - .05)
src('Dan Houser, 2018 · as reported by GameSpot · RDR2 clip supplied by you', t0=97.4)

S(22, t0=102.7, t1=107.3)
person(300, 640, 300, 'DAN HOUSER', 'clarified later', photo=HOUSER, t0=102.8, rot=-3, pos='center 20%')
for n in range(4): icon('person', 640 + n * 150, 520, 130, pt(22, 'four-person') + n * .18, c=['#e8559b', '#2bb5a2', '#f2b82e', '#6aa7d9'][n], rot=[-3, 2, -2, 3][n])
tile('FOUR-PERSON TEAM', 1050, 360, 'w', 900, 'sm', t0=pt(22, 'four-person'))
for n in range(3): calendar('WEEK', str(n + 1), 1330 + n * 190, 650, pt(22, 'three') + n * .3, w=170, rot=[-3, 2, -1][n])
tile('THREE WEEKS', 1530, 800 + 80, 'o', 700, 'sm', t0=pt(22, 'three') + .1)
stamp('NOT YEARS', 960, 880, pt(22, 'years'), 'red', rot=-5, size=64)
src('Houser’s later clarification · reported by GameSpot (Oct 2018)', t0=103.0)

S(23, 24, t0=107.3, t1=111.7)
tile('FINE.', 900, 300, 'w', 600, 'xl', t0=107.4, t1=108.1)
tvc(L, 4, 960, 610, 1160, t0=108.0, rot=-2, cap_text='GTA VI', **{'in': 'slide', 'id': 'l'})
cap(24, 'the legend was built', 960, 150, hl=['legend'], t0=108.0)
src(CL, t0=108.2)

# =============================================================== D. THE DISPUTE
S(25, t0=111.7, t1=114.3)
sweep(111.75, 'red', 12)
calendar('OCT', '2025', 960, 590, 112.0, '', w=560, rot=-4, **{'in': 'stamp'})
cap(25, 'And then came October 2025', 960, 150, hl=['October'], sz='sm', w=1700)

S(26, t0=114.3, t1=118.3)
article('pcg1', 'wide', 700, 600, 1100, 640, t0=114.4, reg2='head', pan=(115, 116.6), hl=116.0, rot=-2, **{'in': 'slide', 'id': 'l'})
for n in range(30): icon('person', 1400 + (n % 6) * 88, 420 + (n // 6) * 100, 82, 114.7 + n * .08, c='#e8602c' if n < 30 else '#efe8d6', rot=0, **{'in': 'pop', 'din': .25})
counter(30, 1580, 900, 115.2, size=150, suf='+', c='#f2b82e', d=1.2)
cap(26, 'More than thirty', 960, 150, hl=['thirty'], t1=pt(26, 'according'))
cap(26, 'according to reporting', 960, 150, hl=['reporting'], sz='sm', t0=pt(26, 'according') - .1)
stamp('REPORTED', 760, 940, pt(26, 'reporting'), 'amber', rot=-4, size=44)
src('PC Gamer · Andy Chalk · 11 Dec 2025 · REPORTED', t0=114.8)

S(27, t0=118.3, t1=121.9)
counter(30, 660, 600, 118.4, size=340, suf='+', c='#efe8d6', d=.4, **{'in': 'cut', 'din': .01})
el('<div class="c fill A" style="font-size:340px;color:#f2b82e;text-shadow:0 8px 12px rgba(0,0,0,.5)">?</div>', 1080, 600, 300, 400, t0=pt(27, 'never'), **{'in': 'pop'})
stamp('NEVER CONFIRMED', 1010, 860, pt(27, 'never') + .15, 'red', rot=-6, size=70)
article('pcg1', 'by', 1560, 420, 520, 320, t0=118.8, rot=3)
cap(27, 'Rockstar, importantly', 960, 150, hl=['importantly'], t1=pt(27, 'never') - .05, sz='sm')
cap(27, 'never confirmed that number', 960, 150, hl=['never'], sz='sm', t0=pt(27, 'never') - .05, w=1700)
src('PC Gamer · 11 Dec 2025 · The Register · 6 Nov 2025 · REPORTED', t0=118.6)

S(28, t0=121.9, t1=128.5)
icon('doc', 330, 500, 260, 122.1, rot=-6)
stamp('ROCKSTAR RESPONSE', 330, 780, 122.5, 'teal', rot=-4, size=30, w=420)
typed('Rockstar acted against “a small number of individuals” for sharing confidential information in a public forum.', 1160, 590, 1180, 520, 122.3, cps=21, title='statement · as quoted by PC Gamer', fs=52)
cap(28, 'a small number of individuals', 960, 150, hl=['small'], sz='sm', w=1700, t0=pt(28, 'quote') - .05, t1=pt(28, 'for'))
src('PC Gamer · 11 Dec 2025 · ROCKSTAR RESPONSE', t0=122.3)

S(29, t0=128.5, t1=134.95)
icon('doc', 330, 500, 260, 128.7, rot=6)
stamp('ROCKSTAR RESPONSE', 330, 780, 129.1, 'teal', rot=-4, size=30, w=420)
typed('“This was in no way related to people’s right to join a union or engage in union activities.”', 1160, 590, 1180, 520, 128.9, cps=15, title='statement · as quoted by The Register', fs=54)
src('The Register · 6 Nov 2025 · ROCKSTAR RESPONSE', t0=128.9)

S(30, t0=134.95, t1=143.2)
article('pcg2', 'wide', 600, 590, 1060, 620, t0=135.1, reg2='prot', pan=(137, 139.5), rot=-2, **{'in': 'slide', 'id': 'l'})
cap(30, 'the IWGB', 960, 150, hl=['IWGB'], t1=pt(30, 'says'))
note('ROCKSTAR SAYS', ['a public forum'], 1500, 400, 520, 170, t0=pt(30, 'forum') - .5, rot=2)
icon('discord', 1330, 640, 190, pt(30, 'private') - .6, rot=-5)
note('THE IWGB SAYS', ['a private Discord'], 1590, 700, 520, 170, t0=pt(30, 'private') - .2, rot=-2)
tile('PLAIN AND SIMPLE UNION BUSTING', 1260, 930, 'o', 1300, 'sm', t0=pt(30, 'plain'))
stamp('UNION CLAIM', 1700, 940, pt(30, 'plain') + .4, 'amber', rot=-4, size=34)
src('PC Gamer · Lincoln Carpenter · 17 Jun 2026 · UNION CLAIM', t0=135.4)

S(31, t0=143.2, t1=144.8)
icon('mag', 960, 590, 380, 143.3, rot=-10)
cap(31, "what we actually know", 960, 150, hl=['know'], sz='sm', w=1700)

S(32, t0=144.8, t1=149.75)
calendar('NOV', '12', 360, 560, 145.0, '2025', w=330, rot=-4)
stamp('CLAIMS FILED', 360, 810, 145.5, 'teal', rot=-3, size=40)
for n, (txt, ph_) in enumerate([('VICTIMISATION', 'victimisation'), ('COLLECTIVE DISMISSAL', 'collective'), ('BLACKLISTING', 'blacklisting')]):
    textcard(txt, 1010 + (n % 2) * 40, 400 + n * 190, 760, 150, t0=pt(32, ph_) - .1, cls='A', fs=70, rot=[-2, 1.5, -1][n], color=['mint', 'yel', 'pink'][n], fc='#1d1b19', **{'in': 'drop'})
icon('gavel', 1620, 820, 180, 147.5, rot=10)
cap(32, 'legal claims', 960, 150, hl=['claims'], t1=pt(32, 'victimisation') + 99 if False else 146.6)
src('IWGB filing · 12 Nov 2025 · CONFIRMED (as reported)', t0=145.1)

S(33, t0=149.75, t1=158.4)
article('tr', 'wide', 650, 590, 1080, 640, t0=149.9, reg2='head', pan=(151, 152.8), hl=152.4, rot=-2, **{'in': 'slide', 'id': 'l'})
calendar('JAN', '2026', 1560, 330, 150.2, '', w=300, rot=4)
stamp('INTERIM RELIEF REFUSED', 1500, 560, pt(33, 'refused') + .1, 'red', rot=-4, size=40, w=620)
typed('could not conclude it was likely that union membership was the principal reason', 1450, 820, 800, 300, pt(33, 'saying'), cps=17, title='the tribunal’s reasoning', fs=34)
src('TechRadar · Demi Williams · 13 Jan 2026 · CONFIRMED', t0=150.2)

S(34, t0=158.4, t1=160.5)
article('tr', 'sub', 960, 590, 1100, 660, t0=158.5, rot=-1.5, **{'in': 'zoom'})
stamp('NOT A FINAL RULING', 960, 880, 158.8, 'red', rot=-4, size=80, w=1000)

S(35, t0=160.5, t1=164.5)
calendar('JUN', '2026', 420, 560, 160.6, '', w=360, rot=-4)
textcard('BLACKLISTING CLAIMS', 1160, 540, 920, 260, t0=pt(35, 'throw') - .6, cls='A', fs=96, rot=2, color='cream', **{'in': 'drop'})
stamp('NOT THROWN OUT', 1160, 800, pt(35, 'blacklisting') + .2, 'teal', rot=-4, size=70)
cap(35, 'refused to throw out', 960, 150, hl=['refused'], sz='sm', w=1700)
src('PC Gamer · Lincoln Carpenter · 17 Jun 2026 · CONFIRMED', t0=160.8)

S(36, t0=164.5, t1=168.1)
icon('pin', 480, 570, 360, 164.7, c='#e8602c', rot=-5)
tile('GLASGOW', 1130, 460, 'o', 800, 'xl', t0=pt(36, 'glasgow') - .1)
tile('CLOSING ARGUMENTS', 1130, 700, 'k', 1000, t0=pt(36, 'closing') - .1)
calendar('NOV', '17–18', 1620, 360, 165.0, '2026', w=250, rot=4)
src('ITV News, 18 Nov 2026 (page not capturable) · CONFIRMED', t0=164.8)

S(37, t0=168.1, t1=171.8)
el('<div class="bubble c" style="height:100%;font-size:130px;padding:20px 50px;border-radius:40px;background:#efe8d6;line-height:1.05">“CAUGHT RED-HANDED”</div>', 960, 560, 1300, 400, t0=pt(37, 'caught') - .3, r=-2, **{'in': 'pop'})
stamp('ROCKSTAR’S LAWYER', 960, 860, pt(37, 'red-handed') + .1, 'teal', rot=-3, size=56)
cap(37, 'the workers were', 960, 150, sz='sm', t1=pt(37, 'caught'))
src('ITV News, 18 Nov 2026 · ROCKSTAR’S SIDE', t0=168.4)

S(38, t0=171.8, t1=176.5)
for n in range(10): icon('person', 190 + n * 171, 520, 150, 172.2 + n * .1, c='#2bb5a2' if n == 0 else '#efe8d6', **{'in': 'pop', 'din': .25})
counter(10, 960, 720, pt(38, 'approached') - .2, size=240, pre='~', suf='%', c='#f2b82e', d=.9)
tile('UNION MEMBERSHIP', 960, 330, 'w', 1100, t0=pt(38, 'union'))
stamp('CLAIMANTS’ LAWYERS', 960, 920, pt(38, 'claimants') + .1, 'amber', rot=-3, size=48)
src('Reported by TechTimes, 19 Nov 2026 · CLAIMANTS’ SIDE (an allegation)', t0=172.1)

S(39, t0=176.5, t1=178.1)
tile('THOSE ARE CLAIMS.', 960, 500, 'w', 1500, 'xl', t0=176.6)
stamp('CLAIM', 520, 820, 176.9, 'red', rot=-8, size=90)
stamp('CLAIM', 1400, 820, 177.15, 'red', rot=6, size=90)

S(40, t0=178.1, t1=183.7)
d = icon('balance', 640, 560, 520, 178.3, c='#f2b82e', c2='#efe8d6')
d['kf'] = [[178.3, dict(r=-4)], [180, dict(r=4)], [181.8, dict(r=-3)], [183.6, dict(r=2)]]
cap(40, 'neither side proven', 960, 150, hl=['neither'], t1=pt(40, 'judge') - .05, sz='sm', w=1700)
icon('clock', 1360, 560, 320, pt(40, 'timeframe') - .6)
stamp('NO TIMEFRAME', 1360, 820, pt(40, 'timeframe') + .1, 'red', rot=-5, size=56)
cap(40, 'the judge', 960, 150, hl=['judge'], t0=pt(40, 'judge') - .05)
src('ITV News, 18 Nov 2026 · DISPUTED', t0=178.5)

S(41, t0=183.7, t1=187.1)
el('<div class="c fill A" style="font-size:560px;color:#f2b82e;text-shadow:0 10px 16px rgba(0,0,0,.5)">?</div>', 400, 590, 400, 700, t0=183.9, **{'in': 'pop'})
tile('THE MOTIVE', 1180, 330, 'w', 800, 'xl', t0=pt(41, 'motive') - .3)
icon('person', 980, 600, 210, 185.0, c='#2bb5a2', rot=-3)
icon('person', 1480, 600, 210, 185.3, c='#e8602c', rot=3)
tile('WORKERS', 980, 790, 'w', 360, 'sm', t0=185.3)
tile('ROCKSTAR', 1480, 790, 'k', 360, 'sm', t0=185.5)
el('<div class="c fill A" style="font-size:150px;color:#f2b82e">?</div>', 1230, 590, 200, 200, t0=185.8, **{'in': 'pop'})
stamp('UNPROVEN', 1230, 930, pt(41, 'motive') + .3, 'red', rot=-5, size=70)
cap(41, 'we are not going to pretend', 960, 150, sz='sm', w=1700, t1=pt(41, 'motive') - .05)

S(42, t0=187.1, t1=188.8)
d = icon('gavel', 960, 560, 420, 187.2, rot=0)
d['kf'] = [[187.2, dict(r=-28)], [187.9, dict(r=-28)], [188.1, dict(r=14)], [188.35, dict(r=14)]]
cap(42, 'A judge will decide that', 960, 150, hl=['judge'], sz='sm', w=1700)

S(43, t0=188.8, t1=190.3)
icon('clock', 960, 590, 420, 188.9)
el(f'<svg viewBox="0 0 100 100" width="420" height="420">{I("hand")}</svg>', 960, 590, 420, 420, t0=188.9, z=40, **{'in': 'pop'}, kf=[[188.9, dict(r=0)], [190.3, dict(r=420)]])
cap(43, 'look at the timing', 960, 150, hl=['timing'])

S(44, t0=190.3, t1=200.0)
el('<svg width="1700" height="40" viewBox="0 0 1700 40"><path class="dr" pathLength="1" d="M0 20H1700" stroke="#efe8d6" stroke-width="10" stroke-linecap="round" fill="none"/></svg>', 960, 740, 1700, 40, t0=190.4, **{'in': 'draw', 'dd': 1.2, 'din': .05})
tl = pt(44, 'dismissed'); tg = pt(44, 'biggest'); tu = pt(44, 'union')
icon('discord', 440, 560, 220, tl, rot=-4)
tile('DISCORD DISMISSALS', 420, 400, 'w', 560, 'sm', t0=tl)
tvc(L, 12, 960, 560, 420, t0=tg - .2, dur=5.2, rot=-2, cap_text='GTA VI', **{'in': 'pop'})
tile('THE BIGGEST GAME OF ITS LIFE', 960, 280, 'o', 800, 'sm', t0=tg)
icon('ballot', 1480, 560, 220, tu, rot=4)
tile('UNION VOTE', 1500, 400, 'k', 520, 'sm', t0=tu)
tile('GAME OUT', 1480, 880, 'y', 400, 'sm', t0=pt(44, 'game', ) + 0 if False else pt(44, 'out') + 0)
for x, tt in ((440, tl), (960, tg), (1480, tu)):
    el('<div style="width:46px;height:46px;border-radius:50%;background:#e8602c;border:7px solid #efe8d6"></div>', x, 740, 46, 46, t0=tt, **{'in': 'pop'})
src('Dismissals & Discord: PC Gamer/IWGB · Union vote: TechTimes, 19 Nov 2026 · REPORTED', t0=191.0)

S(45, t0=200.0, t1=204.4)
tvc(L, 16, 740, 600, 1000, rot=-2, cap_text='GTA VI', **{'in': 'slide', 'id': 'l'})
cap(45, 'not exactly the vibe', 1000, 150, hl=['vibe'], t1=pt(45, 'of') + 99 if False else 202.0)
tile('A STUDIO THAT DOESN’T TAKE ITSELF SERIOUSLY', 1560, 360, 'k', 560, 'sm', t0=202.0)
stamp('OPINION', 1560, 880, 202.6, 'amber', rot=-5, size=50)
src(CL, t0=200.3)

# =============================================================== E. THE VOICE
S(46, t0=204.4, t1=206.3)
sweep(204.45, 'teal', 5)
icon('mega', 640, 580, 440, 204.7, rot=-8)
cap(46, 'the voice has changed', 1280, 560, w=800, hl=['changed'], sz='')

S(47, t0=206.3, t1=216.0)
Tq = pt(47, 'over')
calendar('YEAR', '2020', 330, 400, 206.7, '', w=300, rot=-4, t1=Tq)
el(card(f'<div class="c A" style="font-size:66px;color:#1d1b19;text-align:center;line-height:1.05;padding:20px">COPS ’N’ CROOKS<div class="M" style="font-size:24px;margin-top:10px">planned GTA Online mode</div></div>', 640, 300, 'tan', 7, ('tl', 'br')), 1050, 480, 640, 300, t0=pt(47, 'quietly') - .6, r=-2, t1=Tq, **{'in': 'drop'})
stamp('SHELVED', 1050, 700, pt(47, 'shelved') + .1, 'red', rot=-6, size=84, t1=Tq)
cap(47, 'quietly shelved', 960, 150, hl=['shelved'], t1=Tq)
cap(47, 'over how it would look', 960, 150, hl=['look'], sz='sm', t0=Tq - .1, w=1700)
tvc(G5, 150, 640, 640, 940, t0=Tq, dur=5.5, rot=-2, cap_text='GTA V (generic)', **{'in': 'slide', 'id': 'l'})
el('<div class="bubble c" style="height:100%;font-size:56px">HOW IT LOOKS</div>', 1480, 470, 520, 120, t0=pt(47, 'look') - .2, r=3, **{'in': 'pop'})
el('<div class="bubble c" style="height:100%;font-size:56px;background:#e8559b;color:#fff">THE POLICING DEBATE</div>', 1480, 650, 520, 120, t0=pt(47, 'policing') - .1, r=-3, **{'in': 'pop'})
src('Bloomberg, 27 Jul 2022 · REPORTED · GTA V footage is generic, not the shelved mode', t0=206.6)

S(48, t0=216.0, t1=219.1)
el(card('<div class="E" style="font-size:36px;line-height:1.7;color:#1d1b19;padding:26px">' + ''.join(f'<div style="position:relative">{t}<span data-t="{217.0 + n * .45:.2f}" style="position:absolute;left:0;top:8px;right:0;height:34px;background:#111;opacity:0"></span></div>' for n, t in enumerate(['A person familiar with the plan said', 'the mode was shelved in 2020', 'because of how it would look'])) + '</div>', 960, 400, 'cream', 4, ('tl', 'br')), 960, 560, 960, 400, t0=216.2, r=-2, **{'in': 'slide', 'id': 'l'})
label('illustration: how unnamed sourcing works, not the real text', 960, 780, 217.4, size=22)
stamp('UNNAMED SOURCES', 1450, 460, pt(48, 'unnamed'), 'amber', rot=-5, size=56)
cap(48, 'reported by Bloomberg', 960, 150, hl=['Bloomberg'], sz='sm', w=1700)
src('Bloomberg, 27 Jul 2022 · REPORTED (paywalled, not captured)', t0=216.2)

S(49, t0=219.1, t1=221.0)
checkmark(560, 580, 420, 219.3, c='#2bb5a2')
cap(49, 'allowed to be careful', 1280, 560, w=900, hl=['careful'], sz='sm')

S(50, t0=221.0, t1=225.0)
tvc(G5, 176, 940, 600, 1120, rot=-2, cap_text='OLD ROCKSTAR', **{'in': 'slide', 'id': 'r'})
cap(50, 'built its name', 960, 150, hl=['name'], t1=pt(50, 'by') - .05)
cap(50, 'by not being careful', 960, 150, hl=['careful'], t0=pt(50, 'by') - .05)
crossout(1570, 600, 300, pt(50, 'careful'), rot=0)
src(CG5, t0=221.3)

# =============================================================== F. GTA VI
S(51, t0=225.0, t1=227.2)
sweep(225.05, 'pink', 6)
polaroid(M_img(art(8)), 960, 590, 1000, 680, t0=225.3, cap_text='GRAND THEFT AUTO VI', rot=-2)
cap(51, 'GTA VI', 960, 150, hl=['VI'], sz='xl', w=900)
src('GTA VI key art · Rockstar Games press kit', t0=225.4)

S(52, t0=227.2, t1=230.7)
article('aj', 'wide', 780, 590, 1140, 650, t0=227.3, reg2='head', pan=(228.2, 229.6), hl=229.0, rot=-2, **{'in': 'slide', 'id': 'l'})
calendar('NOV', '19', 1590, 480, 227.6, '2026', w=330, rot=4)
tile('EARLY REVIEWS: GLOWING', 1560, 800, 'o', 700, 'sm', t0=pt(52, 'glowing') - .5)
cap(52, 'came out on the nineteenth', 960, 150, sz='sm', hl=['nineteenth'], w=1700)
src('Al Jazeera · 19 Nov 2026 · CONFIRMED', t0=227.5)

S(53, t0=230.7, t1=233.0)
for n in range(5): icon('star', 520 + n * 220, 520, 190, 230.9 + n * .1, c='#f2b82e', rot=[-4, 3, -2, 4, -3][n])
crossout(960, 560, 760, 231.7)
cap(53, 'reviews are not the question', 960, 150, hl=['question'], sz='sm', w=1700)

S(54, t0=233.0, t1=235.2)
tvc(L, 28, 760, 600, 1060, rot=-2, **{'in': 'slide', 'id': 'l'})
icon('laugh', 1560, 480, 330, 233.9, rot=8, c='#f2b82e')
tile('IS IT FUNNY?', 1500, 760, 'o', 700, 'xl', t0=pt(54, 'funny') - .6)
cap(54, 'the question is', 960, 150, sz='sm', t1=pt(54, 'funny') - .6)
src(CL, t0=233.3)

S(55, t0=235.2, t1=245.4)
Td = pt(55, 'very')
person(300, 600, 320, 'ROB NELSON', 'ROCKSTAR NORTH · CO-STUDIO HEAD', t0=235.4, rot=-3, **{'in': 'slide', 'id': 'l'})
article('gr', 'wide', 1150, 580, 1000, 600, t0=235.5, reg2='quote', pan=(238.0, 239.5), hl=237.5, rot=2, t1=Td, **{'in': 'slide', 'id': 'r'})
cap(55, 'what they satirize', 960, 150, hl=['satirize'], sz='sm', w=1700, t1=Td)
for n, txt in enumerate(['SPECIFIC POLITICAL ISSUES', 'MEMES']):
    textcard(txt, 1050 + n * 120, 440 + n * 190, 760, 150, t0=Td + n * .5, cls='A', fs=70, rot=[-2, 2][n], color=['mint', 'yel'][n], **{'in': 'drop'})
for n in range(3): calendar('', ['1', '2', '3'][n], 1590 + n * 0, 720, 241.5, '', w=1, rot=0) if False else None
stamp('WILL DATE QUICKLY', 1230, 840, pt(55, 'quickly') - .5, 'red', rot=-4, size=62)
cap(55, 'will date quickly', 960, 150, hl=['quickly'], sz='sm', w=1700, t0=pt(55, 'date') - .05)
src('GamesRadar · Jordan Gerblick · 28 Aug 2026 · CONFIRMED', t0=235.7)

S(56, t0=245.4, t1=254.2)
Tq2 = pt(56, 'because')
person(300, 600, 320, 'RUPERT HUMPHRIES', 'ROCKSTAR SVP, NARRATIVE', t0=245.6, rot=3, **{'in': 'slide', 'id': 'l'})
article('wccf', 'head', 1170, 560, 1000, 580, t0=245.7, reg2='img', pan=(248, 249.5), hl=246.5, rot=-2, t1=Tq2, **{'in': 'slide', 'id': 'r'})
cap(56, 'avoid simply mirroring reality', 960, 150, hl=['mirroring'], sz='sm', w=1700, t1=Tq2)
typed('you could just go outside and live in the real world', 1030, 600, 1160, 330, Tq2 + .05, cps=24, title='as reported by Wccftech, relaying Love Magazine', fs=56)
icon('x', 1640, 860, 1, 0) if False else None
src('Wccftech · Alessio Palumbo · 5 Oct 2026 · REPORTED (original interview not seen)', t0=245.9)

for k, (ss, txt, shotn, c) in enumerate([(57, 'SMART?', 23, 'teal'), (58, 'SURE.', 13, 'cream'), (59, 'SAFE?', 95, 'yel'), (60, 'ALSO YES.', 12, 'pink')]):
    t0_ = [254.2, 254.95, 255.7, 256.4][k]; t1_ = [254.95, 255.7, 256.4, 257.5][k]
    S(ss, t0=t0_, t1=t1_)
    tvc(L, [48, 56, 64, 72][k], 960, 590, 1100, t0=t0_, dur=t1_ - t0_ + .5, rot=[-2, 2, -2, 2][k], cap_text='GTA VI', **{'in': 'flip'})
    tile(txt, 960, 130, c if c != 'cream' else 'w', 800, 'xl', t0=t0_ + .05)
    src(CL, t0=t0_ + .1)

S(61, t0=257.5, t1=262.8)
article('wccf', 'img', 700, 590, 1060, 640, t0=257.6, reg2='cap', pan=(259, 260.8), rot=-2, **{'in': 'slide', 'id': 'l'})
cap(61, 'specific real people and movements', 960, 150, sz='sm', hl=['avoids'], w=1800, cols=['w', 'k'])
for n, (nm, tt) in enumerate([('REAL PEOPLE', pt(61, 'real')), ('MOVEMENTS', pt(61, 'movements'))]):
    icon('person', 1520, 400 + n * 280, 150, tt, c='#efe8d6', rot=[-3, 3][n])
    tile(nm, 1520, 540 + n * 280, 'k', 540, 'sm', t0=tt)
    crossout(1520, 410 + n * 280, 200, tt + .5)
stamp('REPORTED', 1560, 920, 259.5, 'amber', rot=-4, size=44)
src('Wccftech · 5 Oct 2026 · relaying Love Magazine · REPORTED', t0=258)

S(62, 63, t0=262.8, t1=264.15)
tvc(L, 32, 760, 590, 1000, rot=-2, **{'in': 'slide', 'id': 'l'})
tile('THAT’S A CHOICE.', 1440, 470, 'w', 800, 'sm', t0=263.0)
tile('MIGHT BE A GOOD ONE', 1440, 700, 'o', 800, 'sm', t0=263.4)
src(CL, t0=263.0)

S(64, t0=264.15, t1=267.9)
tvc(L, 44, 1410, 560, 780, t0=264.2, rot=2, cap_text='GTA VI', **{'in': 'slide', 'id': 'r'})
tile('SATIRE', 420, 350, 'w', 520, 'xl', t0=pt(64, 'satire'))
el(card('<div class="c M" style="font-size:40px;font-weight:700;color:#555;height:100%">NAMES: ________</div>', 560, 150, 'cream', 3, ('tl', 'br')), 470, 560, 560, 150, t0=pt(64, 'never') - .1, r=-2, **{'in': 'drop'})
crossout(470, 560, 250, pt(64, 'names') + .2)
tile('JUST A VIBE', 520, 800, 'o', 900, 'xl', t0=pt(64, 'vibe') - .3)
stamp('OPINION', 1560, 930, pt(64, 'vibe'), 'amber', rot=-6, size=48)
src(CL, t0=264.4)

S(65, t0=267.9, t1=269.85)
sweep(267.95, 'vio', 9)
tvc(L, 40, 960, 600, 1140, rot=-2, **{'in': 'slide', 'id': 'l'})
cap(65, 'So did Rockstar change?', 960, 150, hl=['change'], w=1700)
src(CL, t0=268.2)

S(66, t0=269.85, t1=271.55)
article('gx', 'head', 700, 590, 1020, 620, t0=270.0, rot=-2, **{'in': 'slide', 'id': 'l'})
el('<div class="bubble c" style="height:100%;font-size:96px;background:#e8559b;color:#fff">SAFER?</div>', 1520, 520, 520, 190, t0=pt(66, 'safer') - .3, r=4, **{'in': 'pop'})
stamp('FANS SAY · OPINION', 1520, 760, pt(66, 'fans') + .1, 'amber', rot=-4, size=44, w=620)
src('Gameranx · 10 Oct 2025 · fan reaction is opinion', t0=270.1)

S(67, t0=271.55, t1=279.1)
Trs = pt(67, 'rockstar')
article('pcg2', 'prot', 560, 560, 860, 520, t0=271.7, rot=-2, **{'in': 'slide', 'id': 'l'})
stamp('WORKERS SAY', 560, 270, pt(67, 'workers'), 'amber', rot=-3, size=64, w=640)
tile('HARDER ON THE PEOPLE WHO BUILD THE GAMES', 560, 880, 'k', 840, 'sm', t0=pt(67, 'harder') - .2)
el('<div class="c fill A" style="font-size:120px;color:#efe8d6;text-shadow:0 6px 10px rgba(0,0,0,.5)">VS</div>', 960, 560, 200, 160, t0=Trs - .6, **{'in': 'pop'})
article('pcg1', 'head', 1360, 560, 860, 520, t0=Trs - .2, rot=2, **{'in': 'slide', 'id': 'r'})
stamp('ROCKSTAR SAYS', 1360, 270, Trs, 'teal', rot=3, size=64, w=640)
tile('ONLY ACTED ON CONFIDENTIAL LEAKS', 1360, 880, 'w', 840, 'sm', t0=pt(67, 'confidential') - .3)
src('PC Gamer · 17 Jun 2026 & 11 Dec 2025 · UNION CLAIM vs ROCKSTAR RESPONSE', t0=272.0)

S(68, t0=279.1, t1=280.85)
tvc(AJ, 6, 960, 600, 1280, rot=-1.5, cap_text='GTA VI', **{'in': 'slide', 'id': 'l'})
cap(68, 'Maybe the game is brilliant', 960, 140, hl=['brilliant'], sz='sm', w=1800)
src(CGP, t0=279.3)
S(69, t0=280.85, t1=282.3)
tvc(BF, 40, 960, 600, 1280, rot=1.5, cap_text='GTA VI', **{'in': 'slide', 'id': 'r'})
cap(69, "it's still got bite", 960, 140, hl=['bite'], sz='sm', w=1800)
src(CGP, t0=281.0)
S(70, t0=282.3, t1=283.75)
tvc(DJ, 58, 960, 600, 1280, rot=-1.5, cap_text='GTA VI', **{'in': 'slide', 'id': 'l'})
cap(70, "I can't tell you that", 960, 140, hl=['tell'], sz='sm', w=1800)
src(CGP, t0=282.5)

S(71, t0=283.75, t1=288.1)
tvc(G5, 272, 860, 610, 1160, rot=-2, cap_text='GTA V', **{'in': 'slide', 'id': 'l'})
cap(71, 'built its legend', 960, 150, hl=['legend'], sz='', t1=pt(71, 'throwing') - .05)
cap(71, 'by throwing punches', 960, 150, hl=['punches'], t0=pt(71, 'throwing') - .05)
icon('fist', 1570, 560, 300, pt(71, 'punches') - .6, rot=-8)
icon('burst', 1570, 560, 420, pt(71, 'punches'), c='#f2b82e', rot=6, z=1, **{'in': 'stamp'})
src(CG5, t0=284.0)

S(72, 73, t0=288.1, t1=DUR + 1)
el('<div class="fill sh"><div class="win fill" style="background:#f4f1e8;border-color:#1d1b19;color:#1d1b19"><div class="bar" style="background:#1d1b19"><b style="background:#ff5f57"></b><b style="background:#febc2e"></b><b style="background:#28c840"></b><span class="M" style="margin-left:14px;font-size:20px;color:#efe8d6">comments</span></div><div style="padding:30px"><div class="H" style="font-size:44px;opacity:.6">Add a comment…</div><div class="E typ" data-text="Did Rockstar change for the worse, or are we just older?" style="font-size:58px;line-height:1.25;margin-top:20px;color:#1d1b19"></div></div></div></div>', 960, 600, 1300, 480, t0=288.6, cps=19, r=-1.5, **{'in': 'pop'})
cap(72, 'tell me in the comments', 960, 150, hl=['comments'], sz='sm', w=1800, t1=pt(73, 'did') - .05)
icon('bubble', 330, 440, 200, 289.2, c='#e8602c', rot=-6)
icon('bubble', 1600, 420, 200, 289.5, c='#2bb5a2', rot=6)
sticker('WORSE?', 560, 985, pt(73, 'worse') - .2, 'org', 64, -4, t1=None)
sticker('OR JUST OLDER?', 1280, 985, pt(73, 'older') - .4, 'teal', 64, 3, t1=None)

# ---------------- running subtitles (real sentence text, aligned to the spoken words)
def build_subs():
    for si, snt in enumerate(sents):
        toks = sw(si); D = snt['text'].split(); j = 0; timed = []
        for dw in D:
            target = len(re.sub(r'[^a-z0-9]', '', dw.lower())); acc = 0; first = None
            while j < len(toks) and (acc < target or first is None):
                if first is None: first = toks[j]
                acc += len(norm(toks[j]['w']).replace("'", '')) or 1; j += 1
                if acc >= target: break
            timed.append((dw, (first or toks[-1])['s']))
        lines, cur = [], []
        for dw, t in timed:
            cur.append((dw, t))
            if len(cur) >= 8 or (len(cur) >= 4 and dw[-1] in ',.?!;:'): lines.append(cur); cur = []
        if cur:
            if lines and len(cur) < 3: lines[-1] += cur
            else: lines.append(cur)
        for ln in lines:
            a = ln[0][1]; nxt = None
            html = ''.join(f'<i data-t="{t - .03:.3f}" style="opacity:0">{w}</i>' for w, t in ln)
            idx = lines.index(ln)
            b = (lines[idx + 1][0][1] if idx + 1 < len(lines) else min(sents[si]['end'] + .25, DUR + 1))
            width = int(sum(len(w) for w, _ in ln) * 25 + len(ln) * 18 + 70)
            el(f'<div class="c fill"><div class="subb">{html}</div></div>', 960, 1018, max(500, width), 76, t0=a - .08, t1=b - .02, z=800, drift=0, **{'in': 'cut', 'out': 'none', 'din': .01, 'dout': .01})
build_subs()
n = spec_json()
print('elements', n)
