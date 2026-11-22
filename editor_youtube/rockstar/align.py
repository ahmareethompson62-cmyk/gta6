import re,json,difflib
asr=json.load(open('audio/asr.json'))
A=[(re.sub(r'\(\d\)','',w).lower(),s,e) for w,s,e in asr if w not in('<s>','</s>','<sil>') and not w.startswith('[')]
txt=open('narration.txt').read()
# sentences with paragraph index
sents=[]
for pi,p in enumerate([p for p in txt.split('\n') if p.strip()]):
    for s in re.findall(r'[^.!?]+[.!?]+["”]?|[^.!?]+$',p):
        s=s.strip()
        if s: sents.append((pi,s))
toks=[];owner=[]
for i,(pi,s) in enumerate(sents):
    for w in re.findall(r"[a-z0-9']+",s.lower()):
        toks.append(w);owner.append(i)
# phonetic-ish normalisation for matching
def n(w): return re.sub(r"[^a-z]","",w)[:4]
sm=difflib.SequenceMatcher(None,[n(t) for t in toks],[n(a[0]) for a in A],autojunk=False)
T=[None]*len(toks)
for b in sm.get_matching_blocks():
    for k in range(b.size): T[b.a+k]=(A[b.b+k][1],A[b.b+k][2])
m=sum(t is not None for t in T);print('matched',m,'of',len(toks))
# interpolate
idx=[i for i,t in enumerate(T) if t]
for a,b in zip(idx,idx[1:]):
    t0=T[a][1];t1=T[b][0]
    for k in range(a+1,b): T[k]=(t0+(t1-t0)*(k-a-1)/(b-a-1 if b-a>1 else 1),t0+(t1-t0)*(k-a)/(b-a))
for k in range(0,idx[0]): T[k]=(0,0.1)
for k in range(idx[-1]+1,len(T)): T[k]=(T[idx[-1]][1],293.2)
out=[]
for i,(pi,s) in enumerate(sents):
    ks=[k for k,o in enumerate(owner) if o==i]
    out.append(dict(i=i,para=pi,start=round(T[ks[0]][0],2),end=round(T[ks[-1]][1],2),text=s,matched=sum(1 for k in ks if k in idx)/len(ks)))
for k,o in enumerate(out[:-1]): o['end']=max(o['end'],o['start']+0.3)
json.dump(out,open('sents.json','w'),indent=1)
for o in out: print(o['i'],o['start'],o['end'],f"{o['matched']:.0%}",o['text'][:70])
