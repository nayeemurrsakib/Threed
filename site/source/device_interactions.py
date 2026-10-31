"""Fitted device faces and actions performed by their controls."""
from purposeful_motion import *

def headphones(m):
    presentation(m,'The attached earcups swivel to fit','HOVER TO SWIVEL · DRAG TO EXPLORE',view=[.44,.25,1])
    m.description='Over-ear headphones with a directly attached padded headband, soft oval cushions and swiveling cups; no exposed decorative forks.'
    still(m,'Connected padded headband')
    m.tube([(.65*cos(pi*i/80),.71+.76*sin(pi*i/80),0) for i in range(81)],.042,'ink')
    m.tube([(.61*cos(.10+(pi-.20)*i/80),.71+.71*sin(.10+(pi-.20)*i/80),0) for i in range(81)],.060,'leather')
    for sign in (-1,1):
        action(m,('Left' if sign<0 else 'Right')+' connected swiveling cup',(sign*.65,.53,0),(0,1,0),sign*.22)
        m.ball((sign*.64,.48,0),.30,'body',scale=(.46,1.16,.85),seg=96,rings=48,label='smooth-oval-earcup-housing')
        m.ball((sign*.772,.48,0),.215,'accent',scale=(.12,1.18,.85),seg=80,rings=40,label='fitted-oval-outer-earcup-inlay')
        before=len(m.parts)
        ring(m,(sign*.505,.48,0),.26,.164,.11,'rubber',(0,0,pi/2),label='open-annular-ear-cushion');m.cyl((sign*.51,.48,0),.163,.018,'fabric',(0,0,pi/2),label='recessed-acoustic-cloth')
        for p in m.parts[before:]:
            p['p']=[[v[0],.48+(v[1]-.48)*1.18,v[2]*.85] for v in p['p']]
            for i,n in enumerate(p['n']):
                a=[n[0],n[1]/1.18,n[2]/.85];l=sqrt(sum(v*v for v in a));p['n'][i]=[v/l for v in a]

def controller(m):
    presentation(m,'Move the sticks and press the controls','HOVER TO PLAY · DRAG TO EXPLORE',view=[.43,.38,1])
    m.description='A continuous sculpted gamepad shell with seated buttons, tilting analog sticks and pressing triggers.'
    lobes=[((-.45,.41,0),(.35,.47,.28)),((.45,.41,0),(.35,.47,.28)),((0,.63,0),(.60,.27,.25))]
    still(m,'Continuous controller shell');organic(m,lobes,'body','seamless-ergonomic-controller-shell',144,80)
    def surface(x,y):
        lo,hi=0,.5
        for _ in range(28):
            z=(lo+hi)/2;f=sum(math.exp(-2*(((x-c[0])/r[0])**2+((y-c[1])/r[1])**2+((z-c[2])/r[2])**2)) for c,r in lobes)
            if f>.28:lo=z
            else:hi=z
        return (lo+hi)/2
    for i,(x,y) in enumerate([(-.25,.43),(.24,.43)]):
        z=surface(x,y);still(m,f'Analog socket {i+1}')
        # A flexible socket skirt follows the sculpted grip rather than slicing
        # a flat disk through it. Its outer edge remains seated on the shell.
        pts=[];indices=[];segments=96
        for radius,height in [(0,.010),(.05,.012),(.095,.016),(.115,.004)]:
            for j in range(segments+1):
                a=2*pi*j/segments;px=x+radius*cos(a);py=y+radius*sin(a)
                pts.append([px,py,surface(px,py)+height])
        for row in range(3):
            for j in range(segments):a=row*(segments+1)+j;b=a+segments+1;indices.extend([a,a+1,b,a+1,b+1,b])
        add_mesh(m,pts,indices,'ink','conforming-analog-socket-skirt')
        action(m,f'Tilting stick {i+1}',(x,y,z+.015),(.8,.6,0),-.19 if i==0 else .17,oscillate=.65,phase=i*.8)
        front(m,(x,y,z+.040),.047,.068,'ink');front(m,(x,y,z+.078),.078,.035,'rubber');m.torus((x,y,z+.099),.058,.006,'rubber',(pi/2,0,0))
    still(m,'Seated direction pad');x,y=-.46,.66;z=surface(x,y)
    m.box((x,y,z+.023),(.20,.062,.045),'ink',.021);m.box((x,y,z+.023),(.062,.20,.045),'ink',.021)
    for i,(dx,dy) in enumerate([(0,.073),(.073,0),(0,-.073),(-.073,0)]):
        x,y=.46+dx,.66+dy;z=surface(x,y)
        action(m,f'Pressing action button {i+1}',wave={'axis':[0,0,1],'amplitude':.006,'lift':-.008,'frequency':.7,'phase':i*.7})
        front(m,(x,y,z+.018),.032,.043,'accent')
    for i,x in enumerate((-.40,.40)):
        action(m,f'Pressing shoulder trigger {i+1}',wave={'axis':[0,1,0],'amplitude':.005,'lift':-.008,'frequency':.7,'phase':i*1.2})
        m.box((x,.839,-.015),(.22,.06,.15),'rubber',.028)
    still(m,'Status light');m.box((0,.694,surface(0,.694)+.005),(.12,.014,.01),'secondary',.005)

def radio(m):
    presentation(m,'Turn the tuner and extend the antenna','HOVER TO TUNE · DRAG TO EXPLORE',view=[.38,.25,1],frame=.015)
    m.description='A rounded radio with a matching-radius fitted front, perforated speaker, rotating tuning dial and telescoping antenna.'
    still(m,'Fitted rounded enclosure');tray(m,(0,.57,-.06),(1.66,1.04,.46),'secondary',.19)
    panel(m,(0,.57,.166),(1.642,1.022,.105),'secondary',.185,label='matching-radius-rounded-radio-front')
    still(m,'Fitted speaker grille');panel(m,(-.30,.56,.234),(.88,.75,.028),'body',.077,label='rounded-speaker-grille-surround')
    panel(m,(-.30,.56,.254),(.78,.65,.012),'ink',.035)
    m.grille((-.65,.268,.266),12,10,.064,.016,'body')
    still(m,'Inset tuner display');panel(m,(.48,.86,.227),(.43,.113,.024),'ink',.028);panel(m,(.48,.86,.244),(.37,.071,.012),'lens',.018)
    for i in range(9):m.box((.33+i*.037,.86,.254),(.003,.023 if i%2 else .04,.003),'paper',.001)
    action(m,'Sliding tuner needle',translate=[.12,0,0]);m.box((.40,.86,.258),(.005,.054,.003),'accent',.001)
    still(m,'Fixed dial collar');ring(m,(.49,.43,.253),.173,.136,.033,'metal',(pi/2,0,0))
    action(m,'Turning tuning dial',(.49,.43,.280),angle=-1.2);front(m,(.49,.43,.278),.14,.038,'body');m.box((.49,.483,.300),(.008,.070,.004),'ink',.002)
    still(m,'Attached carrying handle and antenna socket');cable(m,[(-.49,1.08,-.1),(-.40,1.27,-.1),(.40,1.27,-.1),(.49,1.08,-.1)],.025,'leather')
    m.cyl((-.58,1.11,-.14),.035,.09,'metal');m.rod((-.58,1.15,-.14),(-.05,1.63,-.14),.011,'metal')
    action(m,'Extending antenna',translate=[.08,.072,0]);m.rod((-.25,1.45,-.14),(.16,1.82,-.14),.006,'metal');m.ball((.16,1.82,-.14),.011,'metal')
    still(m,'Attached rubber feet');feet(m,(-.52,.52),(-.13,.13),.035)

def webcam(m):
    presentation(m,'The webcam tilts to frame the view','HOVER TO AIM · DRAG TO EXPLORE',view=[.42,.26,1])
    m.description='A capsule webcam with a fitted dark optical front and an attached pivoting head on a monitor clip.'
    still(m,'Monitor clip and hinge');m.box((0,.055,0),(.65,.10,.43),'ink',.045);m.box((0,.20,-.10),(.13,.28,.10),'metal',.045);front(m,(0,.37,-.03),.07,.22,'metal')
    action(m,'Attached aiming camera head',(0,.39,0),(0,1,0),-.22)
    m.box((0,.58,0),(1.16,.48,.36),'body',.225,label='soft-capsule-webcam-housing')
    panel(m,(0,.58,.189),(1.085,.410,.045),'lens',.20,label='fitted-dark-optical-front-window')
    ring(m,(0,.58,.227),.165,.11,.042,'metal',(pi/2,0,0));front(m,(0,.58,.244),.114,.025,'lens')
    m.ball((0,.58,.260),.108,'glass',scale=(1,1,.10),seg=96,rings=32,label='inset-curved-webcam-lens')
    front(m,(-.40,.58,.218),.012,.006,'accent')

BUILDERS={'over-ear-headphones':headphones,'game-controller':controller,'portable-radio':radio,'web-camera':webcam}
