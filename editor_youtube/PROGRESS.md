# PROGRESS: "GTA 6 Might Be Worse Than We Thought"  (updated 2026-11-20)
## State
- Research/script/angle: /home/claude/research/facts.md, /home/claude/script/{angle,script_with_visuals,script,script_elevenlabs}.* (done)
- Narration: assets/narration_declan_sage.mp3 (514.1 s, user's ElevenLabs; used as-is, not regenerated)
- Word/sentence timing: notes/sents.json (167 sentences, pocketsphinx ASR + alignment), notes/asr.json, notes/sil.json
- Edit plan: edl.py (113 segments covering 0-514.10 s; gap check: `python3 edl.py`)
- Cards: cards.py (original typeset graphics; statuses CONFIRMED/REPORTED/RUMOUR/etc.)
- Render: `python3 render.py cards|scenes|concat` (resumable; existing scenes/NNN.mp4 are skipped; delete a scene file to re-render it)
- Music: music.py -> out/music.wav (original synth, no third-party music; silences at 24.0-28.4 s and 491.3-497 s)
- Mix/mux: mix.sh -> out/GTA6_might_be_worse_v1.mp4 (never overwrite earlier renders; bump version)
## Settings
1920x1080, 30 fps, libx264 crf18 veryfast yuv420p, AAC 256k; voice loudnorm -16 LUFS, music ~-24 dB under voice.
## Footage map
Trailers (official, credited): cold open/price/chapter backgrounds. RDR2 clip: ch1 checklist. v19 airbase gameplay @66s (5 wanted stars): ch6. v22 dog jet-ski @15-24s and v23 tree figure @58s: easter-egg beat. Clips v18 (mud party, watermarked) unused.
## Excluded assets (reasons)
AI-generated box photo (Gemini watermark), Ocarina screenshot (is the 96 Switch 2 remake), unofficial price infographics/poster, screenshots of other sites (re-typeset instead). See assets/reference_not_used_on_screen/.
## Known issues / next steps
- Narration says "tomorrow" for user scores; it is now Nov 20 (stale). Needs re-record of s140 & s165 or accept.
- Clip creators unknown: confirm credits. v19/v22/v23 are 640x360 upscaled (soft).
- Mix checked by meters only (cannot listen).

## UPDATE (Nov 20, after final render)
- FINAL: out/GTA6_might_be_worse_v2_final.mp4 (1920x1080, 30 fps, 514.1 s, -15.9 LUFS, peak -1.0 dBFS). All 113 scenes rendered; trailer title-text frames avoided.
- Not done: re-record of stale "tomorrow" lines (s140, s165; cards show Nov 20 12:00 PT); ear-check of the mix; confirm clip creator credits; trailer cursor/footage reuse (about 86 s of trailer reused).
- To redo one scene: delete scenes/NNN.mp4, `python3 render.py scenes && python3 render.py concat && ./mix.sh <new name>`.

## v3 (Nov 20 evening): real-asset visual pass
- out/GTA6_might_be_worse_v3.mp4 (sha256 24f482a2...c415ec), render3.py + edl_v3.py (overrides on edl.py; v2 untouched). Signature-based re-render.
- New assets used: GTA5 Xbox360 box, GTA5 discs, Rockstar Store GTA VI page + code-in-box listing, Engadget 2013 headline, Games.gg 30fps, Dexerto headline/photo/paragraph, Metacritic page (99/152, user 5.2, $79.99 where to buy), TechPowerUp roundup, OpenCritic page, GTA5 gameplay trailer (30fps, Sept 17 end card, heist clip).
- Needs you: narration "tomorrow" lines now contradict the on-screen Metacritic user score 5.2 (Nov 20 capture). Extended Look not supplied: ch5-6 mostly still cards.
- Pushed to GitHub repo arking99854/GTA6-Documentary-Production /v3 as 2 parts + JOIN_ON_WINDOWS.bat.

## media_researcher (Nov 21)
Code: project/media_researcher/, workflow project/workflows/media-research.yml (live copy in repo ahmareethompson62-cmyk/gta6). Tested on runner: runs 44912724085, 44913098894 (crash-physics plan). See media_researcher/README.md.
