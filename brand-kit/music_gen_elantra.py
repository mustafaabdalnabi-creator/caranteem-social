import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(1124)
sr=44100;T=26.0;n=int(sr*T);out=np.zeros((n,2))
def tt(d):return np.arange(int(sr*d))/sr
def lp(x,fc):b,a=butter(2,fc/(sr/2));return lfilter(b,a,x)
def hp(x,fc):b,a=butter(2,fc/(sr/2),'high');return lfilter(b,a,x)
def add(s,st,g=1,pan=0):
    i=int(st*sr)
    if i<0 or i>=n:return
    e=min(n,i+len(s));s=s[:e-i]*g;out[i:e,0]+=s*(1-max(pan,0));out[i:e,1]+=s*(1+min(pan,0))
def sub(f,d):t=tt(d);return np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.exp(-t*3.5)
def tick():t=tt(.03);return hp(rng.standard_normal(len(t)),5000)*np.exp(-t*150)*.3
def blip(f):t=tt(.08);return np.sign(np.sin(2*np.pi*f*t))*np.exp(-t*40)*.1
def kick():t=tt(.25);return np.sin(2*np.pi*np.cumsum(42+70*np.exp(-t*35))/sr)*np.exp(-t*12)*.8
def impact(g=1):
    t=tt(2.2);boom=np.sin(2*np.pi*np.cumsum(30+70*np.exp(-t*5))/sr)*np.exp(-t*1.8)
    return (boom+hp(rng.standard_normal(len(t)),150)*np.exp(-t*7)*.35)*g
def whoosh(d=.6):t=tt(d);return lp(hp(rng.standard_normal(len(t)),400),3000)*np.sin(np.pi*t/d)**2*.22
def drone(f,d):t=tt(d);s=sum(np.sin(2*np.pi*f*k*t+k)/k for k in (1,2,3));return lp(s,500)*np.minimum(1,t/1.0)*np.minimum(1,(d-t)/0.8)*.25
B=60/100;D=43.65
cuts=[0,1.4,2.7,4.3,5.6,7.8,10.0,12.2,14.4,16.6,19.6,21.6]
# hook: sparse pulse, building
t=0.0
while t<5.6:
    add(sub(D*2,.3),t,.55);add(tick(),t+B/2,1,.4);t+=B
r=tt(1.3);add(hp(rng.standard_normal(len(r)),2500)*(r/1.3)**2*.15,4.3,1)
for c in cuts[1:4]:add(impact(.6),c,1)
# generations: steady groove, impact on every cut, blip arpeggio
add(impact(1.2),5.6,1);add(drone(D,11.0),5.6,1)
notes=[D*4,D*4*1.2,D*4*1.5,D*4*1.8]
t=5.6;k=0
while t<16.6:
    add(kick(),t,.75);add(sub(D*2,.35),t,.6)
    for q in range(4):add(tick(),t+q*B/4,1,(-.4 if q%2 else .4))
    add(blip(notes[k%4]),t+B/2,1.4,(.3 if k%2 else -.3));k+=1;t+=B
for c in cuts[5:10]:add(whoosh(.45),c-.35,1);add(impact(.8),c,1)
# parts: pops on each product
for j in range(4):add(blip(notes[j]*2),16.6+.45+j*.28,2.2)
t=16.6
while t<19.6:add(kick(),t,.7);add(tick(),t+B/2,1,.3);t+=B
add(impact(1.0),19.6,1);add(drone(D*1.5,2.0),19.6,1)
for x in (19.6,20.0,20.4):add(tick(),x,1.6)
add(impact(1.3),21.6,1);add(drone(D,4.4),21.6,1.4)
for f in (D*4,D*5,D*6):
    t=tt(4.2);add(np.sin(2*np.pi*f*t)*np.exp(-t*.8)*.12,21.6,1)
out=out/np.abs(out).max()*.9;fl=int(.9*sr);out[-fl:]*=np.linspace(1,0,fl)[:,None]
wavfile.write('music_gen.wav',sr,(out*32767).astype(np.int16));print('ok')
