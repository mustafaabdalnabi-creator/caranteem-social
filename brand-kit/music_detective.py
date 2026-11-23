import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(20)
sr=44100;B=0.6;T=44*B+2.0;n=int(sr*T);out=np.zeros(n)
def tt(d):return np.arange(int(sr*d))/sr
def lp(x,fc):b,a=butter(2,fc/(sr/2));return lfilter(b,a,x)
def hp(x,fc):b,a=butter(2,fc/(sr/2),'high');return lfilter(b,a,x)
def add(s,st,g=1):
    i=int(st*sr)
    if i<0 or i>=n:return
    e=min(n,i+len(s));out[i:e]+=s[:e-i]*g
def kick():
    t=tt(.35);f=50+90*np.exp(-t*30);return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*9)
def snap():
    t=tt(.18);return hp(rng.standard_normal(len(t)),1500)*np.exp(-t*28)*.6
def tick():
    t=tt(.04);return hp(rng.standard_normal(len(t)),6000)*np.exp(-t*120)*.35
def pluck(f,d=.5):
    t=tt(d);s=sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*(6+3*k))/k for k in range(1,6));return s*(1-np.exp(-t*400))
def bassn(f,d=.55):
    t=tt(d);s=np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*2*f*t);return lp(s,600)*np.exp(-t*4)
def stamp():
    t=tt(.5);thump=np.sin(2*np.pi*np.cumsum(70+60*np.exp(-t*40))/sr)*np.exp(-t*14)
    slap=hp(rng.standard_normal(len(t)),800)*np.exp(-t*45)
    return thump*1.1+slap*.7
def key():
    t=tt(.05);return hp(rng.standard_normal(len(t)),2500)*np.exp(-t*90)*.5
A=110.0;notes={'A':1,'C':2**(3/12),'D':2**(5/12),'E':2**(7/12),'F':2**(8/12),'G':2**(10/12),'D#':2**(6/12)}
bass=['A','A','F','E']
motif=[('A',0),('C',.5),('E',1),('D#',1.5),('E',2),(None,0),('A',3),('G',3.5)]
nb=44
for b in range(nb):
    t0=b*B;bar=b//4
    if b<6 or b>=38: pass
    if b%4 in (0,2): add(kick(),t0,.9 if b>=2 else .5)
    if b%4 in (1,3) and b>=2: add(snap(),t0,.7)
    for h in range(2): add(tick(),t0+h*B/2,.8 if h==0 else .5)
    if b%2==0 and b>=2: add(bassn(A*notes[bass[bar%4]]/2,B*1.9),t0,.55)
for bar in range(1,11):
    if bar in (7,):continue
    for nm,o in motif:
        if nm is None:continue
        add(pluck(2*A*notes[nm]*(2 if bar%2 else 1),.45),bar*4*B+o*B,.22)
# stamps
for sb in [4,11.5,19.5,27.5,32]: add(stamp(),(sb+0.35)*B,1.0)
# typewriter
def typing(b0,b1):
    t=b0*B
    while t<b1*B: add(key(),t,.5);t+=.06+rng.random()*.05
typing(0,2.6)
for q in (6,14,22): typing(q+1.6,q+3.8)
# end: final chord
for f in (A,A*notes['C'],A*notes['E']): add(pluck(2*f,1.8),38*B,.25)
out=out/np.abs(out).max()*.9
fade=np.ones(n);fl=int(1.2*sr);fade[-fl:]=np.linspace(1,0,fl);out*=fade
wavfile.write('music20.wav',sr,(out*32767).astype(np.int16))
print(T)
