#!/usr/bin/env python3
"""media_researcher CLI. Run from the cloned tools repo:  python3 media_researcher/mr.py <command> ...
  plan-check PLAN                          validate a plan (schema, URLs present, keywords)
  run PLAN --repo-dir DIR                  copy plan into the (write-attached) repo clone, push, print the workflow run id
  wait RUN_ID --repo-dir DIR               poll until the run finishes
  fetch RUN_ID --repo-dir DIR --out OUT    get manifest/report (+ open-licence media) from branch research-results into OUT/package
  inspect MANIFEST                         table of assets with status/eligibility
  approve MANIFEST IDS.. --by NAME --on DATE [--note T] [--commit-media] --out permissions.json   record a HUMAN approval (only when the user said so)
  fetch-approved PERMISSIONS --plan PLAN --manifest MANIFEST --repo-dir DIR   push approvals; runner downloads approved link-only images
  stage MANIFEST DEST [--editor-dir DIR]   verify files and stage usable assets (see stage.py)
"""
import sys, os, json, subprocess, time, re, shutil, glob
HERE = os.path.dirname(os.path.abspath(__file__))
def sh(cmd, cwd=None, check=True): 
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode: sys.exit(f'FAILED {" ".join(cmd)}\n{r.stderr[-500:]}')
    return r.stdout.strip()
def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default
def slug_of(repo_dir):
    u = sh(['git', 'remote', 'get-url', 'origin'], cwd=repo_dir); m = re.search(r'github\.com[/:]([^/]+/[^/.]+)', u); return m.group(1)

def plan_check(p):
    d = json.load(open(p)); errs = []
    if not d.get('segments'): errs.append('no segments')
    ids = {s['id'] for s in d.get('segments', [])}
    for s in d.get('segments', []):
        if not s.get('keywords'): errs.append(f"segment {s['id']}: no keywords")
    types = {'web', 'youtube', 'commons', 'openverse', 'archive', 'fetch_approved'}
    for j in d.get('jobs', []):
        if j.get('type') not in types: errs.append(f"job {j.get('id')}: bad type {j.get('type')}")
        if j['type'] == 'web' and not j.get('urls'): errs.append(f"job {j['id']}: web job needs real seed urls")
        if j['type'] in ('youtube', 'commons', 'openverse', 'archive') and not j.get('queries'): errs.append(f"job {j['id']}: needs queries")
        for s in j.get('segment_ids', []):
            if s not in ids: errs.append(f"job {j['id']}: unknown segment {s}")
    print('PLAN OK' if not errs else 'PLAN PROBLEMS:\n- ' + '\n- '.join(errs)); return not errs

def run():
    plan, rd = sys.argv[2], arg('--repo-dir'); assert plan_check(plan), 'fix the plan first'
    name = os.path.basename(plan); d = json.load(open(plan)); d['rev'] = int(time.time()); os.makedirs(f'{rd}/research_plans', exist_ok=True)
    json.dump(d, open(f'{rd}/research_plans/{name}', 'w'), indent=1)
    os.makedirs(f'{rd}/research_runs', exist_ok=True); json.dump(dict(plan=f'research_plans/{name}', nonce=int(time.time())), open(f'{rd}/research_runs/trigger.json', 'w'))
    sh(['git', 'add', '-A'], rd); sh(['git', '-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com', 'commit', '-qm', f'research plan {name}'], rd); sh(['git', 'push', 'origin', 'HEAD'], rd)
    sha = sh(['git', 'rev-parse', 'HEAD'], rd); slug = slug_of(rd)
    for _ in range(12):
        time.sleep(5); out = sh(['gh', 'api', f'repos/{slug}/actions/runs?head_sha={sha}', '-q', '.workflow_runs[]|select(.name=="media-research")|.id'], check=False)
        if out: print('RUN_ID', out.split()[0]); return
    sys.exit('workflow run not found (are Actions enabled and billing OK?)')

def wait():
    rid, rd = sys.argv[2], arg('--repo-dir'); slug = slug_of(rd)
    while True:
        st = sh(['gh', 'api', f'repos/{slug}/actions/runs/{rid}', '-q', '[.status,.conclusion]|@tsv'])
        if st.startswith('completed'): print(st); return
        time.sleep(15)

def fetch():
    rid, rd, out = sys.argv[2], arg('--repo-dir'), arg('--out'); pk = f'{out}/package'; os.makedirs(pk, exist_ok=True)
    sh(['git', 'fetch', '-q', '--depth=1', 'origin', 'research-results'], rd); tmp = f'{out}/_rr'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    names = sh(['git', 'ls-tree', '-r', '--name-only', 'FETCH_HEAD'], rd).splitlines(); mine = [n for n in names if n.startswith(f'run-{rid}/')]
    if not mine: sys.exit(f'no results for run {rid} on research-results (still running or failed)')
    for n in mine:
        dst = f'{tmp}/{n}'; os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(subprocess.run(['git', 'show', f'FETCH_HEAD:{n}'], cwd=rd, capture_output=True).stdout)
    for f in ('asset_manifest.json', 'report.md'): shutil.copy(f'{tmp}/run-{rid}/{f}', f'{pk}/{f}')
    man = json.load(open(f'{pk}/asset_manifest.json')); got = 0
    for a in man['assets']:
        if a.get('filename'):
            hit = glob.glob(f'{tmp}/run-{rid}/media/{os.path.basename(a["filename"])}')
            if hit: os.makedirs(os.path.dirname(f'{pk}/{a["filename"]}'), exist_ok=True); shutil.copy(hit[0], f'{pk}/{a["filename"]}'); got += 1
    need = sum(1 for a in man['assets'] if a.get('filename'))
    print(f'manifest+report fetched; media files with manifest entries: {need}; retrieved via git (open-licence only): {got}')
    if need > got: print(f'NOTE: {need-got} collected file(s) exist only in the workflow artifact "research-package" (run {rid}). Claude\'s sandbox cannot download artifacts: ask the user to download it from the repo Actions tab and attach/unzip it, or approve commit_approved_media.')

def inspect(p):
    m = json.load(open(p))
    for a in m['assets']:
        print(f"{a['asset_id']:6} {a['asset_type']:10} {('ELIGIBLE' if a.get('editor_eligible') else '-'):9} {a['download_status'][:22]:22} rel={a.get('relevance_score')} {(a.get('title') or a.get('original_url') or '')[:60]}")

def approve():
    man = json.load(open(sys.argv[2])); ids = [x for x in sys.argv[3:] if re.match(r'^A\d+s?$', x)]; by, on = arg('--by'), arg('--on'); out = arg('--out', 'permissions.json')
    assert by and on, '--by and --on required: approvals are a human decision'
    perm = json.load(open(out)) if os.path.exists(out) else {'approvals': [], 'commit_approved_media': False}
    for a in man['assets']:
        if a['asset_id'] in ids: perm['approvals'].append(dict(asset_id=a['asset_id'], url=a.get('original_url'), page_url=a.get('page_url'), source_name=a.get('source_name'), source_author=a.get('source_author'), segment_ids=a.get('narration_segment'), relevance=a.get('relevance_score'), keyword_hits=None, approved_by=by, approved_on=on, note=arg('--note', '')))
    if '--commit-media' in sys.argv: perm['commit_approved_media'] = True
    json.dump(perm, open(out, 'w'), indent=1); print('recorded', len(perm['approvals']), 'approvals ->', out)

def fetch_approved():
    perm_p, plan_p, rd = sys.argv[2], arg('--plan'), arg('--repo-dir'); perm = json.load(open(perm_p)); plan = json.load(open(plan_p))
    plan['jobs'] = [j for j in plan['jobs'] if j['type'] != 'fetch_approved'] + [dict(id='approved', type='fetch_approved', approvals=perm['approvals'])]
    name = os.path.basename(plan_p).replace('.json', '') + '-approved.json'; os.makedirs(f'{rd}/research_plans', exist_ok=True)
    plan['jobs'] = [j for j in plan['jobs'] if j['id'] == 'approved']; plan['rev'] = int(time.time()); json.dump(plan, open(f'{rd}/research_plans/{name}', 'w'), indent=1)
    shutil.copy(perm_p, f'{rd}/research_plans/{name.replace(".json", ".permissions.json")}')
    sys.argv = ['mr', 'run', f'{rd}/research_plans/{name}', '--repo-dir', rd]; run()

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'plan-check': sys.exit(0 if plan_check(sys.argv[2]) else 1)
    elif c == 'run': run()
    elif c == 'wait': wait()
    elif c == 'fetch': fetch()
    elif c == 'inspect': inspect(sys.argv[2])
    elif c == 'approve': approve()
    elif c == 'fetch-approved': fetch_approved()
    elif c == 'stage': os.execv(sys.executable, [sys.executable, f'{HERE}/stage.py'] + sys.argv[2:])
    else: print(__doc__)
