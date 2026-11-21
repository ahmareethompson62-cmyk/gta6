"""Edit decision list: every segment = (t0, t1, base, cardspec). Times from narration sentence alignment (notes/sents.json).
base: None -> solid card bg | ('T',) next trailer footage | ('T','blur') | ('F', key, in_sec) fixed footage
Run: python3 edl.py  -> prints coverage check."""
import json, os
P = '/home/claude/project'
S_ = json.load(open(P + '/notes/sents.json'))
END = 514.10
def s(i): return S_[i]['start'] if i < len(S_) else END
def e(i): return S_[i]['end'] if i < len(S_) - 1 else END
def st(i): return s(i)

CREDIT = {
 'T': 'Rockstar Games: Grand Theft Auto VI trailers (official)',
 'RDR2': 'Red Dead Redemption 2, Rockstar Games (your capture)',
 'WANTED': 'GTA 6 gameplay clip supplied by user (creator not identified)',
 'DOG': 'GTA 6 gameplay clip supplied by user (creator not identified)',
 'TREE': 'GTA 6 gameplay clip supplied by user (creator not identified)',
}
def B(*a): return list(a)
def T(t): return ('text', t, 0, 0, 0)

def tx(t, size=84, wt='Black', c='ink'): return ('text', t, size, wt, c)
def gap(n=30): return ('gap', n)
def stamp(t, c='amber', size=80): return ('stamp', t, size, c)

SEG = []
def add(t0, t1, base=None, **card): SEG.append(dict(t0=t0, t1=t1, base=base, card=card))

# ---------------- COLD OPEN ----------------
add(0, s(1), None, blocks=[tx('GTA 5 · 2013', 54, 'Bold', 'dim'), gap(10), tx('$59.99', 230, 'Black', 'ink')], chip='Standard edition, launch price (context)')
add(s(1), s(2), ('T',), scrim=120, blocks=[tx('GTA 6', 54, 'Bold', 'dim'), gap(10), tx('$79.99', 230, 'Black', 'pink')], status='CONFIRMED', chip='Rockstar pricing, June 2026 (Engadget)', credit=CREDIT['T'])
add(s(2), s(3), None, blocks=[tx('GTA 5', 54, 'Bold', 'dim'), gap(10), tx('A DISC', 200, 'Black', 'ink')])
add(s(3), s(4), ('T',), scrim=120, blocks=[tx('GTA 6', 54, 'Bold', 'dim'), gap(10), tx('A BOX', 150, 'Black', 'pink'), tx('WITH A CODE', 100, 'Black', 'ink')], status='CONFIRMED', chip='No disc: download code in a box (Engadget)', credit=CREDIT['T'])
add(s(4), s(5), None, blocks=[tx('GTA 5', 54, 'Bold', 'dim'), gap(10), tx('ONLINE', 130, 'Black', 'ink'), tx('~2 WEEKS LATER', 100, 'Black', 'teal')], chip='Context: Dexerto')
add(s(5), s(6), ('T',), scrim=120, blocks=[tx('GTA 6', 54, 'Bold', 'dim'), gap(10), stamp('NO DATE', 'pink', 150)], chip='No online mode announced (GamesRadar)', credit=CREDIT['T'])
add(s(6), s(7), None, blocks=[tx('GTA 5', 54, 'Bold', 'dim'), gap(10), tx('30', 330, 'Black', 'ink'), tx('FRAMES PER SECOND', 56, 'Bold', 'dim')])
add(s(7), s(8), ('T',), scrim=120, blocks=[tx('GTA 6', 54, 'Bold', 'dim'), gap(10), tx('30', 330, 'Black', 'pink'), tx('FRAMES PER SECOND', 56, 'Bold', 'dim')], status='REPORTED', chip='Digital Foundry analysis; Rockstar tech leads', credit=CREDIT['T'])
add(s(8), s(9), None, blocks=[tx('SOME BOXES REPORTEDLY ARRIVE', 76, 'Black', 'ink'), tx('WITH THE CODE ALREADY USED', 76, 'Black', 'amber'), gap(30), tx('Dexerto citing Twisted Voxel · Nov 15 · Rockstar has not confirmed scale', 36, 'Medium', 'dim')], status='REPORTED')
add(s(9), s(11), ('T',), scrim=110, blocks=[tx('99', 420, 'Black', 'teal'), tx('METACRITIC · BEST-REVIEWED GAME LISTED', 54, 'Bold', 'ink')], chip='Metacritic: about 150 critic reviews, none negative at last read', status='REPORTED', credit=CREDIT['T'])
add(s(11), s(12), ('T',), scrim=110, blocks=[tx('NOT ONE NEGATIVE REVIEW', 90, 'Black', 'ink'), tx('(at last count, Metacritic)', 44, 'Medium', 'dim')], status='REPORTED', credit=CREDIT['T'])
add(s(12), s(13), ('T', 'blur'), scrim=150, blocks=[tx('“the single most impressive video game I have ever played.”', 78, 'Black', 'ink'), gap(30), tx('IGN review', 50, 'Bold', 'teal')], status='REPORTED', chip='Quoted from IGN review as reported by Endgame Tools', credit=CREDIT['T'])
add(s(13), s(15), ('T',), scrim=0, blocks=[], credit=CREDIT['T'])
add(s(15), s(17), None, blocks=[tx('EVERYTHING AROUND IT', 100, 'Black', 'ink'), gap(30), tx('REVIEWS  ·  PREVIEWS  ·  ROCKSTAR ANNOUNCEMENTS', 46, 'Bold', 'teal'), gap(20), tx('what you get, and what you don’t', 50, 'Medium', 'dim')])
add(s(17), s(20), ('T', 'blur'), scrim=150, blocks=[stamp('99 ?', 'teal', 260), gap(30), tx('Why this number can’t settle the question. Hold onto that.', 50, 'Bold', 'ink')])
add(s(20), s(22), None, blocks=[tx('CRITICS SCORED THE GAME.', 96, 'Black', 'ink'), tx('NOBODY SCORED THE DEAL.', 96, 'Black', 'pink'), gap(40), tx('GTA 6 MIGHT BE WORSE THAN WE THOUGHT', 40, 'Bold', 'dim')])
# ---------------- 1 THIRTY ----------------
add(s(22), s(24), None, blocks=[tx('30', 700, 'Black', 'ink')], tag='01 · THIRTY')
add(s(24), s(25), ('T',), scrim=60, blocks=[tx('NATIVE 1440p', 80, 'Black', 'ink'), tx('LOCKED NEAR 30 FPS', 80, 'Black', 'teal'), tx('rare single-frame drops', 44, 'Medium', 'dim')], status='REPORTED', chip='Digital Foundry analysis of the Extended Look (via TechRadar)', credit=CREDIT['T'])
add(s(25), s(27), None, blocks=[tx('30 FPS:', 150, 'Black', 'ink'), tx('DISAPPOINTING?', 150, 'Black', 'amber'), gap(30), tx('Dot Esports review roundup', 48, 'Bold', 'dim')], status='REPORTED')
add(s(27), s(28), None, blocks=[tx('“occasional performance drops”', 92, 'Black', 'ink'), gap(30), tx('Noisy Pixel · 9 / 10', 54, 'Bold', 'teal')], status='REPORTED', chip='Via Endgame Tools roundup')
add(s(28), s(30), ('T',), scrim=90, blocks=[tx('THIRTY.', 170, 'Black', 'ink'), tx('SOMETIMES LESS.', 120, 'Black', 'amber')], credit=CREDIT['T'])
add(s(30), s(32), None, blocks=[tx('FAIR IS FAIR', 130, 'Black', 'ink'), tx('this is Rockstar tradition', 64, 'Bold', 'teal')])
# checklist reveal split into 3
a, b = s(32), e(32); d3 = (b - a) / 3
rows = [('GTA 4', '30 FPS', 'teal'), ('GTA 5', '30 FPS', 'teal'), ('RED DEAD REDEMPTION 2', '30 FPS', 'teal')]
for k in range(3):
    add(a + k * d3, a + (k + 1) * d3, ('F', 'RDR2', 0.0), scrim=170, blocks=[tx('ALL LAUNCHED AT 30 ON CONSOLE', 56, 'Bold', 'dim'), gap(30), ('rows', rows[:k + 1], 110)], maxw=1100, status='CONTEXT', chip='Games.gg', credit=CREDIT['RDR2'])
add(s(33), s(35), None, blocks=[tx('THE REASON IS THE PROCESSOR', 76, 'Black', 'ink'), gap(30), ('rows', [('PS5 base CPU', '1.00x', 'ink'), ('PS5 Pro CPU', '≈1.07x', 'amber')], 120), gap(20), tx('about 7% faster in CPU-limited cases (Digital Foundry via TweakTown)', 36, 'Medium', 'dim')], maxw=1300, status='REPORTED', chip='Explanatory graphic (original design)')
add(s(35), s(37), ('T',), scrim=60, blocks=[tx('A TRADE:', 110, 'Black', 'ink'), tx('DETAIL OVER SMOOTHNESS', 110, 'Black', 'pink')], credit=CREDIT['T'])
add(s(37), s(38), None, blocks=[tx('THE SAME TRADE', 110, 'Black', 'ink'), tx('WITH YOUR WALLET', 110, 'Black', 'pink')])
# ---------------- 2 EIGHTY ----------------
add(s(38), s(39), None, blocks=[tx('STANDARD EDITION', 54, 'Bold', 'dim'), tx('$79.99', 340, 'Black', 'ink')], tag='02 · EIGHTY', status='CONFIRMED', chip='Engadget')
add(s(39), s(40), None, blocks=[tx('ULTIMATE EDITION', 54, 'Bold', 'dim'), tx('$99.99', 340, 'Black', 'pink')], status='CONFIRMED', chip='Engadget')
add(s(40), s(41), None, blocks=[tx('ANNOUNCED', 60, 'Bold', 'dim'), tx('JUNE 2026', 200, 'Black', 'ink')], status='CONFIRMED', chip='Engadget · Fortune')
add(s(41), s(43), None, blocks=[('rows', [('GTA 5 (2013)', '$59.99', 'ink'), ('GTA 6 (2026)', '$79.99', 'pink'), ('DIFFERENCE', '+$20', 'amber')], 150)], maxw=1200, chip='Standard edition prices')
add(s(43), s(45), ('T', 'blur'), scrim=140, blocks=[tx('CREDIT WHERE IT’S DUE', 110, 'Black', 'ink'), tx('Multiple outlets: lower than feared', 56, 'Bold', 'teal')], status='REPORTED', chip='Engadget · Stuff.tv', credit=CREDIT['T'])
add(s(45), s(46), None, blocks=[tx('“exactly where its leverage lets it.”', 96, 'Black', 'ink'), gap(30), tx('Joost van Dreunen, analyst', 52, 'Bold', 'teal')], status='REPORTED', chip='GameDev.net')
add(s(46), s(49), None, blocks=[tx('THE LEVERAGE IS THE POINT', 70, 'Black', 'ink'), gap(30), ('rows', [('Mario Kart World', 'raised standard price', 'amber'), ('Microsoft, 2025', 'tried $80, backed down', 'amber'), ('GTA 6', '$79.99', 'pink')], 110)], maxw=1500, status='REPORTED', chip='Fortune · TechSpot')
add(s(49), s(52), ('T', 'blur'), scrim=150, blocks=[tx('EIGHTY STOPS BEING A PRICE.', 90, 'Black', 'ink'), tx('IT BECOMES AN ARGUMENT.', 90, 'Black', 'pink')], credit=CREDIT['T'])
add(s(52), s(55), None, blocks=[stamp('NO DISC', 'pink', 200), gap(30), tx('A BOX. WITH A CODE IN IT.', 64, 'Bold', 'ink')], status='CONFIRMED', chip='Engadget', credit='Explanatory graphic (original design)')
add(s(55), s(56), None, blocks=[tx('“the difference between physical and digital is the box.”', 70, 'Black', 'ink'), gap(20), tx('Engadget, paraphrased', 44, 'Bold', 'dim')], status='REPORTED')
# ---------------- 3 THE CODE ----------------
add(s(56), s(58), ('T', 'blur'), scrim=170, blocks=[tx('A CODE IN A BOX', 120, 'Black', 'ink'), tx('HAS ONE WEAKNESS', 80, 'Black', 'pink'), tx('the code has to be in the box', 48, 'Medium', 'dim')], tag='03 · THE CODE', credit=CREDIT['T'])
add(s(58), s(59), None, blocks=[tx('BUYERS POSTED:', 54, 'Bold', 'dim'), tx('NO CODE, OR AN ALREADY-REDEEMED ONE', 80, 'Black', 'ink'), tx('from Nov 13', 44, 'Medium', 'dim')], status='REPORTED', chip='Dexerto, citing Twisted Voxel')
add(s(59), s(60), None, blocks=[tx('NAMED IN THE REPORT', 54, 'Bold', 'dim'), gap(20), ('rows', [('GameStop', '', 'amber'), ('Best Buy', '', 'amber'), ('Rockstar’s own store', '', 'amber')], 100)], maxw=1100, status='REPORTED', chip='Dexerto, Nov 15')
add(s(60), s(61), None, blocks=[tx('SOME SAY SUPPORT', 70, 'Black', 'ink'), tx('SAID NO, OR CLOSED THE TICKET', 70, 'Black', 'amber')], status='REPORTED')
add(s(61), s(63), None, blocks=[tx('HOW MANY?', 170, 'Black', 'ink'), gap(20), stamp('UNKNOWN', 'amber', 90)])
add(s(63), s(64), None, blocks=[stamp('NOT CONFIRMED', 'amber', 120), gap(30), tx('Rockstar hasn’t confirmed a widespread problem', 56, 'Bold', 'ink')])
add(s(64), s(66), None, blocks=[tx('CODES READABLE THROUGH SEALED BOXES?', 74, 'Black', 'ink'), gap(20), tx('a viral theory', 48, 'Medium', 'dim')], status='RUMOUR', chip='Dexerto')
add(s(66), s(67), None, blocks=[stamp('RUMOUR', 'red', 240), gap(20), tx('Kotaku’s editor-in-chief couldn’t make it work', 50, 'Bold', 'ink')])
add(s(67), s(70), ('T', 'blur'), scrim=160, blocks=[tx('NO DISC. NO FALLBACK.', 100, 'Black', 'ink'), tx('A CODE IN A BOX.', 130, 'Black', 'pink')], credit=CREDIT['T'])
add(s(70), s(71), ('T',), scrim=60, blocks=[], credit=CREDIT['T'])
# ---------------- 4 LATER ----------------
add(s(71), s(74), None, blocks=[tx('HOW ONLINE ARRIVED', 56, 'Bold', 'dim'), gap(20), ('rows', [('GTA 5 · Sep 2013', 'Online ~2 weeks later', 'teal'), ('Red Dead 2', 'Online ~1 month later', 'teal'), ('GTA 6 · Nov 2026', 'single-player only', 'pink')], 120)], maxw=1500, tag='04 · LATER', status='CONFIRMED', chip='Context: Dexerto · GamesRadar')
add(s(74), s(76), None, blocks=[tx('LAUNCHED AS A', 70, 'Bold', 'dim'), tx('SINGLE-PLAYER GAME', 130, 'Black', 'ink'), tx('Rockstar and Take-Two both describe it that way', 44, 'Medium', 'dim')], status='CONFIRMED', chip='GamesRadar')
add(s(76), s(77), None, blocks=[tx('WHAT ABOUT ONLINE?', 140, 'Black', 'ink')])
add(s(77), s(78), None, blocks=[tx('GTA Online support continues', 56, 'Bold', 'dim'), tx('“after GTA 6 release and beyond.”', 90, 'Black', 'ink'), gap(20), tx('Take-Two, Sept shareholder meeting (ResetEra transcript)', 40, 'Medium', 'teal')], status='REPORTED', chip='TechRadar')
add(s(78), s(79), None, blocks=[tx('TAKE-TWO ISN’T PLANNING', 70, 'Black', 'ink'), tx('TO TALK ABOUT NEW ONLINE SOON', 70, 'Black', 'ink'), gap(20), tx('Jason Schreier, Bloomberg', 50, 'Bold', 'teal')], status='REPORTED', chip='Notebookcheck')
add(s(79), s(80), None, blocks=[tx('“A YEAR OR TWO AWAY”', 110, 'Black', 'ink'), gap(20), tx('Paul Tassi, Forbes', 50, 'Bold', 'violet')], status='PREDICTION', chip='Notebookcheck')
add(s(80), s(83), None, blocks=[tx('NOT CANCELLED.', 120, 'Black', 'ink'), tx('JUST LATER.', 160, 'Black', 'pink')])
add(s(83), s(84), None, blocks=[stamp('NO DATE', 'pink', 220)])
add(s(84), s(86), None, blocks=[tx('LATER.', 330, 'Black', 'pink')])
# ---------------- 5 RAILS ----------------
add(s(86), s(88), None, blocks=[tx('FOR YEARS, THE CRITICISM WAS THE SAME', 70, 'Bold', 'dim'), gap(10), tx('DO EXACTLY WHAT THE GAME WANTS,', 90, 'Black', 'ink'), tx('OR FAIL.', 150, 'Black', 'red')], tag='05 · RAILS')
add(s(88), s(89), ('T', 'blur'), scrim=150, blocks=[tx('ROB NELSON, ROCKSTAR NORTH, TO IGN:', 50, 'Bold', 'dim'), tx('MORE FLEXIBLE MISSIONS', 110, 'Black', 'ink')], status='PRE-LAUNCH CLAIM', chip='Notebookcheck', credit=CREDIT['T'])
add(s(89), s(90), ('T',), scrim=130, blocks=[tx('PREVIEWS: SEVERAL APPROACHES', 80, 'Black', 'ink'), tx('AND ESCAPE ROUTES', 80, 'Black', 'teal')], status='REPORTED', chip='TechSpot', credit=CREDIT['T'])
add(s(90), s(91), None, blocks=[tx('THEN THE REVIEWS CAME IN', 120, 'Black', 'ink')])
add(s(91), s(93), None, blocks=[('cols', [tx('PROMISED', 70, 'Black', 'teal'), gap(20), tx('Missions with options and escape routes', 50, 'Bold', 'ink')], [tx('IN REVIEWS', 70, 'Black', 'amber'), gap(20), tx('Restrictive missions, pacing issues, occasional control problems', 50, 'Bold', 'ink')])], maxw=1650, status='REPORTED', chip='Dot Esports roundup · Noisy Pixel (“uneven storytelling”)')
add(s(93), s(97), None, blocks=[tx('BOTH CAN BE TRUE', 130, 'Black', 'ink'), gap(30), tx('Options in one mission. A rail in another.', 56, 'Bold', 'dim'), gap(10), tx('Reviewers have different tolerances.', 56, 'Bold', 'dim')])
add(s(97), s(99), None, blocks=[tx('RAILS.', 330, 'Black', 'red')])
# ---------------- 6 FRICTION ----------------
add(s(99), s(100), ('T',), scrim=90, blocks=[tx('A WORLD BUILT TO PUNISH IMPROVISING', 90, 'Black', 'ink')], tag='06 · FRICTION', credit=CREDIT['T'])
w0 = 66.0
for (i, j, line, c) in [(100, 102, 'THE WANTED SYSTEM IS REBUILT: SIX STARS', 'ink'), (102, 103, 'A CRIME HAS TO BE WITNESSED', 'ink'), (103, 104, 'COPS BUILD A DESCRIPTION: FACE · CLOTHES · VEHICLE', 'amber')]:
    add(s(i), s(j), ('F', 'WANTED', w0 + (s(i) - s(100))), bgmode='lower', scrim=0, blocks=[], caption=line, status='REPORTED', chip='TechSpot · GTA Intel', credit=CREDIT['WANTED'])
add(s(104), s(105), ('F', 'WANTED', w0 + (s(104) - s(100))), scrim=0, caption='HIDING ON THE MINIMAP: REPORTEDLY NO LONGER WORKS', status='REPORTED', chip='GTA Intel', credit=CREDIT['WANTED'])
add(s(105), s(108), ('T',), scrim=60, caption='CAR THEFT IS A SYSTEM: SECURITY TIERS · STORY-UNLOCKED HARDWARE', status='REPORTED', chip='TechSpot (previews)', credit=CREDIT['T'])
add(s(108), s(110), None, blocks=[stamp('CASH GATE', 'amber', 170), gap(30), tx('Some story progress needs a set amount of cash', 60, 'Bold', 'ink')], status='REPORTED', chip='Previews: TechSpot · Exputer')
add(s(110), s(113), None, blocks=[tx('THE GOAL: YOU SHOULDN’T FEEL OVERPOWERED', 80, 'Black', 'ink'), gap(30), tx('Rob Nelson, Rockstar North (paraphrased)', 46, 'Bold', 'dim'), gap(30), tx('NOT A BUG. THE DESIGN.', 110, 'Black', 'pink')], maxw=1600, status='REPORTED', chip='TechSpot')
add(s(113), s(115), None, blocks=[tx('SIX REVIEWS WARN OF A LEARNING CURVE', 76, 'Black', 'ink'), tx('fragile cars · repair bills · daily chores', 56, 'Bold', 'teal'), gap(30), tx('One aggregator’s count: treat it as a hint', 44, 'Medium', 'dim')], status='LOW-RELIABILITY', chip='Output Lag roundup')
add(s(115), s(118), None, blocks=[('cols', [tx('LOVED GTA 5', 52, 'Bold', 'dim'), tx('AS A WRECKING BALL?', 52, 'Bold', 'dim'), gap(20), tx('WORSE', 140, 'Black', 'red')], [tx('WANTED', 52, 'Bold', 'dim'), tx('CONSEQUENCES?', 52, 'Bold', 'dim'), gap(20), tx('BETTER', 140, 'Black', 'teal')])], maxw=1650)
# ---------------- 7 FAST ROUND ----------------
add(s(118), s(119), None, blocks=[tx('FIVE MORE,', 150, 'Black', 'ink'), tx('QUICKLY', 150, 'Black', 'pink')], tag='07 · FAST ROUND')
add(s(119), s(121), None, blocks=[tx('TWO PATCHES BEFORE LAUNCH', 90, 'Black', 'ink'), tx('NO PATCH NOTES', 110, 'Black', 'amber')], status='REPORTED', chip='Red Bull')
add(s(121), s(122), None, blocks=[tx('NO PC VERSION', 150, 'Black', 'ink'), tx('ANNOUNCED', 150, 'Black', 'pink')], status='CONFIRMED', chip='GamesRadar')
add(s(122), s(123), None, blocks=[tx('NO SECOND-HAND', 140, 'Black', 'ink'), tx('VALUE ON A CODE', 140, 'Black', 'pink')], status='ANALYSIS')
add(s(123), s(125), None, blocks=[tx('NO 60 FPS', 220, 'Black', 'ink'), tx('reportedly', 60, 'Bold', 'amber')], status='REPORTED')
add(s(125), s(128), None, blocks=[stamp('RUMOUR', 'red', 170), gap(20), tx('PC could come sooner than expected', 70, 'Black', 'ink'), gap(10), tx('A report, not a Rockstar announcement. Unconfirmed.', 46, 'Medium', 'dim')], status='RUMOUR', chip='Dexerto / GamesBeat sources')
# ---------------- 8 THE 99 ----------------
add(s(128), s(129), ('T', 'blur'), scrim=150, blocks=[tx('BACK TO THE NUMBER', 120, 'Black', 'ink')], tag='08 · THE 99', credit=CREDIT['T'])
add(s(129), s(130), None, blocks=[tx('99', 520, 'Black', 'teal'), tx('METACRITIC', 60, 'Bold', 'ink')], status='REPORTED', chip='Metacritic (live numbers move)')
add(s(130), s(131), None, blocks=[tx('99', 520, 'Black', 'teal'), tx('OPENCRITIC', 60, 'Bold', 'ink')], status='REPORTED', chip='OpenCritic (live numbers move)')
add(s(131), s(132), None, blocks=[tx('TIED FOR THE TOP', 100, 'Black', 'ink'), tx('WITH OCARINA OF TIME', 70, 'Bold', 'dim')], status='REPORTED', chip='Endgame Tools · Technobezz')
add(s(132), s(136), ('T',), scrim=90, blocks=[tx('THE CRITICS WEREN’T WRONG.', 80, 'Black', 'ink'), tx('IS THE GAME GOOD?', 100, 'Black', 'teal'), tx('Probably, yes.', 60, 'Bold', 'dim')], credit=CREDIT['T'])
add(s(136), s(137), None, blocks=[tx('IS THE DEAL GOOD?', 150, 'Black', 'pink'), tx('the 99 doesn’t answer that', 56, 'Bold', 'dim')])
add(s(137), s(141), None, blocks=[('rows', [('Nov 18', 'Reviews published', 'ink'), ('Nov 19', 'Launch · codes opened', 'ink'), ('Nov 20', 'User scores open, 12:00 PT', 'amber')], 130)], maxw=1400, status='REPORTED', chip='Endgame Tools · Comic Shop Locator (verify)')
add(s(141), s(143), None, blocks=[tx('THE 99 IS A SCORE', 90, 'Black', 'ink'), tx('FOR THE GAME', 130, 'Black', 'teal')])
cb = [(s(143), 459.37, 'THIRTY'), (459.37, 460.16, 'EIGHTY'), (460.16, 461.7, 'A CODE IN A BOX'), (461.7, 462.15 + .0, 'RAILS'), (462.15, e(143), 'RAILS'), ]
cb = [(s(143), 459.37, 'NOT FOR', 'dim'), (459.37, 460.16, 'THIRTY', 'ink'), (460.16, 461.5, 'EIGHTY', 'ink'), (461.5, 462.15, 'A CODE IN A BOX', 'pink'), (462.15, 463.02, 'RAILS', 'red'), (463.02, s(144), 'LATER', 'pink')]
for a_, b_, t_, c_ in cb:
    add(a_, b_, None, blocks=[tx(t_, 260 if len(t_) < 8 else 170, 'Black', c_)])
# ---------------- ENDING ----------------
add(s(144), s(146), ('T', 'blur'), scrim=190, blocks=[tx('“the single most impressive video game I have ever played.”', 66, 'Black', 'ink'), gap(20), tx('IGN', 46, 'Bold', 'teal')], status='REPORTED', credit=CREDIT['T'])
add(s(146), s(147), None, blocks=[tx('IS GTA 6 WORSE THAN WE THOUGHT?', 90, 'Black', 'ink')])
add(s(147), s(148), None, blocks=[tx('THE GAME:', 60, 'Bold', 'dim'), tx('NO', 330, 'Black', 'teal')])
add(s(148), s(149), None, blocks=[tx('THE PACKAGE:', 60, 'Bold', 'dim'), tx('IN A FEW SPECIFIC WAYS, YES', 100, 'Black', 'pink')])
for i, t_ in [(149, 'THIRTY FRAMES'), (150, 'EIGHTY DOLLARS'), (151, 'A CODE IN A BOX'), (152, 'ONLINE, LATER'), (153, 'MISSIONS ON RAILS'), (154, 'A WORLD THAT FIGHTS BACK')]:
    add(s(i), s(i + 1), None, blocks=[tx(t_, 150, 'Black', 'ink' if i % 2 else 'pink')])
for i, t_ in [(155, 'GREAT UNTIL THE CODE’S ALREADY USED'), (156, 'GREAT UNTIL YOU WANT TO PLAY WITH FRIENDS'), (157, 'GREAT UNTIL A MISSION PUTS YOU ON A RAIL')]:
    add(s(i), s(i + 1), None, blocks=[tx(t_, 100, 'Black', 'ink')], maxw=1600)
mid = 496.3
add(s(158), mid, ('F', 'TREE', 60.0), scrim=0, caption='CREATOR CLIP: A FOREST ODDITY (UNVERIFIED)', credit=CREDIT['TREE'])
add(mid, s(159) + 0.0, ('F', 'DOG', 20.0), scrim=0, caption='CREATOR CLIP: A DOG ON A JET SKI', credit=CREDIT['DOG'])
add(s(159), s(161), ('F', 'DOG', 23.0), scrim=0, caption='NOBODY PLANNED THAT', credit=CREDIT['DOG'])
add(s(161), s(163), ('T', 'blur'), scrim=170, blocks=[tx('THIRTY FRAMES. EIGHTY DOLLARS.', 84, 'Black', 'ink'), tx('NO ONLINE.', 84, 'Black', 'ink'), tx('A FAIR PRICE FOR A 99?', 100, 'Black', 'pink'), gap(30), tx('PICK ONE. COMMENT BELOW.', 54, 'Bold', 'teal')], credit=CREDIT['T'])
add(s(163), s(165), None, blocks=[tx('PICK ONE.', 220, 'Black', 'ink'), tx('COMMENT BELOW.', 120, 'Black', 'teal')])
add(s(165), END, None, blocks=[tx('USER SCORES OPEN', 90, 'Black', 'ink'), tx('NOV 20 · 12:00 PT', 140, 'Black', 'pink'), gap(20), tx('Reported; I’ll check back then.', 48, 'Medium', 'dim')], status='REPORTED')

if __name__ == '__main__':
    SEG.sort(key=lambda x: x['t0'])
    prev = 0
    for g in SEG:
        if abs(g['t0'] - prev) > 0.002: print('GAP/OVERLAP', prev, g['t0'])
        prev = g['t1']
    print(len(SEG), 'segments; end', prev)
