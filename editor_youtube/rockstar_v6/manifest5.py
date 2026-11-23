import json, re
spec = json.load(open('spec.json'))
rows = []
for e in spec['els']:
    m = re.search(r'<div class="src">(.*?)</div>', e['html'])
    if m: rows.append((e['t0'], m.group(1)))
rows.sort()
imgs = {}
for e in spec['els']:
    for u in re.findall(r"url\('([^']+)'\)", e['html']): imgs.setdefault(u.split('/')[-1], 0); imgs[u.split('/')[-1]] += 1
kinds = {'clips (gameplay in TV frames)': sum(1 for e in spec['els'] if e.get('clip')), 'article/page crops': sum(1 for e in spec['els'] if e.get('pan')), 'elements total': len(spec['els'])}
M = ["# Rockstar Has Changed — v5 (paper-cutout rebuild) source & attribution manifest", "",
"Runtime 293.25 s, 1920x1080 @30 fps, narration = your ElevenLabs file unchanged (loudness-normalised). Style follows the reference video you supplied (flat paper-cutout explainer: ransom-note tiles, torn paper, tape, stamps, TV/polaroid frames, animated diagrams). All motion is rendered from keyframes at sub-pixel precision (no zoompan shake).", "",
"## Counts", *[f"- {k}: {v}" for k, v in kinds.items()], "",
"## Licensing / approval notes",
"- **Dan Houser photo**: supplied by you in chat on 2026-11-22; identified as Dan Houser by you. Photographer/licence unknown to me; used on your instruction. Used at San Andreas and 2018 '100-hour weeks' / clarification sections.",
"- **Other people (Donald Love, Tom Goldberg, Jack Thompson, Rob Nelson, Rupert Humphries, Lazlow Jones)**: no photos supplied, so neutral silhouette cards with name labels are used. Send photos and they will replace the silhouettes.",
"- **Rockstar press-kit images (GTA VI)**: press page states no usage terms; used under your approval of 2026-11-21 ('Official Rockstar/publisher press media'). Licence not independently verified. Vice City still is GTA VI context, NOT the 2002 game.",
"- **GTA V trailer, GTA VI trailer/gameplay clips, RDR2 clip**: supplied by you earlier; uploader/licence unknown. One earlier render wrongly called a supplied clip 'official'; corrected. The bottom ~13% of each gameplay frame is cropped to hide burned-in foreign-language subtitles present in the supplied GTA V trailer.",
"- **Article screenshots (Gameranx, Al Jazeera, GamesRadar, PC Gamer x2, SUPERJUMP, TechRadar, Wccftech)**: approved by you 2026-11-22; credited on screen with outlet/author/date; copyright remains with publishers; shown as commentary/criticism.",
"- **Statue of Liberty photo**: William Warby, Wikimedia Commons, CC BY 2.0, labelled 'context'.",
"- **Illustrations (no source)**: 'GTA NEWS?' bubbles (labelled as illustration of reported replies, not quotes); redacted-document card (labelled illustration); icons/diagrams are original drawings. The Cops 'n' Crooks scene uses generic GTA V footage, labelled as such.",
"- **Not captured / unavailable**: ITV, IWGB, GameSpot, The Register, TechTimes pages (credited by text only), Bloomberg (paywalled). No footage of GTA III, Vice City, San Andreas or IV was available; those sections use SUPERJUMP page imagery and diagrams.", "",
"## Claims labelling", "Confirmed / reported / claim / opinion labels appear on screen as stamps and source chips (e.g. REPORTED, CONFIRMED, UNION CLAIM, ROCKSTAR RESPONSE, OPINION, UNPROVEN).", "",
"## On-screen credits by time", "| Time (s) | Credit chip |", "|---|---|", *[f"| {t:.1f} | {c} |" for t, c in rows], "",
"## Image files used (count of appearances)", *[f"- {k} ×{v}" for k, v in sorted(imgs.items())]]
open('../out/source_manifest_v5.md', 'w').write('\n'.join(M))
print(len(rows), 'credits', len(imgs), 'images')
