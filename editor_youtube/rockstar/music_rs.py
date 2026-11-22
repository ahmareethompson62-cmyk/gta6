"""Original synthesized ambient bed + accents (no third-party music) for the Rockstar video. Output work/music.wav"""
import numpy as np, wave
sr=44100; D=293.5; n=int(sr*D); t=np.arange(n)/sr; rng=np.random.default_rng(11)
chords=[[57,60,64],[53,57,60],[55,59,62],[52,55,59]]
f=lambda m:440*2**((m-69)/12)
L=np.zeros(n); R=np.zeros(n); per=12.0
for k in range(int(D/per)+1):
    ch=chords[k%4]; a=int(k*per*sr); b=min(n,int((k+1)*per*sr+3*sr))
    if a>=n: break
    tt=t[a:b]-k*per; env=np.clip(tt/4,0,1)*np.clip((per+3-tt)/4,0,1)
    for j,m in enumerate(ch):
        for det,pan in [(-0.4,0.3),(0.4,0.7)]:
            fr=f(m-12)*2**(det/1200*5)
            sig=(np.sin(2*np.pi*fr*tt)+.35*np.sin(2*np.pi*2*fr*tt+j))*env*0.05
            L[a:b]+=sig*(1-pan); R[a:b]+=sig*pan
    sub=np.sin(2*np.pi*f(ch[0]-24)*tt)*env*0.09; L[a:b]+=sub; R[a:b]+=sub
lfo=.85+.15*np.sin(2*np.pi*t/7.5); L*=lfo; R*=lfo
def hit(at,amp=1.0,low=48):
    a=int(at*sr); m=int(2.2*sr); tt=np.arange(m)/sr
    h=np.sin(2*np.pi*(f(low)*(1+1.5*np.exp(-tt*9)))*tt)*np.exp(-tt*2.4)*amp*.45
    nz=rng.standard_normal(m)*np.exp(-tt*18)*amp*.05
    sg=h+nz; e=min(n-a,m); L[a:a+e]+=sg[:e]; R[a:a+e]+=sg[:e]
for at,amp in [(0.3,1.0),(16.45,.9),(94.87,1.0),(114.19,1.1),(143.04,.8),(183.67,.8),(204.32,.9),(224.77,1.0),(267.73,.9),(288.32,1.0)]: hit(at,amp)
fade=np.clip((D-t)/4,0,1); L*=fade; R*=fade
pk=max(abs(L).max(),abs(R).max()); L/=pk; R/=pk; L*=.8; R*=.8
x=(np.stack([L,R],1)*32767).astype('<i2')
w=wave.open('/home/claude/rockstar_video/work/music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes()); w.close()
