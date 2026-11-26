import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(1127)
sr=44100;T=24.0;n=int(sr*T);out=np.zeros((n,2));BPM=104;B=60/BPM;E=41.2  # key E
def tt(d):return np.arange(int(sr*d))/sr
def lp(x,fc):b,a=butter(2,fc/(sr/2));return lfilter(b,a,x)
def hp(x,fc):b,a=butter(2,fc/(sr/2),'high');return lfilter(b,a,x)
def add(s,st,g=1,pan=0):
    i=int(st*sr)
    if i<0 or i>=n:return
    e=min(n,i+len(s));s=s[:e-i]*g;out[i:e,0]+=s*(1-max(pan,0));out[i:e,1]+=s*(1+min(pan,0))
def kick():t=tt(.28);return np.sin(2*np.pi*np.cumsum(45+95*np.exp(-t*32))/sr)*np.exp(-t*11)*.85
def snare():t=tt(.22);return (hp(rng.standard_normal(len(t)),1500)*np.exp(-t*18)*.4+np.sin(2*np.pi*190*t)*np.exp(-t*30)*.3)
def hat():t=tt(.04);return hp(rng.standard_normal(len(t)),7500)*np.exp(-t*90)*.22
def sub(f,d):t=tt(d);return np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.exp(-t*3)
def impact(g=1):
    t=tt(2.0);boom=np.sin(2*np.pi*np.cumsum(32+80*np.exp(-t*5))/sr)*np.exp(-t*2)
    return (boom+hp(rng.standard_normal(len(t)),180)*np.exp(-t*8)*.35)*g
def riser(d):t=tt(d);return hp(rng.standard_normal(len(t)),1200)*(t/d)**2*.18
def stab(f,d=.5):t=tt(d);s=sum(np.sign(np.sin(2*np.pi*f*r*t))*.3/r for r in (1,1.498,2));return lp(s,2500)*np.exp(-t*6)*.35
def pad(f,d):t=tt(d);s=sum(np.sin(2*np.pi*f*k*t+k)/k for k in (1,2,3,4));return lp(s,700)*np.minimum(1,t/.6)*np.minimum(1,(d-t)/.6)*.18
CUTS=[0,1.7,3.4,6.0,9.2,10.3,13.1,15.9,18.4,20.6]
# intro hit
add(impact(1.2),0);add(stab(E*8),0,1)
# groove 1.7-9.2 (half-time feel then full)
t=1.7
while t<9.15:
    add(kick(),t,.9);add(sub(E*2,B*.9),t,.6)
    if t>3.3:add(snare(),t+B,.9) if False else None
    for k in range(4):add(hat(),t+k*B/4,1,(.4 if k%2 else -.4))
    if t>3.3:add(kick(),t+B*1.5,.6)
    t+=B*2 if t<3.4 else B
    if t>3.4 and int((t-3.4)/B)%2==1:add(snare(),t,.8)
add(pad(E*2,7.5),1.7,1)
# gift reveal riser and hit
add(riser(1.0),5.0,1);add(impact(1.0),6.0);add(stab(E*6),6.0,1.2)
# "وكمان" pause: drop drums, riser into 20%
add(riser(1.1),9.2,1.2)
# 20% sections: driving 4-on-floor
t=10.3
while t<15.85:
    add(kick(),t,1);add(sub(E*2*(1.335 if t>13.1 else 1),B*.9),t,.6)
    add(hat(),t+B/2,1.3,.3)
    if int((t-10.3)/B)%2==1:add(snare(),t,.9)
    t+=B
for c in (10.3,13.1):add(impact(.9),c);add(stab(E*8 if c<13 else E*8*1.335),c,1.3)
# dates: stop + big hit
add(riser(.8),15.1,1);add(impact(1.2),15.9);add(pad(E*1.5,2.5),15.9,1)
# trust line: light groove
t=18.4
while t<20.55:
    add(kick(),t,.7);add(hat(),t+B/2,1);t+=B
add(stab(E*6),18.4,.9)
# end card
add(impact(1.3),20.6);add(pad(E*2,3.4),20.6,1.3)
for f in (E*8,E*12,E*16*1.189):
    t2=tt(3.2);add(np.sin(2*np.pi*f*t2)*np.exp(-t2*.9)*.1,20.6,1)
out=out/np.abs(out).max()*.9;fl=int(.8*sr);out[-fl:]*=np.linspace(1,0,fl)[:,None]
wavfile.write('music_bf.wav',sr,(out*32767).astype(np.int16));print('ok')
