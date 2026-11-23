// Ordinary guy, flat-illustration, natural proportions. Local coords: x=0 centre, y=0 top of head, feet ~1150.
const C2={skin:'#D19A78',sk2:'#B47D5C',hair:'#2B211C',sw:'#5E6B78',sw2:'#4E5A66',swd:'#43505B',jean:'#6F8FB5',jean2:'#5B7BA1',shoe:'#F2F2F2',sole:'#D9D9D9',ink:'#1A1416'};
function poly(pts,fill){return `<path d="M${pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L')}Z" fill="${fill}" stroke-linejoin="round"/>`}
function limb(x1,y1,x2,y2,w1,w2,fill){const a=Math.atan2(y2-y1,x2-x1),nx=-Math.sin(a),ny=Math.cos(a);
 return poly([[x1+nx*w1/2,y1+ny*w1/2],[x2+nx*w2/2,y2+ny*w2/2],[x2-nx*w2/2,y2-ny*w2/2],[x1-nx*w1/2,y1-ny*w1/2]],fill)+`<circle cx="${x2}" cy="${y2}" r="${w2/2}" fill="${fill}"/><circle cx="${x1}" cy="${y1}" r="${w1/2}" fill="${fill}"/>`}
function arm2(side,a1,a2,point){
 const sx=side*92,sy=218,L1=180,L2=165,r1=a1*Math.PI/180,r2=a2*Math.PI/180;
 const ex=sx+side*Math.sin(r1)*L1,ey=sy+Math.cos(r1)*L1,hx=ex+side*Math.sin(r2)*L2,hy=ey+Math.cos(r2)*L2;
 const shade=side<0?C2.sw2:C2.sw;
 let s=limb(sx,sy,ex,ey,58,46,shade)+limb(ex,ey,hx,hy,46,38,shade);
 const a=Math.atan2(hy-ey,hx-ex),cx=hx+Math.cos(a)*4,cy=hy+Math.sin(a)*4;
 s+=limb(hx-Math.cos(a)*14,hy-Math.sin(a)*14,cx,cy,40,40,C2.swd); // cuff
 // hand
 const px=cx+Math.cos(a)*22,py=cy+Math.sin(a)*22;
 s+=`<g transform="translate(${px} ${py}) rotate(${a*180/Math.PI})">`;
 if(point){s+=`<rect x="-14" y="-15" width="34" height="30" rx="13" fill="${C2.skin}"/><rect x="12" y="-14" width="40" height="11" rx="5.5" fill="${C2.skin}"/><ellipse cx="0" cy="${side>0?12:-12}" rx="12" ry="7" fill="${C2.sk2}" opacity=".5"/>`}
 else{s+=`<rect x="-14" y="-15" width="38" height="30" rx="14" fill="${C2.skin}"/><path d="M14 -6 h10 M14 2 h12 M14 10 h10" stroke="${C2.sk2}" stroke-width="2.5" stroke-linecap="round"/>`}
 return s+`</g>`;
}
function man(o={}){
 const aL=o.aL||[6,4],aR=o.aR||[6,4];let s='';
 // legs (slim jeans)
 s+=`<path d="M-88 560 Q-96 820 -92 1080 L-26 1080 Q-20 850 -4 680 L4 680 Q20 850 26 1080 L92 1080 Q96 820 88 560Z" fill="${C2.jean}"/>`;
 s+=`<path d="M-4 680 Q-16 880 -22 1078 M60 610 Q64 860 66 1078" stroke="${C2.jean2}" stroke-width="4" fill="none"/>`;
 s+=`<rect x="-94" y="1062" width="72" height="20" rx="6" fill="${C2.jean2}"/><rect x="22" y="1062" width="72" height="20" rx="6" fill="${C2.jean2}"/>`;
 // sneakers
 s+=`<path d="M-24 1080 L-24 1104 Q-24 1124 -44 1126 L-130 1126 Q-146 1124 -140 1108 Q-128 1084 -96 1080Z" fill="${C2.shoe}"/><rect x="-142" y="1120" width="120" height="10" rx="5" fill="${C2.sole}"/>`;
 s+=`<path d="M24 1080 L24 1104 Q24 1124 44 1126 L130 1126 Q146 1124 140 1108 Q128 1084 96 1080Z" fill="${C2.shoe}"/><rect x="22" y="1120" width="120" height="10" rx="5" fill="${C2.sole}"/>`;
 s+=arm2(-1,aL[0],aL[1],false);
 // neck
 s+=`<path d="M-24 140 h48 v62 h-48Z" fill="${C2.sk2}"/>`;
 // sweater torso
 s+=`<path d="M-96 222 Q-98 196 -58 186 L-30 178 Q0 200 30 178 L58 186 Q98 196 96 222 L92 548 Q0 566 -92 548Z" fill="${C2.sw}"/>`;
 s+=`<path d="M-92 530 Q0 548 92 530 L92 572 Q0 590 -92 572Z" fill="${C2.swd}"/>`;
 s+=`<path d="M-32 180 Q0 214 32 180" stroke="${C2.swd}" stroke-width="12" fill="none" stroke-linecap="round"/>`;
 s+=`<path d="M-48 300 Q-40 420 -52 520 M50 300 Q44 420 54 520" stroke="${C2.sw2}" stroke-width="3" fill="none" opacity=".6"/>`;
 s+=arm2(1,aR[0],aR[1],o.point);
 // head
 s+=`<g transform="rotate(${o.tilt||0} 0 150)">`;
 s+=`<ellipse cx="-58" cy="86" rx="11" ry="17" fill="${C2.sk2}"/><ellipse cx="58" cy="86" rx="11" ry="17" fill="${C2.sk2}"/>`;
 s+=`<path d="M-56 40 Q-58 128 -22 150 Q0 160 22 150 Q58 128 56 40 Q54 -4 0 -6 Q-54 -4 -56 40Z" fill="${C2.skin}"/>`;
 // light stubble
 s+=`<path d="M-54 86 Q-50 140 -20 152 Q0 160 20 152 Q50 140 54 86 Q48 118 26 124 Q0 116 -26 124 Q-48 118 -54 86Z" fill="${C2.hair}" opacity=".18"/>`;
 // hair: short, neat side part
 s+=`<path d="M-60 58 Q-66 4 -30 -14 Q4 -30 40 -18 Q66 -6 62 42 Q60 54 58 60 Q54 30 40 20 Q30 8 4 10 L-12 4 Q-30 14 -44 24 Q-56 36 -60 58Z" fill="${C2.hair}"/>`;
 s+=`<path d="M-12 4 Q-2 -10 30 -12" stroke="#4a3a32" stroke-width="3" fill="none"/>`;
 const by=o.happy?46:50;
 s+=`<path d="M-40 ${by} Q-28 ${by-6} -16 ${by-1}" stroke="${C2.hair}" stroke-width="5" stroke-linecap="round" fill="none"/><path d="M40 ${by} Q28 ${by-6} 16 ${by-1}" stroke="${C2.hair}" stroke-width="5" stroke-linecap="round" fill="none"/>`;
 const lx=(o.look||0)*2.5;
 if(o.blink){s+=`<path d="M-36 70 h14 M22 70 h14" stroke="${C2.ink}" stroke-width="4" stroke-linecap="round"/>`}
 else if(o.happy){s+=`<path d="M-37 72 Q-29 63 -21 72 M21 72 Q29 63 37 72" stroke="${C2.ink}" stroke-width="4.5" fill="none" stroke-linecap="round"/>`}
 else{s+=`<ellipse cx="${-29+lx}" cy="70" rx="6" ry="6.5" fill="${C2.ink}"/><ellipse cx="${29+lx}" cy="70" rx="6" ry="6.5" fill="${C2.ink}"/><circle cx="${-27+lx}" cy="68" r="1.8" fill="#fff"/><circle cx="${31+lx}" cy="68" r="1.8" fill="#fff"/>`}
 s+=`<path d="M2 76 Q10 98 -4 102" stroke="${C2.sk2}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
 if(o.m===2)s+=`<path d="M-20 120 Q0 118 20 120 Q16 142 0 143 Q-16 142 -20 120Z" fill="#6b2020"/><path d="M-16 121 h32 l-3 6 h-26Z" fill="#fff"/>`;
 else if(o.m===1)s+=`<ellipse cx="0" cy="126" rx="10" ry="7" fill="#6b2020"/>`;
 else s+=`<path d="M-15 122 Q0 132 15 122" stroke="#8a3d30" stroke-width="4.5" fill="none" stroke-linecap="round"/>`;
 return s+`</g>`;
}
