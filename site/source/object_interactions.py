"""Attached ribbons, feeding paper, a sewn cap, light and a modest launch."""
from purposeful_motion import *

def gift(m):
    from craft_commerce import build
    build(m);freeze(m)
    presentation(m,'Open the gift; the side ribbon stays on the box','HOVER TO OPEN · DRAG TO EXPLORE',frame=.08)
    moving=[]
    for p in m.parts:
        center=sum(v[1] for v in p['p'])/len(p['p'])
        if p['layer']=='Fitted lid' or (p['layer']=='Satin ribbon' and center>1.02):moving.append(p)
    bind(moving,'Lid with attached bow',translate=[0,.32,0])
    m.description='A fitted gift box with a lifting lid and bow; the ribbon on the box sides remains fixed.'

def parcel(m):
    from craft_commerce import build
    build(m);m.parts=[p for p in m.parts if not(p['layer']=='Paper sealing tape' and sum(v[1] for v in p['p'])/len(p['p'])>1.08)];freeze(m)
    presentation(m,'Open the cut top flaps; the front tape stays put','HOVER TO OPEN THE FLAPS · DRAG TO EXPLORE',view=[.45,.48,1],frame=.08)
    for p in m.parts:
        if p['layer']=='Outer flap pair':
            sign=1 if sum(v[2] for v in p['p'])>0 else -1
            bind([p],('Front' if sign>0 else 'Rear')+' hinged top flap',(0,1.09,sign*.45),(1,0,0),sign*1.12)
        elif p['layer']=='Inner flap pair':
            sign=1 if sum(v[0] for v in p['p'])>0 else -1
            bind([p],('Right' if sign>0 else 'Left')+' inner flap',(sign*.62,1.06,0),angle=-sign*.80)
            p['delay']=.12
    for sign in (-1,1):
        action(m,('Front' if sign>0 else 'Rear')+' hinged top flap',(0,1.09,sign*.45),(1,0,0),sign*1.12)
        m.box((0,1.11,sign*.225),(.20,.007,.445),'paper',.003,label='cut-top-tape-attached-to-flap')
    m.description='An opening shipping carton with hinged top flaps, a cut top tape seam and stationary front sealing tape and label.'

def tote(m):
    presentation(m,'Lift the tote by its attached handles','HOVER TO PICK UP · DRAG TO EXPLORE',view=[.40,.28,1])
    m.palette['secondary']=('#bcc8e9',.91,0);m.palette['body']=('#f5f5f1',.89,0)
    action(m,'Sewn tote and attached handles',(0,1.35,0),angle=.055,translate=[0,.08,0]);m.group.update(blast=[0,-.10,0],blastGroup='Sewn canvas body')
    pts=[];idx=[];rows=32;N=len(outline(1.06,.48,.12,20))
    for inner in (False,True):
        for j in range(rows+1):
            t=(j/rows) if not inner else (1-j/rows);w=1.00+.075*sin(pi*t);d=.44+.035*sin(pi*t)
            for i,(x,z) in enumerate(outline(w-(.032 if inner else 0),d-(.032 if inner else 0),.12,20)):
                y=.055+1.03*t-.025*t**5*cos(4*pi*i/(N-1));pts.append([x,y,z])
    totalrows=2*(rows+1)
    for j in range(totalrows-1):
        for i in range(N-1):a=j*N+i;b=a+N;idx.extend([a,b,a+1,a+1,b,b+1])
    add_mesh(m,pts,idx,'secondary','continuous-open-canvas-tote',totalrows,N)
    m.box((0,.057,0),(.82,.018,.32),'secondary',.008,label='sewn-tote-bottom')
    for z in (-.22,.22):
        path=curve([(-.27,.91,z),(-.27,1.35,z),(-.16,1.48,z),(.16,1.48,z),(.27,1.35,z),(.27,.91,z)],12);p=[];ids=[]
        for j,q in enumerate(path):
            a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dx=b[0]-a[0];dy=b[1]-a[1];l=math.hypot(dx,dy) or 1;nx,ny=-dy/l,dx/l
            for side,front in [(-1,-1),(1,-1),(1,1),(-1,1)]:p.append([q[0]+nx*.023*side,q[1]+ny*.023*side,q[2]+front*.005])
        for j in range(len(path)-1):
            for k in range(4):a=j*4+k;b=j*4+(k+1)%4;c=a+4;d=b+4;ids.extend([a,b,c,b,d,c])
        m.group.update(blast=[0,.40,0],blastGroup='Woven carrying straps')
        add_mesh(m,p,ids,'body','flat-woven-attached-carry-strap')
        m.group.update(blast=[0,-.10,0],blastGroup='Sewn handle anchors')
        for x in (-.27,.27):m.box((x,.96,z),(.065,.18,.014),'body',.007,label='sewn-handle-anchor')
    m.description='An open soft canvas tote with a sewn bottom and flat handles that lift together with the bag.'

def printer(m):
    presentation(m,'Feed a printed receipt through the slot','HOVER TO PRINT · DRAG TO EXPLORE',view=[.42,.33,1],frame=.10)
    m.description='A fitted desktop receipt printer that feeds a curled printed sheet through its output slot while the case stays closed.'
    still(m,'Closed printer enclosure');m.box((0,.44,0),(1.06,.80,.88),'secondary',.15);feet(m,(-.34,.34),(-.25,.25),.034)
    panel(m,(0,.829,0),(1.015,.065,.835),'secondary',.14,'y','matching-radius-closed-printer-lid')
    m.box((0,.867,.31),(.72,.009,.09),'ink',.004,label='recessed-paper-feed-slot');m.cyl((.34,.87,-.17),.045,.015,'accent')
    action(m,'Feeding printed receipt',translate=[0,.52,0])
    pts=[];ids=[];N=64
    for i in range(N+1):
        t=i/N;y=.16+.76*t;z=.31+.055*sin(t*pi*.9)
        pts.extend([[-.29,y,z],[.29,y,z]])
    for i in range(N):a=i*2;ids.extend([a,a+1,a+2,a+1,a+3,a+2])
    add_mesh(m,pts,ids,'paper','continuous-feeding-receipt')
    for j in range(10):
        t=.19+j*.068;y=.16+.76*t;z=.315+.055*sin(t*pi*.9)
        m.box((-.02,y,z),(.36 if j%3 else .23,.006,.0015),'ink',.0005,label='printed-receipt-rule')

def lantern(m):
    from craft_travel import build
    build(m);freeze(m)
    presentation(m,'Switch on the warm lantern light','HOVER TO LIGHT UP · DRAG TO EXPLORE')
    m.alpha['glass']=.045
    m.palette['paper']=('#f0e4cb',.46,0)
    bind([p for p in m.parts if p['mat']=='paper'],'Illuminated lantern diffuser',glow=[3.8,1.65,.35])
    m.description='An assembled camp lantern whose central diffuser lights warmly; its chimney, cage, cap and handle stay attached.'

def cap(m):
    presentation(m,'A complete sewn cap, gently turned as one object','HOVER TO TURN · DRAG TO EXPLORE',view=[.42,.46,1])
    m.palette['secondary']=('#bcc8e9',.92,0);m.palette['accent']=('#a4b3dd',.90,0)
    action(m,'Complete sewn cap',(0,.12,0),(0,1,0),-.17);m.group.update(blast=[0,.20,0],blastGroup='Sewn crown')
    profile=[(.515,.065),(.545,.13),(.52,.29),(.43,.48),(.26,.63),(0,.69),(0,.671),(.25,.612),(.41,.465),(.50,.28),(.525,.13),(.495,.07),(.515,.065)]
    lathe(m,profile,mat='secondary',label='continuous-open-six-panel-cloth-crown',seg=144,steps=8)
    m.group.update(blast=[0,-.12,0],blastGroup='Sweatband')
    ring(m,(0,.077,0),.515,.488,.05,'fabric',label='attached-inner-sweatband')
    m.group.update(blast=[0,.20,0],blastGroup='Sewn crown')
    seam_profile=smooth_profile(profile,8)[:41]
    for i in range(6):
        a=i*pi/3;points=[]
        for r,y in seam_profile:points.append([(r+.002)*cos(a),y+.0005,(r+.002)*sin(a)])
        m.tube(points,.0027,'body')
    m.group.update(blast=[0,.47,0],blastGroup='Top button')
    m.ball((0,.696,0),.029,'accent',scale=(1,.45,1),seg=48,rings=24)
    # The rear edge follows the crown's front arc; a real thickness closes the bill.
    pts=[];ids=[];nu=72;nv=24
    def point(u,t,face=0):
        rear=sqrt(max(0,.515**2-(.505*u)**2))-.008;edge=min(1,max(0,(1-abs(u))/.14));blend=edge*edge*(3-2*edge)
        x=(.505+.055*t*blend)*u;z=rear+.43*t*max(0,1-u*u)**.6*blend
        return [x,.078-(.030*u*u+.038)*t*blend+face*.007,z]
    for face in (-1,1):
        for j in range(nv+1):
            for i in range(nu+1):pts.append(point(-1+2*i/nu,j/nv,face))
    count=(nv+1)*(nu+1)
    for side in range(2):
        for j in range(nv):
            for i in range(nu):a=side*count+j*(nu+1)+i;b=a+nu+1;ids.extend([a,b,a+1,a+1,b,b+1] if side==1 else [a,a+1,b,a+1,b+1,b])
    for j in (0,nv):
        for i in range(nu):a=j*(nu+1)+i;b=a+count;ids.extend([a,b,a+1,a+1,b,b+1])
    for i in (0,nu):
        for j in range(nv):a=j*(nu+1)+i;b=a+count;c=a+nu+1;ids.extend([a,c,b,c,b+nu+1,b])
    m.group.update(blast=[0,-.03,.28],blastGroup='Curved bill and stitching')
    add_mesh(m,pts,ids,'accent','attached-curved-bill-with-solid-edge')
    for t in (.84,.94):m.tube([point(-1+2*i/nu,t,1.2) for i in range(nu+1)],.0025,'body')
    m.description='A complete soft six-panel cap with an attached curved stitched bill, open sweatband and fixed top button.'

def rocket(m):
    from craft_play import build
    build(m);freeze(m)
    presentation(m,'A small liftoff with a warm engine flame','HOVER TO LIFT OFF · DRAG TO EXPLORE',view=[.38,.25,1],frame=.08)
    # The original window sat behind the hull. Seat the optical assembly outside it.
    for p in m.parts:
        if p['layer'] in ('Porthole assembly','Porthole fasteners'):p['p']=[[v[0],v[1],v[2]+.06] for v in p['p']]
    still(m,'Inset dark porthole');front(m,(0,.98,.335),.099,.012,'lens')
    bind(m.parts,'Complete lifting rocket',translate=[0,.30,0],wave={'axis':[0,1,0],'amplitude':.010,'lift':0,'frequency':1.0,'phase':0})
    m.palette.update(flame=('#ee7d2f',.35,0),flamecore=('#ffdfa2',.30,0))
    for name,mat,r,h in [('Engine flame','flame',.009,.017),('Flame core','flamecore',.0045,.012)]:
        action(m,name,(0,.125,0),translate=[0,.30,0],scaleFrom=[.001,.001,.001],scaleTo=[10,17,10],activation=[.03,.55],glow=[2.0,.45,.04] if mat=='flame' else [2.5,1.5,.4],wave={'axis':[0,1,0],'amplitude':.010,'lift':0,'frequency':1.0,'phase':0})
        lathe(m,[(0,-h),(r*.6,-h*.70),(r,-h*.25),(r*.7,0),(0,0)],(0,.125,0),mat,label='small-tapered-engine-plume',seg=64)
    m.description='A complete toy rocket that lifts a little with its fins and porthole attached and a small warm flame beneath the engine.'

BUILDERS={'ribbon-gift':gift,'delivery-parcel':parcel,'shopping-tote':tote,'receipt-printer':printer,'camp-lantern':lantern,'sun-cap':cap,'little-rocket':rocket}
