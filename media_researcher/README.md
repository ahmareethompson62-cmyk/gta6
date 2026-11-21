# media_researcher: autonomous research + media sourcing for gta-deep-dive

Plugs into the existing edit pipeline (edl.py / edl_v3.py / render3.py). It does not render anything.

**Flow:** Claude writes a plan (`research_plans/<name>.json`: segments with narration + keywords, jobs with real seed URLs / queries) ->
push the plan or run the `media-research` workflow -> parallel workers on GitHub-hosted `ubuntu-latest` runners (web, youtube, commons) ->
`consolidate.py` (dedupe, QC, relevance, manifest, report) -> text results on branch `research-results/run-<id>/`, media as artifact `research-package` ->
`ingest.py MANIFEST DEST` copies usable assets and writes `research_overrides.json` (segment -> ranked candidates with credit/licence) -> edit in `edl_v3.py` style.

**Job types:** `web` (Playwright: robots.txt check, screenshot, text/meta extraction, image candidates), `youtube` (yt-dlp metadata + caption cues -> real timestamps; downloads only Creative-Commons videos), `commons` (Wikimedia API; downloads only CC/PD files).
**Policy:** no auth/CAPTCHA/paywall/bot-check bypass; a bot check stops that worker; images are downloaded only when the licence is machine-identified as open or the host is on the official allowlist (flagged "usage not verified"); everything else is link + screenshot. Manifest fields are filled only when known. Nothing is marked verified: `needs_human_check`.
**Limits found in testing:** YouTube blocks runner IPs (bot check) after the first search; some publishers return 405; artifacts cannot be downloaded from Claude's sandbox (blob host blocked), so media comes back through the repo's Actions tab (download the `research-package` artifact) while manifest/report come back by git.
**Credits/cost:** public repos run free on standard runners; private repos use paid minutes (this is what failed on the other account). A full 5-job run took about 3 min wall time. Results are cached per plan+worker code hash, so unchanged plans don't re-run.
**Run it:** Actions tab -> media-research -> Run workflow (plan path), or push a plan under `research_plans/`.
**Troubleshooting:** open the failed matrix job log; check `report.md` "Inaccessible / failed"; re-push the plan with a changed `rev` to bypass the cache.
**Secrets:** none needed today. For a search API later, add `BRAVE_API_KEY` as a repository secret and read it from the environment in a new job type; never commit keys.
