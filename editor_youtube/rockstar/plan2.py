"""Sentence-by-sentence visual plan (v4). Every shot: t = start time (s), kind, source, motion, credit/status chip, animated callouts.
Shots run until the next shot starts. Callout times are relative to the shot start."""
import json
sents = json.load(open('/home/claude/rockstar_video/sents.json')); sil = json.load(open('/home/claude/rockstar_video/audio/sil.json'))
DUR = 293.25
def snap(t):
    b = min(((abs((a + c) / 2 - t), (a + c) / 2) for a, c in sil), default=(9, t)); return b[1] if b[0] <= 0.5 else t
def T(i, dt=0.0): return round(snap(sents[i]['start']) + dt, 2)
V = '/home/claude/project/assets/video/'
G5, L, PRE = V + 'gta5_gameplay_trailer.mp4', V + 'trailer_launch.mp4', V + 'trailer_preload.mp4'
BF, DJ, AJ, RDR = V + 'gta6_bigfoot_forest.mp4', V + 'gta6_dog_jetski.mp4', V + 'gta6_gameplay_airbase_jet.mp4', V + 'rdr2_horse_30fps.mp4'
PR = '/home/claude/press/run-44970113516/images/'
def shot(n): return f'{PR}vi-shots_{n:03d}.jpg'
def art(n): return f'{PR}vi-art_{n:03d}.jpg'
NW = '/home/claude/rr11/package/assets/research/screenshots/'
N = dict(aj=NW + 'A037s_w-aj_0.jpg', gr=NW + 'A040s_w-gr_0.jpg', gx=NW + 'A044s_w-gx_0.jpg', pcg1=NW + 'A058s_w-pcg1_0.jpg', pcg2=NW + 'A060s_w-pcg2_0.jpg', sj=NW + 'A063s_w-sj_0.jpg', tr=NW + 'A070s_w-tr_0.jpg', wccf=NW + 'A072s_w-wccf_0.jpg')
ST = '/home/claude/rr9/staged/research/'
STAT = [ST + 'A003_file-statue-of-liberty-ny-jpg.jpg', ST + 'A006_file-statue-of-liberty-frontal-2-crop-jp.jpg']
# page regions (normalised page coords: cx, cy, size)
R = dict(
 gx=dict(wide=(.5,.5,1), head=(.40,.20,.42), date=(.35,.27,.30), logo=(.40,.57,.45)),
 aj=dict(wide=(.5,.5,1), head=(.37,.46,.38), sub=(.40,.53,.30)),
 gr=dict(wide=(.5,.5,1), head=(.41,.51,.38), quote=(.41,.64,.30)),
 pcg1=dict(wide=(.5,.5,1), head=(.42,.56,.42), by=(.40,.70,.30), sub=(.42,.73,.30)),
 pcg2=dict(wide=(.5,.5,1), head=(.41,.52,.40), date=(.38,.72,.30), prot=(.41,.90,.35)),
 sj=dict(wide=(.5,.5,1), head=(.475,.27,.42), left=(.29,.80,.26), mid=(.50,.84,.24), right=(.70,.80,.26)),
 tr=dict(wide=(.5,.5,1), head=(.41,.55,.40), sub=(.41,.68,.30)),
 wccf=dict(wide=(.5,.5,1), head=(.50,.33,.50), img=(.50,.60,.45), cap=(.40,.86,.30)))
# highlight rectangles on pages (x,y,w,h normalised) baked as marker
HL = dict(gx=(.17,.14,.46,.10), aj=(.19,.40,.36,.11), gr=(.25,.44,.32,.14), pcg1=(.25,.43,.33,.24), pcg2=(.25,.43,.33,.18), sj=(.30,.19,.35,.15), tr=(.25,.47,.33,.15), wccf=(.20,.27,.60,.11))
P = []
def add(t, kind, **k): P.append(dict(t=t, kind=kind, **k))
def clip(t, src, ss, credit, status=None, co=(), tr='cut', z=(1.0, .94), c=(.5, .5)): add(t, 'clip', src=src, ss=ss, credit=credit, status=status, co=list(co), tr=tr, z=z, c=c)
def still(t, img, credit, status=None, co=(), tr='cut', b0=(.5, .5, 1), b1=(.5, .5, .90)): add(t, 'still', img=img, credit=credit, status=status, co=list(co), tr=tr, b0=b0, b1=b1)
def pm(b): return b if b[2] >= 1 else (round(.04 + .92 * b[0], 4), round(.04 + .92 * b[1], 4), round(.92 * b[2], 4))
def paper(t, key, r0, r1, credit, status=None, co=(), tr='cut', hl=True): add(t, 'paper', key=key, b0=pm(R[key][r0]), b1=pm(R[key][r1]), credit=credit, status=status, co=list(co), tr=tr, hl=HL[key] if hl else None)
def kin(t, co, tint='pink', credit=None, status=None, tr='cut'): add(t, 'kin', tint=tint, credit=credit, status=status, co=list(co), tr=tr)
def big(a, d, l1, l2=None, c='ink', sub=None): return dict(k='big', a=a, d=d, l1=l1, l2=l2, c=c, sub=sub)
def word(a, d, w, c='ink'): return dict(k='word', a=a, d=d, l1=w, c=c)
def quote(a, d, text, who, c='teal'): return dict(k='quote', a=a, d=d, l1=text, l2=who, c=c)
CG5 = 'GTA V trailer · Rockstar Games'; CL = 'GTA VI trailer · Rockstar Games'; CP = 'GTA VI official screenshot · Rockstar Games press kit'
CGP = 'GTA VI gameplay clip · supplied by you, uploader unknown'
# ---- A. cold open
clip(0.0, G5, 16, CG5, co=[big(0.3, 3.0, 'ROCKSTAR HAS CHANGED', 'BUT NOT FOR THE BETTER', 'pink')], tr='dip', z=(1.0, .93))
still(T(1), shot(50), CP, co=[word(0.0, 0.8, 'NOW?', 'amber')], tr='flash', b0=(.5, .5, .8), b1=(.5, .5, .7))
paper(T(2), 'gx', 'wide', 'head', 'Gameranx · Todd Black · 10 Oct 2025', 'REPORTED', [big(0.4, 3.0, 'HALLOWEEN PROMO', 'FANS WANTED GTA VI NEWS', 'amber')])
paper(T(2, 3.4), 'gx', 'date', 'logo', 'Gameranx · Todd Black · 10 Oct 2025', 'REPORTED', hl=False)
paper(T(3), 'sj', 'mid', 'mid', 'SUPERJUMP · J. Barnes · 11 Dec 2025 (GTA IV’s “Statue of Happiness”)', 'ANALYSIS', [big(0.4, 3.0, 'THE STATUE OF HAPPINESS', 'GTA IV · A ROCKSTAR PARODY', 'pink')], tr='dip', hl=False)
# ---- B. old Rockstar
paper(T(4), 'sj', 'wide', 'head', 'SUPERJUMP · J. Barnes · 11 Dec 2025', 'ANALYSIS', [big(0.3, 3.2, '27 YEARS OF GTA PARODIES', None, 'teal')])
paper(T(5), 'sj', 'head', 'left', 'SUPERJUMP · Donald Love in GTA', 'ANALYSIS', [big(0.3, 3.4, 'DONALD LOVE', 'READ AS A TRUMP PARODY (ANALYSIS)', 'amber')], hl=False)
paper(T(5, 3.8), 'sj', 'left', 'left', 'SUPERJUMP · Donald Love in GTA', 'ANALYSIS', hl=False)
still(T(6), shot(29), 'CONTEXT: GTA VI’s Vice City, not the 2002 game · ' + CP, 'CONTEXT', [big(0.2, 3.8, 'VICE CITY · 2002', '~3× THE TALK RADIO OF GTA III', 'teal')], tr='dip', b0=(.5, .5, 1), b1=(.5, .45, .85))
still(T(6, 4.1), shot(31), 'CONTEXT: GTA VI’s Vice City, not the 2002 game · ' + CP, 'CONTEXT', [], b0=(.45, .5, .9), b1=(.55, .5, .8))
kin(T(7), [big(0.2, 5.8, 'SAN ANDREAS · 2004', '11 RADIO STATIONS', 'teal'), big(6.0, 6.2, '3×+ IN-GAME ADS', 'vs GTA III · per Wikipedia', 'amber')], 'teal', 'Wikipedia: GTA San Andreas · Dan Houser: “broader weirdness” of American consumerism', 'REPORTED')
paper(T(8), 'sj', 'right', 'right', 'SUPERJUMP · J. Barnes · 11 Dec 2025', 'ANALYSIS', [big(0.0, 0.9, 'GTA IV', None, 'pink')], tr='flash', hl=False)
kin(T(9), [big(0.2, 4.0, 'TOM GOLDBERG', 'the lawyer in GTA IV', 'pink'), big(4.2, 4.0, '← JACK THOMPSON', 'real lawyer who went after games', 'amber')], 'pink', 'SUPERJUMP, 11 Dec 2025', 'ANALYSIS')
kin(T(10), [big(0.2, 3.2, 'THE CRITIC', 'BECAME A CHARACTER', 'pink'), quote(3.4, 2.6, 'That is not a studio asking for permission.', 'Commentary', 'ink')], 'violet', 'Commentary', 'ANALYSIS')
paper(T(12), 'sj', 'mid', 'mid', 'SUPERJUMP · GTA IV’s “Statue of Happiness”', 'ANALYSIS', [big(0.3, 3.6, 'HOT COFFEE → COFFEE CUP', 'the Statue of Happiness', 'amber')], hl=False)
still(T(12, 4.2), STAT[1], 'Photo: Daniel Schwen · Wikimedia Commons · public domain per Commons · the real Statue of Liberty (context)', 'CONTEXT', [], b0=(.5, .5, 1), b1=(.5, .46, .85))
still(T(13), STAT[0], 'Photo: William Warby · Wikimedia Commons · CC BY 2.0 · the real Statue of Liberty (context)', 'CONTEXT', [word(0.0, 1.5, 'SUBTLE?', 'pink')], tr='flash', b0=(.5, .5, 1), b1=(.5, .5, .88))
clip(T(14), G5, 200, CG5, co=[big(0.3, 3.2, 'JOCK CRANLEY', '≈ SCHWARZENEGGER PARODY (ANALYSIS)', 'teal')], tr='dip')
clip(T(14, 3.5), G5, 192, CG5)
paper(T(15), 'sj', 'right', 'right', 'SUPERJUMP · LifeInvader in GTA V', 'ANALYSIS', [big(0.2, 3.8, 'LIFEINVADER', '= FACEBOOK, SERIAL NUMBERS FILED OFF', 'teal')], hl=False)
clip(T(16), G5, 156, CG5, co=[big(1.5, 2.6, 'NOBODY WAS SAFE', 'including Rockstar itself', 'pink')], z=(1.0, .92))
clip(T(18), G5, 188, CG5, co=[big(0.3, 3.0, 'PICK A TARGET.', 'AIM. FIRE.', 'pink')], tr='flash')
clip(T(19), G5, 216, CG5, co=[word(0.2, 3.0, 'TEETH', 'amber')], z=(1.0, .93))
# ---- C. modern Rockstar
still(T(20), shot(38), CP, co=[big(0.1, 2.0, 'MODERN ROCKSTAR', None, 'pink')], tr='dip', b0=(.5, .5, 1), b1=(.5, .5, .85))
clip(T(21), RDR, 0, 'Red Dead Redemption 2 clip · supplied by you', 'REPORTED', [big(0.2, 5.2, '2018 · “100-HOUR WEEKS”', 'Dan Houser · reported by GameSpot', 'amber')], z=(1.0, .92))
kin(T(22), [big(0.2, 4.6, 'A FOUR-PERSON TEAM', 'THREE WEEKS, NOT YEARS', 'teal')], 'teal', 'Houser’s later clarification, as reported by GameSpot (Oct 2018)', 'REPORTED')
clip(T(24), L, 4, CL, co=[big(0.2, 3.2, 'HOW THE LEGEND WAS BUILT', None, 'pink')], z=(1.0, .94))
# ---- D. the dispute (reporting and evidence)
paper(T(25), 'pcg1', 'wide', 'wide', 'PC Gamer · Andy Chalk · 11 Dec 2025', 'REPORTED', [big(0.1, 1.9, 'OCTOBER 2025', None, 'red')], tr='dip', hl=False)
paper(T(26), 'pcg1', 'wide', 'head', 'PC Gamer · Andy Chalk · 11 Dec 2025', 'REPORTED', [big(0.4, 3.5, '30+ DISMISSED', 'reported figure', 'amber')])
paper(T(27), 'pcg1', 'head', 'by', 'PC Gamer · 11 Dec 2025 · The Register · 6 Nov 2025', 'REPORTED', [big(0.2, 3.2, 'NUMBER NEVER CONFIRMED', '“a small number of individuals”', 'amber')], hl=False)
paper(T(28), 'pcg1', 'head', 'head', 'Rockstar’s statement · PC Gamer, 11 Dec 2025', 'ROCKSTAR RESPONSE', [quote(0.3, 6.0, 'sharing confidential information in a public forum', 'ROCKSTAR’S STATEMENT', 'teal')])
paper(T(29), 'pcg1', 'sub', 'sub', 'Rockstar’s statement · The Register, 6 Nov 2025', 'ROCKSTAR RESPONSE', [quote(0.3, 5.8, '“This was in no way related to people’s right to join a union or engage in union activities.”', 'ROCKSTAR’S STATEMENT', 'teal')], hl=False)
paper(T(30), 'pcg2', 'wide', 'prot', 'PC Gamer · Lincoln Carpenter · 17 Jun 2026 (IWGB protest image)', 'UNION CLAIM', [quote(0.3, 3.6, '“plain and simple union busting”', 'IWGB · A CLAIM', 'amber')], hl=False)
paper(T(30, 4.2), 'pcg2', 'prot', 'prot', 'PC Gamer · 17 Jun 2026', 'UNION CLAIM', [big(0.2, 3.4, 'THE FORUM?', 'IWGB says: a private Discord', 'amber')], hl=False)
paper(T(31), 'pcg2', 'wide', 'head', 'PC Gamer · 17 Jun 2026', 'CONFIRMED', [big(0.2, 1.4, 'WHAT WE KNOW', None, 'teal')])
paper(T(32), 'pcg2', 'head', 'head', 'IWGB filing · 12 Nov 2025', 'CONFIRMED', [big(0.2, 4.8, 'NOV 12, 2025 · CLAIMS FILED', 'victimisation · collective dismissal · blacklisting', 'teal')])
paper(T(33), 'tr', 'wide', 'head', 'TechRadar · Demi Williams · 13 Jan 2026', 'CONFIRMED', [big(0.3, 4.4, 'JAN 2026 · INTERIM RELIEF REFUSED', None, 'teal')])
paper(T(34), 'tr', 'sub', 'sub', 'TechRadar · 13 Jan 2026', 'CONFIRMED', [big(0.2, 1.8, 'NOT A FINAL RULING', None, 'red')], hl=False)
paper(T(35), 'pcg2', 'date', 'head', 'PC Gamer · 17 Jun 2026', 'CONFIRMED', [big(0.3, 3.4, 'JUN 2026 · CLAIMS NOT STRUCK OUT', 'blacklisting claims go to trial', 'teal')])
kin(T(36), [big(0.2, 3.4, 'NOV 17–18, 2026', 'CLOSING ARGUMENTS · GLASGOW', 'teal')], 'teal', 'ITV News, 18 Nov 2026 (page not capturable)', 'CONFIRMED')
kin(T(37), [quote(0.2, 3.4, '“caught red-handed”', 'ROCKSTAR’S LAWYER · ITV NEWS', 'teal')], 'teal', 'ITV News, 18 Nov 2026', 'ROCKSTAR RESPONSE')
kin(T(38), [big(0.2, 4.4, '~10%', 'union membership when the dismissals came — claimants’ lawyers', 'amber')], 'amber', 'Reported by TechTimes, 19 Nov 2026 · an allegation, untested', 'CLAIM')
paper(T(39), 'pcg2', 'wide', 'head', 'PC Gamer · Lincoln Carpenter · 17 Jun 2026', 'REPORTED', [big(0.1, 1.4, 'THOSE ARE CLAIMS.', None, 'ink')], tr='flash', hl=False)
kin(T(40), [big(0.3, 5.0, 'NO JUDGMENT YET', 'the judge gave no timeframe', 'red')], 'red', 'ITV News, 18 Nov 2026', 'DISPUTED')
paper(T(41), 'tr', 'head', 'head', 'TechRadar · 13 Jan 2026', 'DISPUTED', [big(0.3, 3.8, 'MOTIVE: UNPROVEN', 'a judge will decide', 'red')], hl=False)
clip(T(43), L, 12, CL, co=[big(0.3, 3.5, 'THE BIGGEST GAME OF ITS LIFE', None, 'pink')], tr='dip')
paper(T(44, 5.0), 'aj', 'head', 'sub', 'Al Jazeera · 19 Nov 2026', 'CONFIRMED', [big(0.3, 3.5, 'THE GAME IS OUT', 'a union vote is reported under way (TechTimes)', 'amber')], hl=True)
clip(T(45), L, 16, CL, co=[big(0.3, 3.0, 'NOT EXACTLY “WE DON’T TAKE OURSELVES SERIOUSLY”', None, 'pink')])
# ---- E. the voice
kin(T(46), [big(0.1, 1.7, 'THE VOICE CHANGED', None, 'pink')], 'pink', tr='dip')
clip(T(47), G5, 150, 'GTA V trailer · Rockstar Games · generic footage, not the shelved mode', 'REPORTED', [big(0.3, 4.6, 'SUMMER 2020 · COPS ’N’ CROOKS', 'reportedly shelved · Bloomberg, 27 Jul 2022', 'amber')])
clip(T(47, 5.2), G5, 116, CG5, 'REPORTED', [big(0.2, 3.8, 'OVER HOW IT WOULD LOOK', 'during the policing debate', 'amber')])
kin(T(48), [big(0.2, 2.8, 'UNNAMED SOURCES', 'reported by Bloomberg', 'amber')], 'amber', 'Bloomberg, 27 Jul 2022', 'REPORTED')
clip(T(49), G5, 28, CG5, co=[big(0.2, 1.6, 'CAREFUL IS ALLOWED.', None, 'ink')])
clip(T(50), G5, 176, CG5, co=[big(0.2, 3.4, 'THE OLD ROCKSTAR', 'WASN’T CAREFUL', 'pink')], z=(1.0, .93))
# ---- F. GTA VI
still(T(51), art(8), 'GTA VI key art · Rockstar Games press kit', co=[big(0.1, 2.0, 'GRAND THEFT AUTO VI', None, 'pink')], tr='dip', b0=(.5, .5, 1), b1=(.5, .5, .88))
paper(T(52), 'aj', 'wide', 'head', 'Al Jazeera · 19 Nov 2026', 'CONFIRMED', [big(0.3, 3.0, 'OUT NOV 19, 2026', 'METACRITIC 99 · 150+ REVIEWS', 'teal')])
clip(T(53), L, 24, CL, co=[big(0.2, 2.2, 'REVIEWS ARE NOT THE QUESTION', None, 'ink')], tr='dip')
clip(T(54), L, 28, CL, co=[word(0.1, 2.0, 'IS IT FUNNY?', 'pink')])
paper(T(55), 'gr', 'wide', 'head', 'GamesRadar · Jordan Gerblick · 28 Aug 2026', 'CONFIRMED', [big(0.3, 3.4, 'ROB NELSON', 'ROCKSTAR NORTH CO-STUDIO HEAD', 'teal')])
paper(T(55, 4.0), 'gr', 'head', 'quote', 'GamesRadar · 28 Aug 2026', 'CONFIRMED', [quote(0.2, 5.6, '“We have to be careful that what we’re choosing to satirize is not going to feel dated.”', 'ROB NELSON', 'teal')], hl=False)
paper(T(56), 'wccf', 'wide', 'head', 'Wccftech · Alessio Palumbo · 5 Oct 2026, relaying Love Magazine', 'REPORTED', [big(0.3, 3.4, 'RUPERT HUMPHRIES', 'ROCKSTAR SVP, NARRATIVE', 'teal')])
paper(T(56, 4.6), 'wccf', 'head', 'img', 'Wccftech · 5 Oct 2026 · original Love Magazine interview not seen', 'REPORTED', [quote(0.2, 4.0, '“you could just go outside and live in the real world”', 'RUPERT HUMPHRIES · REPORTED', 'teal')], hl=False)
still(T(57), shot(23), CP, co=[word(0.0, 0.75, 'SMART?', 'teal')], tr='flash', b0=(.5, .5, 1), b1=(.5, .5, .9))
still(T(58), shot(13), CP, co=[word(0.0, 0.7, 'SURE.', 'ink')], tr='flash', b0=(.55, .5, .9), b1=(.5, .5, .8))
still(T(59), shot(95), CP, co=[word(0.0, 0.7, 'SAFE?', 'amber')], tr='flash', b0=(.5, .5, 1), b1=(.5, .5, .88))
still(T(60), shot(12), CP, co=[word(0.0, 1.0, 'ALSO YES.', 'pink')], tr='flash', b0=(.5, .5, .9), b1=(.5, .5, .8))
paper(T(61), 'wccf', 'img', 'cap', 'Wccftech · 5 Oct 2026 · relaying Love Magazine', 'REPORTED', [big(0.3, 4.2, 'NO REAL PEOPLE OR TRENDS', 'reportedly · not verified against the original', 'amber')], hl=False)
clip(T(62, 0.2), L, 32, CL, co=[big(0.3, 1.4, 'THAT’S A CHOICE.', None, 'ink')])
clip(T(64), L, 36, CL, co=[big(0.3, 3.4, 'SATIRE THAT NEVER NAMES ANYBODY', '… IS JUST A VIBE (OPINION)', 'pink')])
# ---- G. verdict
clip(T(65), L, 40, CL, co=[big(0.2, 1.8, 'SO DID ROCKSTAR CHANGE?', None, 'ink')], tr='dip')
paper(T(66), 'gx', 'head', 'head', 'Gameranx · 10 Oct 2025 · fan reaction is opinion', 'OPINION', [big(0.1, 1.5, 'FANS SAY', 'the humor got safer', 'amber')], hl=False)
paper(T(67), 'pcg2', 'prot', 'prot', 'PC Gamer · 17 Jun 2026', 'UNION CLAIM', [big(0.1, 2.4, 'WORKERS SAY', 'harder on the people who build the games', 'amber')], hl=False)
paper(T(67, 3.8), 'pcg1', 'head', 'head', 'PC Gamer · 11 Dec 2025', 'ROCKSTAR RESPONSE', [big(0.1, 3.4, 'ROCKSTAR SAYS', 'it acted on confidential leaks', 'teal')], hl=False)
clip(T(68), AJ, 6, CGP, co=[big(0.2, 3.5, 'MAYBE THE GAME IS BRILLIANT', None, 'ink')])
clip(T(69), BF, 40, CGP, co=[big(0.1, 1.7, 'MAYBE IT STILL HAS BITE', None, 'pink')])
clip(T(70, 0.4), DJ, 58, CGP, co=[big(0.1, 1.2, 'I CAN’T TELL YOU THAT.', None, 'ink')])
clip(T(71), G5, 272, CG5, co=[big(0.3, 3.6, 'A LEGEND BUILT BY THROWING PUNCHES', None, 'pink')], z=(1.0, .92))
still(T(72), art(8), 'GTA VI key art · Rockstar Games press kit', co=[big(0.2, 4.6, 'DID ROCKSTAR CHANGE FOR THE WORSE?', 'OR ARE WE JUST OLDER?', 'pink')], tr='dip', b0=(.5, .5, .95), b1=(.5, .5, .8))
# ---- extra shots to keep the picture moving (added after the first density check)
paper(T(7, 6.4), 'sj', 'wide', 'head', 'SUPERJUMP · J. Barnes · 11 Dec 2025 · 27 years of GTA parodies', 'ANALYSIS', [], hl=False)
paper(T(33, 4.4), 'tr', 'sub', 'head', 'TechRadar · 13 Jan 2026', 'CONFIRMED', [big(0.2, 3.6, 'NOT “LIKELY” THAT UNION', 'MEMBERSHIP WAS THE PRINCIPAL REASON', 'amber')], hl=False)
clip(T(44, 3.2), PRE, 2, CL, co=[big(0.2, 1.8, 'AND A UNION VOTE…', None, 'amber')])
paper(T(55, 4.4), 'gr', 'quote', 'head', 'GamesRadar · 28 Aug 2026', 'CONFIRMED', [], hl=False)
P.sort(key=lambda s: s['t'])
for i, s in enumerate(P): s['end'] = P[i + 1]['t'] if i + 1 < len(P) else DUR; s['id'] = i
