#!/usr/bin/env python3
"""Scaffold a research plan from an existing narration (sents.json from the existing timing step) or a topic.
Usage: plan_tools.py scaffold SENTS.json CHAPTERS.json OUT_PLAN.json
This does only mechanical work: group sentences per chapter, pull candidate search terms (capitalised names, numbers, outlets).
Claude then edits the plan: sets real seed URLs (from web search), queries, per-segment keywords. The plan is the contract with the workers."""
import sys, json, re
if sys.argv[1] == 'scaffold':
    sents = json.load(open(sys.argv[2])); chapters = json.load(open(sys.argv[3])); plan = dict(project='untitled', topic='', segments=[], jobs=[])
    for ch in chapters:
        txt = ' '.join(s['text'] for s in sents if ch['start'] <= s['start'] < ch['end'])
        caps = re.findall(r'\b(?:[A-Z][a-zA-Z0-9]+(?:\s[A-Z][a-zA-Z0-9]+)*)\b', txt); nums = re.findall(r'\b\d[\d,.]*\b', txt)
        plan['segments'].append(dict(id=ch['id'], chapter=ch['name'], start=ch['start'], end=ch['end'], narration=txt[:600], keywords=sorted(set(caps))[:12] + nums[:4]))
    json.dump(plan, open(sys.argv[4], 'w'), indent=1); print('scaffolded', len(plan['segments']), 'segments')
