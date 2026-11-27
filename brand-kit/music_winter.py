import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(1128)
sr=44100;BPM=116;B=60/BPM;T=28.0;n=int(sr*T);out=np.zeros((n,2))
def tt(d):return np.arange(int(sr*d))/sr
def lp(x,fc):b,a=butter(2,fc/(sr/2));return lfilter(b,a,x)
def hp(x,fc):b,a=butter(2,fc/(sr/2),'high');return lfilter(b,a,x)
def add(s,st,g=1,pan=0):
    i=int(st*sr)
    if i<0 or i>=n:return
    e=min(n,i+len(s));s=s[:e-i]*g;out[i:e,0]+=s*(1-max(pan,0));out[i:e,1]+=s*(1+min(pan,0))
def kick():t=tt(.3);return np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*35))/sr)*np.exp(-t*10)
def clap():
    t=tt(.25);x=hp(rng.standard_normal(len(t)),1200);env=np.exp(-t*20)
    for d in (0.01,0.02):env[int(d*sr):]+=np.exp(-(t[int(d*sr):]-d)*60)*.6
    return x*env*.5
def hat(open_=False):t=tt(.18 if open_ else .05);return hp(rng.standard_normal(len(t)),7000)*np.exp(-t*(15 if open_ else 80))*.25
def saw(f,d):
    t=tt(d);s=sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,8));return s
def chord(fs,d):
    s=sum(saw(f,d)+saw(f*1.004,d) for f in fs)/len(fs);t=tt(d);env=np.minimum(1,t/.02)*np.exp(-t*2.2);return lp(s*env,2500)*.25
def bass(f,d):t=tt(d);s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)*np.exp(-t*8);return s*np.exp(-t*3)*.6
def pluck(f,d=.3):t=tt(d);return sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*(10+4*k))/k for k in range(1,5))
R=lambda s:2**(s/12)
root=110*R(7) # E
prog=[[0,4,7],[-3,0,4],[-7,-3,0],[-5,-1,2]] # E C#m A B (major, bright)
nb=int(T/B)
for b in range(nb):
    t0=b*B;bar=b//4;ch=prog[bar%4]
    if b>=2:add(kick(),t0,.9)
    if b%2==1 and b>=4:add(clap(),t0,.8)
    for h in range(2):add(hat(h==1),t0+h*B/2,.9,(-.3 if h else .3))
    if b%4==0:add(chord([root*2*R(x) for x in ch],B*3.8),t0,.9)
    if b>=4:
        for h in range(2):add(bass(root/2*R(ch[0]),B/2*.9),t0+h*B/2,.7)
mel=[0,4,7,11,12,7,4,2]
for b in range(8,nb-4):
    ch=prog[(b//4)%4]
    for h in range(2):add(pluck(root*4*R(ch[0]+mel[(2*b+h)%8]-ch[0]+0)),b*B+h*B/2,.12,(.4 if h else -.4))
B=60/BPM
ST=[0,4,7,13,19,25,30,33,38,43,46]
CUTS=[x*B for x in ST[1:]]
def bell(f,d=1.2):t=tt(d);return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*4))*np.exp(-t*3)*.3
for k,f in enumerate([4,7,11,16]):add(bell(root*4*R(f)),k*B/2,.5,(.3 if k%2 else -.3))
def hit():t=tt(.6);return (np.sin(2*np.pi*np.cumsum(40+90*np.exp(-t*25))/sr)*np.exp(-t*6)+hp(rng.standard_normal(len(t)),2000)*np.exp(-t*18)*.3)*.7
for tc in CUTS:add(hit(),tc,.8)
for tc in CUTS:
    t=tt(.4);w=hp(rng.standard_normal(len(t)),500)*np.sin(np.pi*t/.4)**2*.25;add(w,tc-.25,1)
def tk():t=tt(.12);return (np.sin(2*np.pi*1800*t)+.5*np.sin(2*np.pi*2700*t))*np.exp(-t*40)*.35
TICKS=[(ST[i]+4)*B for i in (2,3,4)]+[ST[5]*B+.25+k*B for k in range(3)]
for tc in TICKS:add(tk(),tc,1);add(bell(root*8),tc,.4)
out=out/np.abs(out).max()*.9
fl=int(1.2*sr);out[-fl:]*=np.linspace(1,0,fl)[:,None]
wavfile.write('music_winter.wav',sr,(out*32767).astype(np.int16));print('ok')
