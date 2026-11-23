import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(25)
sr=44100;T=25.0;n=int(sr*T);out=np.zeros((n,2))
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
B=60/96;D=36.7
# NOISE 0-6.05: pulse accelerating + glitch blips layered
t=0.0
while t<6.05:
    add(sub(D*2,.3),t,.7);add(kick(),t,.6)
    for k in range(4):add(tick(),t+k*B/4,1,(-.5 if k%2 else .5))
    t+=B
for k in range(140):
    st=rng.random()*6.0;add(blip(400+rng.random()*1800),st,.6+st/10,rng.random()*2-1)
r=tt(6.05);add(hp(rng.standard_normal(len(r)),2000)*(r/6.05)**2*.12,0,1)
# silence 6.05-6.75, impact on statement
add(impact(1.1),6.8,1)
add(drone(D,6.6),6.9,1)
# product section beat
for b in range(int((13.5-9.0)/B)):
    t0=9.0+b*B;add(sub(D*2,.45),t0,.8);add(tick(),t0+B/2,1,.3)
for w in (8.8,10.3,11.8):add(whoosh(),w,1)
# pause 13.5-13.95 then impact
add(impact(1.2),13.95,1);add(drone(D*1.5,8.0),14.0,1)
add(impact(.7),16.6,1)
for t0 in (18.2,19.9):add(whoosh(.4),t0-.2,1);add(tick(),t0,1.5)
add(impact(.9),20.25,1)
add(impact(1.2),21.6,1);add(drone(D,3.4),21.6,1.4)
for f in (D*4,D*6,D*8*1.189):
    t=tt(3.3);add(np.sin(2*np.pi*f*t)*np.exp(-t*.9)*.12,21.6,1)
out=out/np.abs(out).max()*.9;fl=int(.8*sr);out[-fl:]*=np.linspace(1,0,fl)[:,None]
wavfile.write('music25.wav',sr,(out*32767).astype(np.int16));print('ok')
