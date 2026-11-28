import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter,butter
rng=np.random.default_rng(1130)
sr=44100;BPM=112;B=60/BPM;T=25.9;n=int(sr*T);out=np.zeros((n,2))
cuts=[0,4,10,13,16,19,22,25,28,35,40]
def tt(d):return np.arange(int(sr*d))/sr
def lp(x,fc):b,a=butter(2,fc/(sr/2));return lfilter(b,a,x)
def hp(x,fc):b,a=butter(2,fc/(sr/2),'high');return lfilter(b,a,x)
def add(s,st,g=1,pan=0):
    i=int(st*sr)
    if i<0 or i>=n:return
    e=min(n,i+len(s));s=s[:e-i]*g;out[i:e,0]+=s*(1-max(pan,0));out[i:e,1]+=s*(1+min(pan,0))
def kick():t=tt(.28);return np.sin(2*np.pi*np.cumsum(45+120*np.exp(-t*40))/sr)*np.exp(-t*11)
def clap():
    t=tt(.22);x=hp(rng.standard_normal(len(t)),1400);env=np.exp(-t*22)
    for d in (.008,.016):env[int(d*sr):]+=np.exp(-(t[int(d*sr):]-d)*70)*.7
    return x*env*.45
def ohat():t=tt(.16);return hp(rng.standard_normal(len(t)),8000)*np.exp(-t*18)*.22
def sq(f,d):t=tt(d);return np.sign(np.sin(2*np.pi*f*t))*.5+np.sin(2*np.pi*f*2.005*t)*.3
def stab(fs,d=.32):
    t=tt(d);s=sum(sq(f,d)+sq(f*1.007,d) for f in fs)/len(fs);return lp(s,3200)*np.exp(-t*9)*.35
def sub(f,d):t=tt(d);return np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.exp(-t*5)*.7
def impact():
    t=tt(1.2);boom=np.sin(2*np.pi*np.cumsum(35+80*np.exp(-t*6))/sr)*np.exp(-t*3)
    return boom+hp(rng.standard_normal(len(t)),300)*np.exp(-t*8)*.4
def riser(d):t=tt(d);x=hp(rng.standard_normal(len(t)),800);return x*(t/d)**2*.35
R_=lambda s:2**(s/12);root=55*R_(-3) # F#
prog=[[0,4,7],[-3,0,4],[5,9,12],[7,11,14]] # F# D#m B C# (bright)
nb=int(T/B)
for b in range(nb-2):
    t0=b*B;ch=prog[(b//4)%4]
    if b>=1:add(kick(),t0,1)
    add(ohat(),t0+B/2,1,.25)
    if b%2==1:add(clap(),t0,.8)
    add(sub(root*R_(ch[0]),B*.9),t0+B/2,.8)
for c in cuts:
    ch=prog[(c//4)%4];add(stab([root*4*R_(x) for x in ch]),c*B,1,(-.3 if c%2 else .3))
add(riser(4*B),6*B,1);add(impact(),10*B,.8);add(riser(3*B),25*B,.8);add(impact(),28*B,1);add(impact(),35*B,.6);add(impact(),40*B,.9)
def cash():t=tt(.25);return (np.sin(2*np.pi*2093*t)+np.sin(2*np.pi*2637*t)*.7)*np.exp(-t*14)*.25
for c in [10,13,16,19,22,25]:add(cash(),c*B+.35*1,1,(.3 if c%2 else -.3))
out=out/np.abs(out).max()*.9;fl=int(1.0*sr);out[-fl:]*=np.linspace(1,0,fl)[:,None]
wavfile.write('/tmp/claude-0/prev/music2.wav',sr,(out*32767).astype(np.int16));print('ok')
