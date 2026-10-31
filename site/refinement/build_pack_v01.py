"""Little Things Vol. 01 — original procedural models. Python 3, no geometry dependencies.
Run from any directory. NumPy + Pillow are required only for the preview renderer.
All assets use Y up, metres, floor origin and named editable PBR materials.
"""
import array, json, math, pathlib, struct
from math import sin, cos, pi, sqrt

ROOT = pathlib.Path(__file__).resolve().parents[1]
PALETTE = {
    'body': ('#e8e4d8', .30, 0), 'accent': ('#e66e45', .26, 0),
    'secondary': ('#9ebaaa', .40, 0), 'ink': ('#293330', .37, .08),
    'metal': ('#b4a078', .23, .72), 'lens': ('#17272a', .10, .28),
    'paper': ('#f5eddb', .65, 0), 'rubber': ('#444844', .80, 0),
}
def rgb(h):
    c = [int(h[i:i+2],16)/255 for i in (1,3,5)]
    return [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
def unit(v):
    s = sqrt(sum(x*x for x in v)) or 1
    return [x/s for x in v]
def matrix(rot):
    x,y,z = rot; sx,cx,sy,cy,sz,cz = sin(x),cos(x),sin(y),cos(y),sin(z),cos(z)
    return [[cz*cy,cz*sy*sx-sz*cx,cz*sy*cx+sz*sx],
            [sz*cy,sz*sy*sx+cz*cx,sz*sy*cx-cz*sx],[-sy,cy*sx,cy*cx]]
def trans(v,r): return [sum(r[i][j]*v[j] for j in range(3)) for i in range(3)]

class Model:
    def __init__(self,slug,name,category,description):
        self.slug,self.name,self.category,self.description=slug,name,category,description
        self.parts=[]
    def mesh(self,p,n,idx,mat='body',pos=(0,0,0),rot=(0,0,0),label=None):
        r=matrix(rot)
        p=[[a+b for a,b in zip(trans(v,r),pos)] for v in p]
        n=[unit(trans(v,r)) for v in n]
        self.parts.append({'p':p,'n':n,'i':idx,'mat':mat,'name':label or f'{mat}-{len(self.parts):02d}'})
    def ball(self,pos,r,mat='body',scale=(1,1,1),rot=(0,0,0),seg=32,rings=16,label=None):
        p=[]; n=[]; idx=[]
        for j in range(rings+1):
            t=pi*j/rings
            for i in range(seg+1):
                a=2*pi*i/seg; v=[sin(t)*cos(a),cos(t),sin(t)*sin(a)]
                p.append([v[k]*r*scale[k] for k in range(3)])
                n.append(unit([v[k]/scale[k] for k in range(3)]))
        for j in range(rings):
            for i in range(seg):
                a=j*(seg+1)+i; b=a+seg+1
                idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def box(self,pos,size,mat='body',bevel=.08,rot=(0,0,0),label=None):
        # A rounded box: subdivided cube projected to the Minkowski sum of a box and sphere.
        half=[v/2 for v in size]; b=min(bevel,min(half)*.96); inner=[x-b for x in half]
        p=[]; n=[]; idx=[]; sub=8
        for axis in range(3):
            u=(axis+1)%3; v=(axis+2)%3
            for sign in (-1,1):
                start=len(p)
                for j in range(sub+1):
                    for i in range(sub+1):
                        q=[0.,0.,0.]; q[axis]=sign*half[axis]
                        q[u]=(2*i/sub-1)*half[u]; q[v]=(2*j/sub-1)*half[v]
                        near=[max(-inner[k],min(inner[k],q[k])) for k in range(3)]
                        normal=unit([q[k]-near[k] for k in range(3)])
                        p.append([near[k]+b*normal[k] for k in range(3)]); n.append(normal)
                for j in range(sub):
                    for i in range(sub):
                        a=start+j*(sub+1)+i; c=a+sub+1
                        idx += [a,a+1,c,a+1,c+1,c] if sign>0 else [a,c,a+1,a+1,c,c+1]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def lathe(self,profile,pos=(0,0,0),mat='body',rot=(0,0,0),seg=48,label=None):
        p=[]; n=[]; idx=[]
        for j,(radius,y) in enumerate(profile):
            before=profile[max(0,j-1)]; after=profile[min(len(profile)-1,j+1)]
            dr=after[0]-before[0]; dy=after[1]-before[1]
            for i in range(seg+1):
                a=2*pi*i/seg
                p.append([radius*cos(a),y,radius*sin(a)])
                n.append(unit([dy*cos(a),-dr,dy*sin(a)]))
        for j in range(len(profile)-1):
            for i in range(seg):
                a=j*(seg+1)+i; b=a+seg+1
                idx += [a,b,a+1,a+1,b,b+1]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def cyl(self,pos,r,h,mat='body',rot=(0,0,0),top=None,label=None):
        t=r if top is None else top; b=min(.035,h*.14,r*.12)
        self.lathe([(0,-h/2),(r-b,-h/2),(r,-h/2+b),(t,h/2-b),(t-b,h/2),(0,h/2)],pos,mat,rot,label=label)
    def torus(self,pos,r,t,mat='body',rot=(0,0,0),arc=2*pi,seg=48):
        p=[]; n=[]; idx=[]; radial=10
        for j in range(seg+1):
            a=arc*j/seg
            for i in range(radial+1):
                b=2*pi*i/radial
                p.append([(r+t*cos(b))*cos(a),t*sin(b),(r+t*cos(b))*sin(a)])
                n.append([cos(b)*cos(a),sin(b),cos(b)*sin(a)])
        for j in range(seg):
            for i in range(radial):
                a=j*(radial+1)+i; b=a+radial+1
                idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat,pos,rot)
    def rod(self,a,b,r,mat='metal'):
        d=[b[i]-a[i] for i in range(3)]; length=sqrt(sum(v*v for v in d))
        # Rotating a Y-axis cylinder with Rz * Rx.
        rot=(math.atan2(d[2],sqrt(d[0]**2+d[1]**2)),0,-math.atan2(d[0],d[1]))
        self.cyl(tuple((a[i]+b[i])/2 for i in range(3)),r,length,mat,rot)
    def tube(self,points,r,mat='body'):
        # Parallel local frame, open ends; enough for stylized handles and cables.
        p=[]; n=[]; idx=[]; sides=12
        for j,point in enumerate(points):
            a=points[max(0,j-1)]; b=points[min(len(points)-1,j+1)]
            tangent=unit([b[k]-a[k] for k in range(3)])
            ref=[0,0,1] if abs(tangent[2])<.9 else [0,1,0]
            u=unit([tangent[1]*ref[2]-tangent[2]*ref[1],tangent[2]*ref[0]-tangent[0]*ref[2],tangent[0]*ref[1]-tangent[1]*ref[0]])
            v=[tangent[1]*u[2]-tangent[2]*u[1],tangent[2]*u[0]-tangent[0]*u[2],tangent[0]*u[1]-tangent[1]*u[0]]
            for i in range(sides+1):
                a=2*pi*i/sides; normal=[u[k]*cos(a)+v[k]*sin(a) for k in range(3)]
                p.append([point[k]+r*normal[k] for k in range(3)]); n.append(normal)
        for j in range(len(points)-1):
            for i in range(sides):
                a=j*(sides+1)+i; b=a+sides+1; idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat)
    def normalize(self):
        verts=[p for part in self.parts for p in part['p']]
        lo=[min(v[k] for v in verts) for k in range(3)]; hi=[max(v[k] for v in verts) for k in range(3)]
        factor=2/max(hi[k]-lo[k] for k in range(3)); center=[(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2]
        for part in self.parts: part['p']=[[(v[k]-center[k])*factor for k in range(3)] for v in part['p']]
        return [round((hi[k]-lo[k])*factor,4) for k in range(3)]

MODELS=[]
def model(slug,name,category,description):
    m=Model(slug,name,category,description); MODELS.append(m); return m
def front(m,pos,r,h,mat='ink',top=None): m.cyl(pos,r,h,mat,(pi/2,0,0),top)
def feet(m,xs=(-.53,.53),zs=(-.3,.3),y=.08):
    for x in xs:
        for z in zs: m.cyl((x,y,z),.075,.12,'rubber')
def arc_points(cx,cy,z,rx,ry,start=0,end=pi,count=25):
    return [(cx+rx*cos(start+(end-start)*j/(count-1)),cy+ry*sin(start+(end-start)*j/(count-1)),z) for j in range(count)]
def screen(m,pos,size): m.box(pos,size,'lens',min(size)*.25)
def dial(m,pos,r=.12):
    front(m,pos,r,.09,'metal'); m.box((pos[0],pos[1]+r*.35,pos[2]+.055),(.025,r*.6,.015),'ink',.008)

def build_desk():
    m=model('dome-lamp','Dome lamp','Desk','Low domed shade, sculpted stem and heavy circular base.')
    m.cyl((0,.09,0),.56,.18,'secondary'); m.cyl((0,.55,0),.09,.9,'metal')
    m.lathe([(0,.98),(.59,.98),(.67,1.01),(.68,1.06),(.65,1.23),(.54,1.42),(.35,1.55),(0,1.6)],mat='accent')
    m.cyl((0,.99,0),.55,.025,'paper'); m.ball((0,1.64,0),.055,'metal')
    m=model('task-lamp','Task lamp','Desk','Articulated desk light with two pivot joints.')
    m.cyl((0,.09,0),.52,.18,'body'); m.rod((0,.15,0),(-.37,.85,0),.045)
    m.ball((-.37,.85,0),.1,'accent'); m.rod((-.37,.85,0),(.22,1.38,0),.045)
    m.ball((.22,1.38,0),.1,'accent'); m.cyl((.42,1.28,0),.26,.43,'secondary',(0,0,.65),top=.14)
    m=model('pencil-cup','Pencil cup','Desk','Open ceramic vessel with three contrasting writing tools.')
    m.lathe([(0,0),(.36,0),(.42,.05),(.42,.83),(.38,.87),(.34,.83),(.34,.09),(0,.09)],mat='secondary')
    for x,h,z,c in [(-.18,1.45,0,'accent'),(.11,1.65,-.08,'metal'),(.2,1.3,.13,'ink')]:
        m.cyl((x,h/2,z),.037,h,c); m.cyl((x,h+.06,z),.037,.12,'paper',top=0)
    m=model('stapler','Stapler','Desk','Weighted desktop stapler with a visible hinge and metal jaw.')
    m.box((0,.12,0),(1.5,.2,.5),'ink',.07); m.box((-.02,.34,0),(1.35,.24,.46),'accent',.1,rot=(0,0,.1))
    m.box((.35,.22,0),(.7,.055,.27),'metal',.02); front(m,(-.55,.3,.25),.075,.04,'metal')
    m=model('pocket-notebook','Pocket notebook','Desk','Clothbound notebook with page block, elastic and ribbon.')
    m.box((0,.13,0),(1.12,.16,1.5),'paper',.045)
    for y in (.025,.245): m.box((0,y,0),(1.2,.055,1.59),'secondary',.055)
    m.box((-.56,.135,0),(.12,.27,1.6),'secondary',.045)
    m.box((.38,.28,0),(.075,.025,1.58),'accent',.01); m.box((.04,.12,.85),(.09,.022,.28),'accent',.01)
    for y in (.1,.14,.18): m.box((.565,y,0),(.008,.009,1.35),'body',.002)
    m=model('calculator','Calculator','Desk','Rounded desktop calculator with individual tactile keys.')
    m.box((0,.15,0),(1.0,.28,1.55),'body',.12); screen(m,(0,.3,-.48),(.72,.03,.32))
    for row in range(4):
        for col in range(3): m.box((-.29+col*.29,.315,-.08+row*.29),(.21,.055,.2),'accent' if col==2 else 'secondary',.045)
    m=model('tape-dispenser','Tape dispenser','Desk','Curved weighted tape dispenser with exposed spool and blade.')
    m.box((0,.13,0),(1.35,.22,.48),'secondary',.1)
    m.box((-.35,.35,0),(.5,.5,.43),'secondary',.18)
    m.torus((-.28,.53,0),.28,.105,'paper',(pi/2,0,0)); front(m,(-.28,.53,.18),.12,.11,'metal')
    m.box((.52,.32,0),(.14,.35,.46),'secondary',.045); m.box((.52,.51,0),(.22,.035,.42),'metal',.01)
    m.box((.1,.57,0),(.67,.02,.26),'paper',.005,rot=(0,0,-.12))
    m=model('alarm-clock','Alarm clock','Desk','Twin-bell clock with raised hands and minute markers.')
    front(m,(0,.73,0),.55,.32,'secondary'); front(m,(0,.73,.19),.46,.045,'paper')
    for a in range(12):
        t=2*pi*a/12; m.ball((.39*sin(t),.73+.39*cos(t),.23),.022,'ink',seg=12,rings=6)
    m.rod((0,.73,.25),(-.18,.92,.25),.018,'ink'); m.rod((0,.73,.26),(.23,.87,.26),.014,'accent')
    m.ball((0,.73,.27),.04,'metal');
    for x in (-.34,.34):
        m.ball((x,1.27,0),.23,'accent',scale=(1,.6,1)); m.rod((x*.8,.3,0),(x*1.15,.03,0),.04,'metal')
    m.tube(arc_points(0,1.2,-.04,.3,.27),.025,'metal')
    m=model('sand-timer','Sand timer','Desk','Hourglass with translucent-looking shell and a sculpted sand cone.')
    for y in (.07,1.43): m.cyl((0,y,0),.46,.14,'secondary')
    m.lathe([(0,.17),(.31,.17),(.34,.25),(.31,.43),(.1,.72),(.07,.75),(.1,.78),(.31,1.07),(.34,1.25),(.31,1.33),(0,1.33)],mat='body')
    for x,z in [(-.34,-.19),(.34,-.19),(0,.38)]: m.rod((x,.14,z),(x,1.36,z),.035,'metal')
    m.lathe([(0,.17),(.28,.17),(.02,.55),(0,.55)],mat='accent')
    m=model('fountain-pen','Fountain pen','Desk','Pocket pen with brass nib, cap band and sculpted clip.')
    m.cyl((0,.64,0),.13,1.15,'secondary',top=.105); m.cyl((0,1.27,0),.11,.12,'metal')
    m.cyl((0,1.43,0),.1,.22,'metal',top=.005); m.box((0,1.44,.09),(.012,.21,.012),'ink',.003)
    m.cyl((0,.13,0),.15,.26,'accent'); m.rod((.145,.18,0),(.145,.75,0),.022,'metal')

def build_devices():
    m=model('rangefinder-camera','Rangefinder','Devices','Compact retro camera with stepped lens, viewfinder and top dials.')
    m.box((0,.61,0),(1.6,1.04,.65),'body',.19); m.box((0,.39,.32),(1.55,.38,.045),'secondary',.05)
    front(m,(.15,.6,.4),.36,.2,'ink'); front(m,(.15,.6,.53),.29,.16,'metal'); front(m,(.15,.6,.63),.225,.07,'lens')
    front(m,(.15,.6,.675),.16,.025,'ink'); m.ball((.08,.69,.69),.045,'body',scale=(1,1,.1))
    screen(m,(-.52,.91,.342),(.26,.18,.025)); m.cyl((.49,1.18,0),.14,.1,'metal'); m.cyl((-.42,1.18,0),.085,.09,'accent')
    for x in (-.83,.83): front(m,(x,.85,0),.055,.1,'metal')
    m=model('portable-radio','Portable radio','Devices','Horizontal radio with slotted speaker, tuner and angled antenna.')
    m.box((0,.56,0),(1.7,1.0,.62),'secondary',.17)
    m.box((-.28,.56,.325),(.88,.69,.04),'body',.06)
    for x in range(11):
        for y in range(7): front(m,(-.64+x*.072,.32+y*.075,.355),.014,.012,'ink')
    dial(m,(.55,.47,.35),.2); screen(m,(.48,.86,.33),(.42,.12,.035))
    m.rod((-.52,1.07,-.1),(.14,1.72,-.1),.015,'metal'); m.ball((.14,1.72,-.1),.028,'metal')
    m.tube(arc_points(0,1.05,-.12,.5,.28),.035,'ink')
    m=model('over-ear-headphones','Headphones','Devices','Over-ear headset with a padded arched headband and split cups.')
    m.tube(arc_points(0,.72,0,.65,.78),.075,'secondary')
    m.tube(arc_points(0,.72,0,.58,.69,.1,pi-.1),.055,'rubber')
    for x in (-.64,.64):
        m.box((x,.5,0),(.27,.6,.44),'body',.13); m.box((x*.79,.5,0),(.12,.49,.35),'rubber',.06)
        m.box((x*1.07,.5,0),(.08,.37,.3),'accent',.035)
    m=model('game-controller','Game controller','Devices','Chunky controller with two analog sticks and colored face keys.')
    m.box((0,.42,0),(1.42,.48,.67),'body',.21)
    for x in (-.52,.52): m.box((x,.23,.25),(.45,.43,.75),'body',.2,rot=(0,x*.3,0))
    for x,z in [(-.27,.1),(.23,.25)]: m.cyl((x,.71,z),.12,.1,'rubber')
    m.box((-.47,.71,-.15),(.26,.055,.08),'ink',.02); m.box((-.47,.71,-.15),(.08,.055,.26),'ink',.02)
    for x,z in [(0,-.11),(.13,0),(0,.11),(-.13,0)]: m.cyl((.46+x,.7,-.16+z),.048,.06,'accent')
    m=model('bookshelf-speaker','Bookshelf speaker','Devices','Compact two-way speaker with concentric drivers and a status light.')
    m.box((0,.78,0),(.95,1.5,.74),'secondary',.14); m.box((0,.78,.38),(.8,1.32,.035),'ink',.07)
    for y,r in [(.55,.29),(1.15,.14)]:
        front(m,(0,y,.42),r,.07,'rubber'); front(m,(0,y,.47),r*.7,.045,'ink'); m.ball((0,y,.5),r*.4,'lens',scale=(1,1,.35))
    front(m,(.3,.18,.42),.025,.025,'accent')
    m=model('desktop-display','Desktop display','Devices','Freestanding display with inset screen, neck and heavy foot.')
    m.box((0,.075,0),(.94,.15,.65),'secondary',.1); m.box((0,.55,-.08),(.18,.9,.18),'metal',.06)
    m.box((0,1.14,0),(1.78,1.1,.18),'body',.1); screen(m,(0,1.15,.1),(1.57,.88,.035))
    front(m,(.7,.67,.105),.02,.02,'accent')
    m=model('mechanical-keyboard','Keyboard','Devices','Low-profile 40-key keyboard with a contrasting spacebar.')
    m.box((0,.1,0),(1.9,.2,.78),'body',.09)
    for row in range(4):
        for col in range(10):
            if row==3 and 2<=col<=6: continue
            m.box((-.83+col*.183,.235,-.27+row*.18),(.153,.1,.14),'accent' if col in (0,9) else 'secondary',.035)
    m.box((-.1,.235,.27),(.88,.1,.14),'paper',.03)
    m=model('pocket-console','Pocket console','Devices','Portrait handheld console with inset screen, D-pad and two action buttons.')
    m.box((0,.84,0),(1.0,1.6,.23),'secondary',.16); m.box((0,1.12,.14),(.82,.65,.04),'ink',.075)
    screen(m,(0,1.13,.17),(.67,.49,.025)); m.box((-.25,.48,.15),(.29,.07,.09),'ink',.025)
    m.box((-.25,.48,.15),(.09,.07,.29),'ink',.025)
    for x,y in [(.2,.44),(.36,.58)]: front(m,(x,y,.16),.078,.05,'accent')
    for x in range(4): m.box((.13+x*.065,.18,.14),(.022,.12,.02),'ink',.009)
    m=model('studio-microphone','Studio microphone','Devices','Capsule microphone on a desktop stand with a yoke and grille.')
    m.cyl((0,.07,0),.43,.14,'ink'); m.cyl((0,.43,0),.055,.65,'metal')
    m.tube([(-.34,1.2,0),(-.34,.71,0),(0,.62,0),(.34,.71,0),(.34,1.2,0)],.04,'accent')
    m.box((0,1.16,0),(.49,.82,.43),'secondary',.22)
    for y in range(8): m.box((0,1.02+y*.061,.215),(.35,.02,.025),'ink',.009)
    front(m,(0,.91,.24),.047,.025,'metal')
    m=model('web-camera','Web camera','Devices','Capsule webcam on a pivoting monitor clip.')
    m.box((0,.1,0),(.68,.15,.48),'ink',.06); m.box((0,.28,0),(.13,.3,.14),'metal',.045)
    m.box((0,.6,0),(1.17,.48,.4),'body',.23); front(m,(0,.6,.24),.19,.12,'ink'); front(m,(0,.6,.31),.125,.04,'lens')
    front(m,(.42,.6,.22),.025,.02,'accent')

def build_kitchen():
    m=model('pour-over-kettle','Pour-over kettle','Kitchen','Rounded enamel kettle with arched handle and slender gooseneck.')
    m.lathe([(0,0),(.43,0),(.5,.08),(.53,.38),(.46,.75),(.29,.91),(0,.91)],mat='secondary')
    m.cyl((0,.94,0),.31,.07,'body'); m.ball((0,1.03,0),.075,'metal')
    m.tube(arc_points(-.02,.68,-.13,.51,.62,-.1,pi+.1),.065,'ink')
    m.tube([(.43,.23,0),(.61,.25,0),(.72,.4,0),(.77,.7,0),(.87,.91,0),(1.03,.97,0)],.053,'body')
    m=model('stovetop-brewer','Stovetop brewer','Kitchen','Faceted coffee brewer with a narrow waist and offset handle.')
    m.lathe([(0,0),(.42,0),(.43,.08),(.29,.6),(.28,.66),(.45,.75),(.43,1.2),(.33,1.28),(0,1.28)],mat='metal',seg=8)
    m.cyl((0,1.3,0),.44,.055,'secondary'); m.ball((0,1.4,0),.095,'ink')
    m.tube([(.39,1.18,0),(.7,1.15,0),(.76,.9,0),(.58,.71,0),(.4,.77,0)],.07,'ink')
    m.box((-.37,1.15,0),(.32,.14,.2),'metal',.03,rot=(0,0,-.3))
    m=model('two-slot-toaster','Toaster','Kitchen','Two-slot toaster with raised levers, vents and a circular browning dial.')
    m.box((0,.52,0),(1.5,.92,.79),'body',.23); m.box((0,.12,0),(1.4,.17,.7),'secondary',.06)
    for z in (-.19,.19): m.box((0,.982,z),(1.1,.035,.14),'ink',.065)
    m.rod((.78,.3,0),(.78,.77,0),.024,'metal'); m.box((.86,.69,0),(.25,.07,.15),'accent',.03)
    dial(m,(.38,.39,.4),.12)
    m=model('lidded-pot','Lidded pot','Kitchen','Enamel cooking pot with two loop handles and a domed lid.')
    m.lathe([(0,0),(.49,0),(.61,.12),(.64,.63),(.62,.72),(0,.72)],mat='body')
    m.lathe([(0,.72),(.65,.72),(.65,.77),(.49,.85),(.28,.9),(0,.91)],mat='accent')
    m.ball((0,.98,0),.09,'metal',scale=(1,.7,1))
    for sign in (-1,1): m.tube([(sign*.59,.57,0),(sign*.86,.58,0),(sign*.9,.44,0),(sign*.63,.4,0)],.045,'secondary')
    m=model('countertop-blender','Blender','Kitchen','Rounded motor base with a faceted jar, handle and fitted lid.')
    m.box((0,.25,0),(.88,.5,.73),'accent',.16); dial(m,(0,.27,.39),.12)
    m.lathe([(0,.5),(.26,.5),(.34,.62),(.42,1.38),(.4,1.44),(0,1.44)],mat='body',seg=12)
    m.cyl((0,1.48,0),.44,.1,'ink'); m.cyl((0,1.57,0),.12,.1,'metal')
    m.tube([(.38,1.29,0),(.63,1.29,0),(.69,.86,0),(.35,.77,0)],.055,'secondary')
    for y in (.78,.94,1.1): m.box((-.12,y,.39),(.13,.018,.025),'secondary',.006)
    m=model('espresso-cup','Espresso cup','Kitchen','Thick ceramic cup, saucer and visible coffee surface.')
    m.lathe([(0,0),(.61,0),(.67,.04),(.62,.09),(.3,.1),(0,.1)],mat='secondary')
    m.lathe([(0,.1),(.27,.1),(.33,.17),(.38,.62),(.36,.66),(.31,.64),(.29,.22),(0,.2)],mat='body')
    m.cyl((0,.55,0),.323,.016,'ink'); m.torus((.39,.41,0),.18,.052,'body',(pi/2,0,0))
    m=model('insulated-bottle','Insulated bottle','Kitchen','Double-wall bottle with a contrasting screw lid and carrying loop.')
    m.lathe([(0,0),(.28,0),(.33,.06),(.33,1.15),(.27,1.27),(.23,1.3),(0,1.3)],mat='secondary')
    m.cyl((0,1.39,0),.26,.19,'accent'); m.torus((0,1.57,0),.13,.035,'metal',(pi/2,0,0),arc=pi)
    m.cyl((0,.1,0),.334,.12,'rubber')
    m=model('citrus-press','Citrus press','Kitchen','Manual citrus press with a fluted reamer and catch bowl.')
    m.lathe([(0,0),(.42,0),(.55,.12),(.62,.37),(.57,.43),(.49,.32),(.28,.2),(0,.2)],mat='secondary')
    m.lathe([(0,.22),(.22,.22),(.24,.34),(.18,.55),(.07,.76),(0,.78)],mat='accent',seg=12)
    for i in range(12):
        a=2*pi*i/12; m.rod((.21*cos(a),.31,.21*sin(a)),(.07*cos(a),.69,.07*sin(a)),.018,'body')
    m=model('kitchen-scale','Kitchen scale','Kitchen','Mechanical countertop scale with a raised pan and round dial.')
    m.box((0,.11,0),(.91,.2,.79),'secondary',.09); m.box((0,.49,0),(.69,.7,.57),'body',.17)
    front(m,(0,.52,.32),.27,.08,'metal'); front(m,(0,.52,.37),.23,.025,'paper')
    m.rod((0,.52,.39),(.12,.67,.39),.012,'accent')
    m.lathe([(0,.87),(.57,.87),(.63,.95),(.64,1.05),(.59,1.08),(.49,.98),(0,.98)],mat='metal')
    m=model('pepper-mill','Pepper mill','Kitchen','Sculptural pepper grinder with a pinched waist and brass top screw.')
    m.lathe([(0,0),(.32,0),(.36,.06),(.33,.19),(.23,.31),(.19,.65),(.24,.89),(.34,1.02),(.36,1.18),(.29,1.35),(0,1.4)],mat='secondary')
    m.cyl((0,.91,0),.27,.06,'metal'); m.cyl((0,1.44,0),.055,.09,'metal')

def build_commerce():
    m=model('shopping-tote','Shopping tote','Commerce','Structured shopping bag with rounded fabric handles.')
    m.box((0,.63,0),(1.16,1.22,.57),'secondary',.14)
    for z in (-.23,.23): m.tube(arc_points(0,1.14,z,.29,.48),.035,'body')
    m.box((0,.64,.295),(.41,.35,.025),'body',.05)
    m=model('ribbon-gift','Ribbon gift','Commerce','Wrapped square present with a ribbon cross and sculpted bow.')
    m.box((0,.5,0),(1.0,.96,1.0),'body',.1); m.box((0,1.0,0),(1.08,.13,1.08),'secondary',.055)
    m.box((0,.54,.515),(.14,.97,.025),'accent',.01); m.box((0,1.08,0),(.14,.025,1.1),'accent',.01)
    m.box((0,1.08,0),(1.1,.026,.14),'accent',.01)
    for sign in (-1,1): m.torus((sign*.19,1.2,0),.18,.035,'accent',(0,0,sign*.45))
    m.ball((0,1.19,0),.075,'accent')
    m=model('payment-terminal','Payment terminal','Commerce','Countertop card terminal with a screen and raised payment keys.')
    m.box((0,.21,0),(.8,.4,1.29),'secondary',.13); screen(m,(0,.423,-.31),(.58,.035,.48))
    for row in range(3):
        for col in range(3): m.box((-.21+col*.21,.44,.07+row*.22),(.16,.055,.15),'accent' if row==2 else 'body',.035)
    m.box((0,.22,.65),(.55,.06,.025),'ink',.015)
    m=model('delivery-parcel','Delivery parcel','Commerce','Rounded shipping box with paper tape, corner seam and label.')
    m.box((0,.57,0),(1.3,1.1,.93),'secondary',.08)
    m.box((0,1.128,0),(.22,.023,.94),'paper',.008); m.box((0,.63,.47),(.22,1.02,.02),'paper',.008)
    m.box((.29,.79,.48),(.35,.25,.025),'body',.02)
    for x in range(7): m.box((.17+x*.036,.79,.5),(.012,.16,.007),'ink',.002)
    m=model('market-basket','Market basket','Commerce','Open market basket with vertical slots and a folding arch handle.')
    m.box((0,.09,0),(1.2,.16,.82),'secondary',.06)
    for z in (-.39,.39):
        for x in range(9): m.box((-.53+x*.132,.39,z),(.065,.55,.065),'secondary',.025)
        m.box((0,.68,z),(1.25,.1,.1),'secondary',.04)
    for x in (-.58,.58):
        for z in (-.26,0,.26): m.box((x,.39,z),(.08,.55,.08),'secondary',.025)
    m.tube(arc_points(0,.68,0,.61,.59),.045,'accent')
    m=model('price-tag','Price tag','Commerce','Thick rounded tag with raised circular seal and tied cord.')
    m.box((0,.59,0),(.85,1.13,.13),'body',.13,rot=(0,0,-.15)); front(m,(.055,.96,.08),.07,.025,'metal')
    m.tube([(0,.97,.09),(-.1,1.21,.1),(.0,1.48,.06),(.25,1.48,0),(.33,1.25,-.06),(.13,1.02,-.07)],.018,'accent')
    front(m,(-.03,.47,.09),.23,.03,'secondary'); m.box((-.03,.47,.12),(.23,.045,.025),'paper',.018)
    m=model('coin-stack','Coin stack','Commerce','Two unequal coin stacks with raised face medallions.')
    for x,h,z in [(-.25,6,0),(.42,3,.15)]:
        for i in range(h):
            m.cyl((x,.07+i*.12,z),.33,.105,'metal'); m.torus((x,.12+i*.12,z),.27,.009,'body')
        m.cyl((x,.02+h*.12,z),.18,.012,'accent')
    m=model('store-awning','Storefront','Commerce','Miniature storefront with striped awning and recessed display window.')
    m.box((0,.66,0),(1.25,1.2,.68),'body',.08); screen(m,(-.18,.58,.36),(.63,.69,.025))
    m.box((.39,.48,.36),(.29,.88,.04),'secondary',.025); front(m,(.47,.47,.39),.025,.025,'metal')
    for i in range(7): m.box((-.6+i*.2,1.19,.35),(.2,.16,.72),'accent' if i%2==0 else 'paper',.035,rot=(.15,0,0))
    m.box((0,.04,.06),(1.48,.08,.94),'secondary',.025)
    m=model('receipt-printer','Receipt printer','Commerce','Desktop thermal printer with a curling receipt and feed button.')
    m.box((0,.45,0),(1.06,.85,.91),'secondary',.16); m.box((0,.7,.47),(.78,.075,.035),'ink',.025)
    m.box((0,1.01,.22),(.62,.58,.026),'paper',.015,rot=(-.15,0,0))
    for y in range(5): m.box((-.04,.84+y*.07,.28),(.38 if y%2==0 else .25,.014,.015),'ink',.003)
    m.cyl((.32,.87,.1),.07,.035,'accent')
    m=model('piggy-bank','Piggy bank','Commerce','Plump ceramic savings pig with four feet and a coin slot.')
    m.ball((0,.52,0),.51,'secondary',scale=(1.24,1,.9)); m.ball((.59,.53,0),.2,'accent',scale=(.55,.8,1))
    for x in (-.3,.3):
        for z in (-.26,.26): m.cyl((x,.13,z),.09,.26,'secondary')
    for z in (-.24,.24): m.cyl((.24,1.0,z),.14,.26,'secondary',top=.015)
    m.ball((.39,.72,.36),.028,'ink'); m.box((-.05,1.02,0),(.29,.016,.045),'ink',.014)
    m.torus((-.63,.58,0),.1,.022,'accent',(0,0,pi/2),arc=pi*1.7)

def build_travel():
    m=model('cabin-suitcase','Cabin suitcase','Travel','Ribbed hard-shell carry-on with telescoping handle and wheels.')
    m.box((0,.76,0),(1.0,1.3,.59),'secondary',.17)
    for x in (-.3,-.1,.1,.3): m.box((x,.77,.31),(.033,.94,.04),'body',.015)
    for x in (-.36,.36):
        m.rod((x*.7,1.37,0),(x*.7,1.83,0),.025,'metal'); front(m,(x,.08,0),.09,.15,'rubber')
    m.box((0,1.83,0),(.6,.1,.12),'ink',.045)
    m=model('weekend-backpack','Backpack','Travel','Rounded travel backpack with front pocket, top loop and two straps.')
    m.box((0,.79,0),(1.06,1.48,.57),'secondary',.25); m.box((0,.49,.35),(.83,.6,.27),'accent',.13)
    m.box((0,.75,.5),(.66,.028,.02),'metal',.009)
    m.tube(arc_points(0,1.47,0,.18,.17),.035,'ink')
    for x in (-.29,.29): m.tube([(x,1.29,-.28),(x,.92,-.53),(x,.38,-.47),(x,.2,-.22)],.055,'ink')
    m=model('binoculars','Binoculars','Travel','Twin optical barrels connected by a center hinge and focus wheel.')
    for x in (-.34,.34):
        m.cyl((x,.43,0),.28,.86,'secondary',(pi/2,0,0)); front(m,(x,.43,.47),.28,.12,'ink'); front(m,(x,.43,.54),.21,.025,'lens')
        front(m,(x,.43,-.47),.17,.12,'rubber')
    m.box((0,.43,0),(.34,.25,.46),'body',.07); m.cyl((0,.64,0),.12,.13,'accent')
    m=model('pocket-compass','Pocket compass','Travel','Open compass with cardinal markers, floating needle and a carrying ring.')
    m.cyl((0,.15,0),.58,.3,'metal'); m.cyl((0,.315,0),.5,.035,'paper')
    for i in range(16):
        a=2*pi*i/16; m.box((.43*sin(a),.343,.43*cos(a)),(.025,.012,.055),'ink',.005,rot=(0,a,0))
    m.cyl((0,.36,0),.04,.05,'metal'); m.box((0,.36,0),(.06,.04,.65),'accent',.02,rot=(0,.5,0))
    m.torus((0,.17,-.7),.13,.035,'metal')
    m=model('camp-lantern','Camp lantern','Travel','Protective lantern cage around a warm central diffuser.')
    for y in (.1,1.04): m.cyl((0,y,0),.4,.2,'secondary')
    m.cyl((0,.58,0),.24,.78,'paper')
    for a in range(4):
        t=2*pi*a/4; m.rod((.32*cos(t),.18,.32*sin(t)),(.32*cos(t),1.0,.32*sin(t)),.028,'metal')
    m.tube(arc_points(0,1.12,0,.32,.37),.035,'ink'); dial(m,(0,.12,.4),.065)
    m=model('travel-mug','Travel mug','Travel','Insulated takeaway mug with a thick lip and side handle.')
    m.lathe([(0,0),(.28,0),(.31,.06),(.37,.94),(.35,1.03),(0,1.03)],mat='secondary')
    m.cyl((0,1.07,0),.4,.13,'ink'); m.box((0,1.15,.12),(.18,.025,.26),'accent',.045)
    m.tube([(.34,.85,0),(.61,.86,0),(.68,.63,0),(.55,.35,0),(.31,.35,0)],.06,'secondary')
    m=model('passport-wallet','Passport wallet','Travel','Pocket travel document with inset emblem and layered page block.')
    m.box((0,.12,0),(.9,.16,1.32),'paper',.04)
    for y in (.02,.22): m.box((0,y,0),(.98,.06,1.4),'secondary',.055)
    m.cyl((0,.263,-.09),.23,.025,'metal'); m.torus((0,.281,-.09),.16,.012,'secondary')
    m.box((0,.264,.38),(.46,.022,.04),'metal',.014)
    m=model('folding-sunglasses','Sunglasses','Travel','Thick-framed round sunglasses with curved temples.')
    for x in (-.4,.4):
        m.torus((x,.46,0),.3,.055,'accent',(pi/2,0,0)); front(m,(x,.46,.005),.256,.035,'lens')
        m.tube([(x*1.8,.5,0),(x*1.8,.5,-.52),(x*1.6,.42,-.69)],.035,'accent')
    m.tube([(-.11,.5,0),(0,.56,0),(.11,.5,0)],.04,'accent')
    m=model('sun-cap','Sun cap','Travel','Soft six-panel cap with a curved bill and top button.')
    m.lathe([(.55,0),(.58,.08),(.56,.28),(.46,.51),(.28,.67),(0,.72)],mat='secondary')
    m.ball((0,.04,.5),.5,'accent',scale=(1.2,.10,1)); m.ball((0,.74,0),.055,'accent')
    for i in range(6):
        a=i*pi/3; points=[(.565*sin(t)*cos(a),.72*cos(t),.565*sin(t)*sin(a)) for t in [j*pi/2/16 for j in range(17)]]
        m.tube(points,.009,'body')
    m=model('key-fob','Key fob','Travel','Rounded leather-style fob, brass split ring and single house key.')
    m.box((-.19,.22,0),(.57,.42,.14),'secondary',.18)
    m.torus((.16,.38,0),.19,.025,'metal',(pi/2,0,0))
    m.box((.39,.17,0),(.17,.54,.09),'metal',.03,rot=(0,0,-.4))
    for y in (-.03,.07): m.box((.55,y,0),(.14,.07,.1),'metal',.012)

def build_play():
    m=model('orbit-sculpture','Orbit sculpture','Play','Interlocking sculptural hoops around a ceramic center sphere.')
    m.ball((0,.76,0),.3,'accent')
    for i,rot in enumerate([(0,0,0),(pi/2,.35,0),(.5,0,pi/2)]): m.torus((0,.76,0),.65,.038,'metal' if i==1 else 'secondary',rot)
    m.cyl((0,.06,0),.28,.12,'body'); m.rod((0,.1,0),(0,.47,0),.035,'metal')
    m=model('stacking-rings','Stacking rings','Play','Four softly inflated rings on a rounded central peg.')
    m.cyl((0,.08,0),.5,.16,'body'); m.cyl((0,.66,0),.075,1.18,'metal'); m.ball((0,1.28,0),.1,'accent')
    for i,(r,c) in enumerate([(.4,'secondary'),(.33,'accent'),(.26,'body'),(.19,'secondary')]): m.torus((0,.26+i*.25,0),r,.11,c)
    m=model('little-rocket','Little rocket','Play','Toy rocket with a round porthole and three sculpted fins.')
    m.lathe([(0,.14),(.21,.14),(.29,.32),(.32,.8),(.27,1.17),(.16,1.43),(0,1.59)],mat='body')
    front(m,(0,.96,.3),.17,.065,'metal'); front(m,(0,.96,.34),.12,.025,'lens')
    for a in [0,2*pi/3,4*pi/3]: m.box((.34*cos(a),.29,.34*sin(a)),(.16,.54,.33),'accent',.065,rot=(0,-a,0))
    m.cyl((0,.13,0),.15,.18,'ink',top=.2)
    m=model('rubber-duck','Rubber duck','Play','Sculpted bathing duck with flattened tail, broad beak and raised wings.')
    m.ball((0,.38,0),.45,'secondary',scale=(1.25,.8,1)); m.ball((.28,.86,0),.31,'secondary')
    m.ball((.59,.78,.015),.2,'accent',scale=(1.1,.32,.8)); m.ball((-.48,.46,0),.23,'secondary',scale=(1.1,.5,.7))
    for z in (-.33,.33): m.ball((0,.42,z),.25,'body',scale=(1.2,.6,.3))
    m.ball((.43,.96,.23),.032,'ink'); m.ball((.43,.96,-.23),.032,'ink')
    m=model('tiny-robot','Tiny robot','Play','Friendly box robot with two lens eyes and articulated-looking limbs.')
    m.box((0,.69,0),(.69,.64,.43),'secondary',.12); m.box((0,1.27,0),(.86,.53,.46),'body',.14)
    for x in (-.23,.23):
        front(m,(x,1.31,.26),.105,.055,'ink'); front(m,(x,1.31,.295),.055,.02,'lens')
        m.box((x,.19,0),(.22,.36,.28),'ink',.07); m.box((x,.06,.08),(.29,.12,.4),'body',.045)
        m.rod((x*1.8,.86,0),(x*2.1,.43,0),.055,'metal'); m.ball((x*2.1,.4,0),.1,'accent')
    m.rod((0,1.54,0),(0,1.72,0),.02,'metal'); m.ball((0,1.75,0),.06,'accent')
    m.box((0,.74,.24),(.25,.18,.04),'accent',.04)
    m=model('cloud-sculpture','Cloud sculpture','Play','Ceramic cloud built from overlapping soft volumes.')
    for x,y,r in [(-.47,.36,.34),(-.13,.57,.43),(.35,.43,.37),(.62,.31,.22)]: m.ball((x,y,0),r,'body',scale=(1,1,.7))
    m.box((.04,.22,0),(1.3,.3,.46),'body',.14)
    m=model('ceramic-rainbow','Ceramic rainbow','Play','Three thick standing arches on a rounded plinth.')
    m.box((0,.05,0),(1.5,.1,.43),'body',.045)
    for r,c in [(.62,'accent'),(.43,'body'),(.25,'secondary')]:
        m.tube(arc_points(0,.1,0,r,r,0,pi,40),.075,c)
    m=model('flower-vase','Flower vase','Play','Glazed bud vase with a brass stem and five-petal sculpted flower.')
    m.lathe([(0,0),(.26,0),(.38,.12),(.4,.35),(.29,.58),(.13,.69),(.12,.86),(.09,.88),(.07,.84),(.08,.68),(0,.64)],mat='secondary')
    m.rod((0,.65,0),(.08,1.52,0),.019,'metal')
    for i in range(5):
        a=2*pi*i/5; m.ball((.08+.21*sin(a),1.54+.21*cos(a),0),.145,'accent',scale=(1,1,.35))
    m.ball((.08,1.54,.07),.1,'metal',scale=(1,1,.4)); m.ball((.15,1.08,0),.15,'secondary',scale=(1,.35,.3),rot=(0,0,.5))
    m=model('wind-up-bird','Wind-up bird','Play','Small mechanical bird on two feet, with a rear winding key.')
    m.ball((0,.61,0),.4,'secondary',scale=(1.3,.9,.8)); m.ball((.34,.97,0),.24,'body')
    m.cyl((.61,.94,0),.08,.24,'accent',(0,0,-pi/2),top=0); m.ball((.43,1.05,.18),.027,'ink')
    for z in (-.24,.24):
        m.ball((-.02,.65,z),.22,'accent',scale=(1.2,.7,.22)); m.rod((.02,.37,z*.7),(.02,.09,z*.7),.022,'metal')
        m.box((.09,.06,z*.7),(.29,.07,.12),'metal',.025)
    m.torus((-.62,.58,0),.105,.022,'metal',(pi/2,0,0)); m.box((-.47,.58,0),(.2,.045,.06),'metal',.01)
    m=model('balance-mobile','Balance mobile','Play','Desktop kinetic sculpture with offset weights and a curved fulcrum.')
    m.cyl((0,.07,0),.39,.14,'body'); m.cyl((0,.71,0),.035,1.25,'metal'); m.ball((0,1.36,0),.065,'metal')
    m.rod((-.63,1.49,0),(.7,1.23,0),.022,'metal')
    m.rod((-.63,1.49,0),(-.63,.95,0),.015,'metal'); m.ball((-.63,.83,0),.18,'accent')
    m.rod((.7,1.23,0),(.7,.72,0),.015,'metal'); m.torus((.7,.57,0),.17,.055,'secondary',(pi/2,0,0))

def export_glb(m):
    bounds=m.normalize(); blob=bytearray(); views=[]; access=[]; meshes=[]; nodes=[]
    def accessor(values,kind,component,target,count,minmax=False):
        while len(blob)%4: blob.append(0)
        offset=len(blob); data=array.array('f' if component==5126 else 'I',values)
        import sys
        if sys.byteorder!='little': data.byteswap()
        blob.extend(data.tobytes()); vi=len(views)
        views.append({'buffer':0,'byteOffset':offset,'byteLength':len(data)*data.itemsize,'target':target})
        a={'bufferView':vi,'componentType':component,'count':count,'type':kind}
        if minmax:
            a['min']=[min(values[k::3]) for k in range(3)]; a['max']=[max(values[k::3]) for k in range(3)]
        access.append(a); return len(access)-1
    slots=list(PALETTE)
    for part in m.parts:
        pa=accessor([v for p in part['p'] for v in p],'VEC3',5126,34962,len(part['p']),True)
        na=accessor([v for p in part['n'] for v in p],'VEC3',5126,34962,len(part['n']))
        ia=accessor(part['i'],'SCALAR',5125,34963,len(part['i']))
        meshes.append({'name':part['name'],'primitives':[{'attributes':{'POSITION':pa,'NORMAL':na},'indices':ia,'material':slots.index(part['mat'])}]})
        nodes.append({'name':part['name'],'mesh':len(meshes)-1})
    materials=[{'name':slot,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':rgb(h)+[1],'roughnessFactor':rough,'metallicFactor':metal}} for slot,(h,rough,metal) in PALETTE.items()]
    doc={'asset':{'version':'2.0','generator':'Little Things original procedural studio / 1.0','copyright':'Original asset recipes supplied in source/build_pack.py'},
         'scene':0,'scenes':[{'name':m.name,'nodes':list(range(len(nodes)))}],'nodes':nodes,'meshes':meshes,'materials':materials,
         'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':access,
         'extras':{'category':m.category,'description':m.description,'materialSlots':slots,'units':'metres','upAxis':'Y','floorOrigin':True}}
    js=json.dumps(doc,separators=(',',':')).encode(); js+=b' '*((-len(js))%4); blob+=b'\0'*((-len(blob))%4)
    out=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(blob))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(blob),0x004E4942)+blob
    path=ROOT/'models'/f'{m.slug}.glb'; path.write_bytes(out)
    return {'id':m.slug,'name':m.name,'category':m.category,'description':m.description,'model':f'models/{m.slug}.glb',
            'thumbnail':f'previews/{m.slug}.png','dimensions':bounds,'triangles':sum(len(p['i'])//3 for p in m.parts),
            'vertices':sum(len(p['p']) for p in m.parts),'parts':len(m.parts),'bytes':len(out),'materialSlots':sorted(set(p['mat'] for p in m.parts))}

def main():
    for folder in ('models','previews','presets'): (ROOT/folder).mkdir(exist_ok=True)
    build_desk(); build_devices(); build_kitchen(); build_commerce(); build_travel(); build_play()
    assets=[export_glb(m) for m in MODELS]
    manifest={'name':'Little Things','volume':'01','version':'0.1.0','stage':'First collection / review edition','assetCount':len(assets),
              'categories':list(dict.fromkeys(a['category'] for a in assets)),'defaultPalette':{k:v[0] for k,v in PALETTE.items()},'assets':assets}
    (ROOT/'catalog.json').write_text(json.dumps(manifest,indent=2))
    palettes={
      'Workshop':{k:v[0] for k,v in PALETTE.items()},
      'Cobalt':{'body':'#e4e7ed','accent':'#3054d7','secondary':'#a2b1dc','ink':'#202939','metal':'#a4acb8','lens':'#14212b','paper':'#f2eee7','rubber':'#384455'},
      'Cherry':{'body':'#efddd2','accent':'#a82e40','secondary':'#d17b81','ink':'#392c31','metal':'#b79b75','lens':'#2c1926','paper':'#faebdf','rubber':'#4f373b'},
      'Butter':{'body':'#f3e5ba','accent':'#e3a53c','secondary':'#a6b695','ink':'#3a4135','metal':'#b99a62','lens':'#23352c','paper':'#fbf4de','rubber':'#4d5344'},
      'Lilac':{'body':'#e9e4f1','accent':'#8664b0','secondary':'#b3a7c4','ink':'#343044','metal':'#b8a8a0','lens':'#251f38','paper':'#f3ecf5','rubber':'#4b4359'},
      'Graphite':{'body':'#a7aaa7','accent':'#4b5854','secondary':'#d5d6cf','ink':'#252c29','metal':'#9b9f98','lens':'#1b2421','paper':'#ecece5','rubber':'#3c443f'}}
    (ROOT/'presets/palettes.json').write_text(json.dumps(palettes,indent=2))
    lighting={'Softbox':{'azimuth':-40,'elevation':48,'intensity':3.0,'fill':.65,'warmth':.15,'shadow':.55,'softness':2.5},
              'Daylight':{'azimuth':-65,'elevation':60,'intensity':3.5,'fill':.85,'warmth':-.18,'shadow':.35,'softness':3.0},
              'Golden hour':{'azimuth':-75,'elevation':23,'intensity':3.7,'fill':.35,'warmth':.8,'shadow':.7,'softness':1.2},
              'Gallery':{'azimuth':30,'elevation':65,'intensity':3.8,'fill':.3,'warmth':0,'shadow':.65,'softness':1.8}}
    (ROOT/'presets/lighting.json').write_text(json.dumps(lighting,indent=2))
    print(f'Built {len(assets)} original assets / {sum(a["triangles"] for a in assets):,} triangles / {sum(a["bytes"] for a in assets)/1e6:.1f} MB')
    return MODELS

if __name__=='__main__': main()
