import json, math
RAL = json.load(open('ral.json'))
DE = {'Green beige':'Grünbeige'}
def hex2rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def lin(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h): r,g,b=[lin(x) for x in hex2rgb(h)]; return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
def lab(h):
    r,g,b=[lin(x) for x in hex2rgb(h)]
    x=(0.4124*r+0.3576*g+0.1805*b)/0.95047; y=(0.2126*r+0.7152*g+0.0722*b); z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return (116*f(y)-16, 500*(f(x)-f(y)), 200*(f(y)-f(z)))
def de2000(l1,l2):
    L1,a1,b1=l1;L2,a2,b2=l2
    C1=math.hypot(a1,b1);C2=math.hypot(a2,b2);Cb=(C1+C2)/2
    G=0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7)))
    a1p,a2p=(1+G)*a1,(1+G)*a2
    C1p,C2p=math.hypot(a1p,b1),math.hypot(a2p,b2)
    h1p=math.degrees(math.atan2(b1,a1p))%360;h2p=math.degrees(math.atan2(b2,a2p))%360
    dLp=L2-L1;dCp=C2p-C1p
    dh=h2p-h1p
    if C1p*C2p==0: dh=0
    elif dh>180: dh-=360
    elif dh<-180: dh+=360
    dHp=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dh/2))
    Lbp=(L1+L2)/2;Cbp=(C1p+C2p)/2
    hbp=(h1p+h2p)/2 if abs(h1p-h2p)<=180 else (h1p+h2p+360)/2
    if C1p*C2p==0: hbp=h1p+h2p
    T=1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))+0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63))
    dth=30*math.exp(-((hbp-275)/25)**2)
    Rc=2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    Sl=1+0.015*(Lbp-50)**2/math.sqrt(20+(Lbp-50)**2);Sc=1+0.045*Cbp;Sh=1+0.015*Cbp*T
    Rt=-math.sin(math.radians(2*dth))*Rc
    return math.sqrt((dLp/Sl)**2+(dCp/Sc)**2+(dHp/Sh)**2+Rt*(dCp/Sc)*(dHp/Sh))
def nearest_ral(h):
    L=lab(h); best=min(RAL,key=lambda r: de2000(L,lab(r['hex'])))
    return best['id'], best['name'], best['hex'], round(de2000(L,lab(best['hex'])),1)
def cmyk(h):
    r,g,b=[x/255 for x in hex2rgb(h)]; k=1-max(r,g,b)
    if k==1: return (0,0,0,100)
    return tuple(round(v*100) for v in ((1-r-k)/(1-k),(1-g-k)/(1-k),(1-b-k)/(1-k),k))
