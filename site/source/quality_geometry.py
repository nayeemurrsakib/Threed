"""Shared construction tools for the camera-standard collection.

These helpers supply geometry, not automatic art direction. Each recipe must author
its proportions, material response and assembly groups before the export gate passes.
"""
import math
from math import pi, sin, cos, sqrt
from camera_benchmark import add_mesh, smooth_profile, group

STANDARD='camera-craft-v1'
PALETTE={
    'body':('#f5f5f1',.23,0),'accent':('#a4b3dd',.25,0),
    'secondary':('#bcc8e9',.35,0),'ink':('#191d24',.34,.06),
    'metal':('#b8bdc3',.20,.92),'lens':('#102128',.13,.08),
    'paper':('#eff1ed',.68,0),'rubber':('#25282d',.76,0),
    'glass':('#aec6cf',.065,0),'circuit':('#364b42',.58,.05),
    'fabric':('#a4b3dd',.88,0),'leather':('#8f9fba',.62,0),
    'coffee':('#321b10',.18,0),'sand':('#d1b589',.91,0),
}

def prepare(m):
    m.parts=[];m.group={};m.palette=dict(PALETTE);m.alpha={'glass':.10}
    m.preferredPalette='Cobalt';m.qualityStandard=STANDARD
    m.presentation={'viewDirection':[.42,.32,1],'explodeYaw':-.18,'contactShade':.36,'study':STANDARD}

def finish(m):
    for i,p in enumerate(m.parts):
        if not all(k in p for k in ('layer','explode','delay')):
            raise ValueError(f'{m.slug}: part {i} needs an authored assembly')
        if p['name'].startswith(p['mat']+'-') or p['name'] in ('fine-knurled-edge','perforated-speaker-sheet'):
            p['name']=p['layer'].lower().replace(' ','-')+f'-{i+1:03d}'
    m.group={}

def curve(points,steps=6):
    """Centripetal-style bounded Catmull sampling for 3D cables/handles."""
    out=[]
    for i in range(len(points)-1):
        a=points[max(0,i-1)];b=points[i];c=points[i+1];d=points[min(len(points)-1,i+2)]
        for j in range(steps):
            t=j/steps
            out.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in range(3)))
    return out+[points[-1]]

def cable(m,points,r,mat='metal'):m.tube(curve(points,8),r,mat)

def lathe(m,profile,pos=(0,0,0),mat='body',rot=(0,0,0),label='sculpted-surface',seg=96,steps=5):
    p=smooth_profile(profile,steps)
    # Overshoot across the axis can create inside-out tiny rings.
    m.lathe([(max(0,r),y) for r,y in p],pos,mat,rot,seg,label)

def bowl(m,pos,r,h,mat='body',thickness=.035):
    """Open vessel with a continuous rounded base, inner well and rolled lip."""
    profile=[(0,0),(r*.68,0),(r*.84,h*.08),(r*.94,h*.32),(r,h*.90),
             (r,h*.98),(r-thickness*.5,h+thickness*.25),(r-thickness,h*.98),
             (r-thickness,h*.90),(r*.94-thickness,h*.34),(r*.80-thickness,h*.14),(0,h*.14)]
    lathe(m,profile,pos,mat,label='hollow-vessel-with-rolled-lip',seg=112)

def ring(m,pos,outer,inner,depth,mat='metal',rot=(0,0,0),label='machined-annular-ring'):
    b=min((outer-inner)*.22,depth*.23,.018)
    profile=[(inner,-depth/2+b),(inner+b,-depth/2),(outer-b,-depth/2),(outer,-depth/2+b),
             (outer,depth/2-b),(outer-b,depth/2),(inner+b,depth/2),(inner,depth/2-b),(inner,-depth/2+b)]
    lathe(m,profile,pos,mat,rot,label,seg=112,steps=3)

def front(m,pos,r,depth,mat='ink',top=None,label=None):
    m.cyl(pos,r,depth,mat,(pi/2,0,0),top,label)

def screws(m,locations,r=.015,frontward=True):
    rot=(pi/2,0,0) if frontward else (0,0,0)
    for x,y,z in locations:
        m.cyl((x,y,z),r,.008,'metal',rot,label='recessed-slotted-fastener')
        m.box((x,y,z+.005) if frontward else (x,y+.005,z),(r*1.2,.003,.002) if frontward else (r*1.2,.002,.003),'ink',.0007,label='fastener-drive')

def feet(m,xs=(-.4,.4),zs=(-.23,.23),y=.025,r=.055):
    for x in xs:
        for z in zs:m.cyl((x,y,z),r,y*2,'rubber',label='inset-nonslip-foot')

def outline(w,h,r,n=24):
    """Counterclockwise rounded-rectangle perimeter, centered in XY."""
    pts=[];r=min(r,w/2*.98,h/2*.98)
    for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,pi/2),(-w/2+r,-h/2+r,pi),(w/2-r,-h/2+r,pi*1.5)]:
        for i in range(n+1):
            a=start+pi/2*i/n;pts.append((cx+r*cos(a),cy+r*sin(a)))
    return pts+[pts[0]]

def tray(m,pos,size,mat='body',corner=.13,wall=.03,axis='z',flip=False,label='hollow-rounded-housing'):
    """Moulded tray: a back panel and real inner sidewalls, open on +axis.

    size is expressed in world XYZ; a companion tray can close the assembly.
    Rims are sampled through their radius, instead of relying on smooth normals
    to disguise coarse corners. No solid plate fills the visible opening.
    """
    w,h,d=(size[0],size[1],size[2]) if axis=='z' else (size[0],size[2],size[1])
    b=min(.065,d*.3,corner*.45);profiles=[(wall+b,-d/2+wall),(wall,-d/2+wall+b),(wall,d/2-.008),(wall*.65,d/2),(0,d/2-.005),(0,-d/2+b)]
    for i in range(1,13):
        a=pi/2*i/12;profiles.append((b*(1-cos(a)),-d/2+b-b*sin(a)))
    pts=[];idx=[];N=len(outline(w,h,corner))
    # First/last collapsed rings close the floor on both sides.
    rings=[[(0,0,-d/2+wall)]]+[[(x,y,z) for x,y in outline(w-2*inset,h-2*inset,max(.012,corner-inset))] for inset,z in profiles]+[[(0,0,-d/2)]]
    for row in rings:
        if len(row)==1:row=row*N
        for x,y,z in row:
            if flip:z=-z
            q=(x,y,z) if axis=='z' else (x,z,-y)
            pts.append([q[k]+pos[k] for k in range(3)])
    for j in range(len(rings)-1):
        for i in range(N-1):
            a=j*N+i;b=a+N;idx.extend([a,b,a+1,a+1,b,b+1] if not flip else [a,a+1,b,a+1,b+1,b])
    add_mesh(m,pts,idx,mat,label,len(rings),N)

def lid(m,pos,size,mat='body',corner=.13,axis='y',label='fitted-rounded-cover'):
    # A separate shallow tray gives the cover an underside during separation.
    tray(m,pos,size,mat,corner,.025,axis,True,label)

def marks(m,center,r,count=60,plane='z',mat='ink'):
    for i in range(count):
        a=i*2*pi/count;long=i%5==0;l=.055 if long else .024
        if plane=='z':
            p=(center[0]+r*sin(a),center[1]+r*cos(a),center[2]);size=(.008,l,.004);rot=(0,0,-a)
        else:p=(center[0]+r*sin(a),center[1],center[2]+r*cos(a));size=(.008,.004,l);rot=(0,a,0)
        m.box(p,size,mat,.0015,rot,label='precision-dial-index')

def seams(m,points,r=.006,mat='paper'):cable(m,points,r,mat)

def optical(m,center,r,offset=(0,.02,.6),name='Optical window'):
    x,y,z=center;group(m,name,offset,.10)
    ring(m,center,r,r*.77,.055,'metal',(pi/2,0,0))
    front(m,(x,y,z-.025),r*.78,.025,'lens')
    m.ball((x,y,z+.01),r*.76,'glass',scale=(1,1,.12),seg=96,rings=32,label='convex-transparent-window')

def shape_loft(m,contour,depth,pos=(0,0,0),mat='body',label='continuous-sculpted-form'):
    """Cushioned closed extrusion of a smooth XY silhouette."""
    area=sum(contour[i][0]*contour[(i+1)%len(contour)][1]-contour[(i+1)%len(contour)][0]*contour[i][1] for i in range(len(contour)))
    if area>0:contour=list(reversed(contour))
    edge=smooth_profile(contour+[contour[0]],6);N=len(edge);pts=[];idx=[]
    for scale,z in [(0,-depth/2),(.78,-depth/2),(1,-depth*.30),(1,0),(1,depth*.30),(.78,depth/2),(0,depth/2)]:
        for x,y in edge:pts.append([x*scale+pos[0],y*scale+pos[1],z+pos[2]])
    for j in range(6):
        for i in range(N-1):
            a=j*N+i;b=a+N;idx.extend([a,b,a+1,a+1,b,b+1])
    add_mesh(m,pts,idx,mat,label,7,N)

def organic(m,lobes,mat='body',label='continuous-organic-surface',seg=112,rings=64):
    """A smooth implicit blend, sampled as a single star-shaped skin.

    Lobes are Gaussian fields (center, radii). This keeps a cloud or a toy's
    neck continuous instead of leaving intersecting-sphere seams in the finish.
    Use only connected star-shaped fields; concave/holed shapes need authored lofts.
    """
    center=[sum(c[k] for c,r in lobes)/len(lobes) for k in range(3)];pts=[];norm=[];idx=[]
    def field(p):return sum(math.exp(-2*sum(((p[k]-c[k])/r[k])**2 for k in range(3))) for c,r in lobes)
    if field(center)<.28:raise ValueError('Organic skin requires a connected central field')
    for j in range(rings+1):
        t=pi*j/rings
        for i in range(seg+1):
            a=2*pi*i/seg;v=[sin(t)*cos(a),cos(t),sin(t)*sin(a)];lo=0.;hi=4.
            for _ in range(23):
                d=(lo+hi)*.5;p=[center[k]+v[k]*d for k in range(3)]
                if field(p)>.28:lo=d
                else:hi=d
            p=[center[k]+v[k]*(lo+hi)*.5 for k in range(3)];n=[0.,0.,0.]
            for c,r in lobes:
                f=math.exp(-2*sum(((p[k]-c[k])/r[k])**2 for k in range(3)))
                for k in range(3):n[k]+=f*(p[k]-c[k])/(r[k]*r[k])
            length=sqrt(sum(x*x for x in n));norm.append([x/length for x in n]);pts.append(p)
    for j in range(rings):
        for i in range(seg):a=j*(seg+1)+i;b=a+seg+1;idx.extend([a,a+1,b,a+1,b+1,b])
    m.mesh(pts,norm,idx,mat,label=label)
