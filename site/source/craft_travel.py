"""Travel collection: fitted shells, optical barrels and sewn curved forms."""
from quality_geometry import *

def build(m):
    s=m.slug
    if s=='cabin-suitcase':
        group(m,'Rear suitcase shell',[0,0,-.23]);tray(m,(0,.81,-.13),(.97,1.29,.30),'secondary',.18,.035)
        group(m,'Front suitcase shell',[0,0,.34],.05);tray(m,(0,.81,.15),(.97,1.29,.30),'secondary',.18,.035,flip=True)
        for x in (-.30,-.10,.10,.30):m.box((x,.81,.309),(.028,.93,.025),'body',.012)
        group(m,'Zipper welt',[0,.05,.05],.025)
        edge=outline(.99,1.31,.19,16);m.tube([(x,y+.81,.005) for x,y in edge],.012,'rubber')
        for y in (.64,.74):m.box((.49,y,.035),(.022,.065,.04),'metal',.01)
        group(m,'Telescoping handle',[0,.39,-.06],.10)
        for x in (-.25,.25):m.rod((x,1.37,-.13),(x,1.85,-.13),.018,'metal');m.cyl((x,1.44,-.13),.026,.14,'ink')
        m.box((0,1.87,-.13),(.58,.08,.115),'rubber',.038)
        group(m,'Spinner wheels',[0,-.18,0],.035)
        for x in (-.34,.34):
            for z in (-.16,.16):m.cyl((x,.10,z),.08,.075,'rubber',(0,0,pi/2));m.cyl((x,.10,z),.039,.085,'metal',(0,0,pi/2))
    elif s=='weekend-backpack':
        m.palette['secondary']=('#bcc8e9',.86,0);m.palette['accent']=('#a4b3dd',.78,0)
        group(m,'Sewn main body',[0,-.07,-.05]);m.box((0,.76,0),(1.02,1.41,.58),'secondary',.25,label='soft-continuous-backpack-body')
        group(m,'Front pocket',[0,.04,.34],.055);m.box((0,.48,.34),(.80,.55,.22),'accent',.13)
        cable(m,[(-.32,.66,.45),(0,.70,.465),(.32,.66,.45)],.009,'metal');m.box((.29,.65,.47),(.022,.08,.018),'metal',.007)
        group(m,'Curved upper panel',[0,.35,.13],.10)
        # A separate fabric crown panel follows the curved main volume.
        shape_loft(m,[(-.45,-.17),(-.46,.17),(-.31,.38),(0,.43),(.31,.38),(.46,.17),(.45,-.17)],.035,(0,1.01,.283),'secondary','rounded-sewn-crown-panel')
        seams(m,[(-.43,.91,.31),(-.43,1.24,.25),(-.27,1.42,.19),(0,1.45,.15),(.27,1.42,.19),(.43,1.24,.25),(.43,.91,.31)],.005,'body')
        group(m,'Shoulder straps',[0,.10,-.29],.075)
        for x in (-.29,.29):
            cable(m,[(x,1.25,-.25),(x,1.06,-.48),(x,.54,-.51),(x,.23,-.27)],.043,'fabric')
            m.box((x,.34,-.37),(.12,.075,.035),'ink',.022)
        group(m,'Carry handle',[0,.55,-.03],.145);cable(m,[(-.16,1.40,0),(-.13,1.58,0),(.13,1.58,0),(.16,1.40,0)],.025,'rubber')
    elif s=='binoculars':
        group(m,'Bridge and focus',[0,.24,-.03],.06);m.box((0,.46,0),(.36,.20,.35),'body',.07);m.knurl((0,.60,0),.10,.12,'metal',48)
        for i,x in enumerate((-.34,.34)):
            group(m,('Left' if i==0 else 'Right')+' optical barrel',[x*.54,0,-.13],.025)
            lathe(m,[(.14,-.47),(.20,-.39),(.25,-.21),(.28,.25),(.28,.43),(.25,.47),(.22,.47),(.22,.39),(.23,.23),(.20,-.20),(.13,-.39),(.14,-.47)],(x,.42,0),'secondary',(pi/2,0,0),'continuous-hollow-optical-barrel')
            ring(m,(x,.42,-.44),.17,.11,.09,'rubber',(pi/2,0,0))
            optical(m,(x,.42,.47),.245,(x*.54,0,.43),('Left' if i==0 else 'Right')+' objective optics')
            group(m,('Left' if i==0 else 'Right')+' eyepiece',[x*.54,.03,-.39],.11);front(m,(x,.42,-.51),.115,.02,'lens')
    elif s=='pocket-compass':
        group(m,'Machined compass case',[0,-.12,0]);lathe(m,[(0,.03),(.43,.03),(.53,.07),(.56,.14),(.55,.24),(.51,.28),(.48,.28),(.48,.10),(0,.10)],mat='metal',seg=144)
        group(m,'Dial plate',[0,.16,0],.045);m.cyl((0,.23,0),.477,.02,'paper');marks(m,(0,.243,0),.415,48,'y')
        group(m,'Floating compass needle',[0,.32,0],.085)
        for sign,mat in [(1,'accent'),(-1,'ink')]:shape_loft(m,[(-.035,0),(0,sign*.33),(.035,0)],.012,(0,0,0),mat,'tapered-magnetic-needle')
        # Needle silhouette is authored in XY then placed flat in the compass.
        for p in m.parts[-2:]:
            p['p']=[[v[0],.273+v[2],v[1]] for v in p['p']];p['n']=[[v[0],v[2],v[1]] for v in p['n']]
        m.cyl((0,.289,0),.025,.026,'metal')
        group(m,'Crystal and bezel',[0,.51,0],.13);ring(m,(0,.27,0),.54,.478,.035,'metal');m.ball((0,.284,0),.478,'glass',scale=(1,.035,1),seg=112,rings=32)
        group(m,'Carrying loop',[0,.12,-.20],.065);m.torus((0,.16,-.66),.105,.022,'metal');m.box((0,.16,-.54),(.12,.07,.07),'metal',.025)
        m.presentation['viewDirection']=[.35,.9,1]
    elif s=='camp-lantern':
        group(m,'Lower lantern base',[0,-.15,0]);lathe(m,[(0,.03),(.29,.03),(.39,.08),(.39,.15),(.34,.22),(0,.22)],mat='secondary')
        front(m,(0,.14,.365),.045,.04,'metal')
        group(m,'Light engine',[0,.13,0],.04);m.cyl((0,.57,0),.17,.66,'paper');ring(m,(0,.27,0),.24,.15,.05,'metal')
        group(m,'Glass chimney',[0,.34,0],.085);lathe(m,[(.23,.23),(.26,.27),(.26,.86),(.23,.94),(.21,.94),(.24,.85),(.24,.29),(.21,.24),(.23,.23)],mat='glass',seg=128)
        group(m,'Protective metal cage',[.16,.12,0],.065)
        for i in range(4):
            a=pi/4+pi/2*i;m.rod((.31*cos(a),.18,.31*sin(a)),(.31*cos(a),.98,.31*sin(a)),.018,'metal')
        group(m,'Ventilated cap',[0,.55,0],.13);lathe(m,[(0,.94),(.32,.94),(.39,1.00),(.37,1.08),(.27,1.13),(.19,1.15),(0,1.15)],mat='secondary')
        for i in range(12):
            a=i*pi/6;m.box((.29*cos(a),1.08,.29*sin(a)),(.06,.018,.008),'ink',.006,rot=(0,-a,0))
        group(m,'Carry handle',[0,.76,0],.17);cable(m,[(-.32,1.04,0),(-.28,1.40,0),(-.13,1.50,0),(.13,1.50,0),(.28,1.40,0),(.32,1.04,0)],.023,'rubber')
    elif s=='travel-mug':
        group(m,'Double-wall cup',[0,-.10,0]);lathe(m,[(0,.035),(.25,.035),(.29,.07),(.35,.88),(.35,.98),(.33,1.00),(.30,.98),(.30,.89),(.25,.13),(0,.10)],mat='secondary',seg=128)
        cable(m,[(.33,.80,0),(.55,.82,0),(.62,.66,0),(.54,.39,0),(.30,.34,0)],.043,'secondary')
        group(m,'Lid gasket',[0,.15,0],.04);ring(m,(0,.98,0),.35,.30,.045,'rubber')
        group(m,'Sealed lid',[0,.39,0],.09);m.cyl((0,1.035,0),.37,.09,'ink');m.torus((0,1.08,0),.32,.015,'rubber')
        group(m,'Drinking slide',[0,.60,.07],.14);m.box((0,1.092,.13),(.16,.018,.25),'accent',.055);m.box((0,1.085,.25),(.12,.009,.06),'rubber',.025)
    elif s=='passport-wallet':
        group(m,'Leather back cover',[0,-.10,0]);m.box((0,.035,0),(.94,.045,1.38),'leather',.045)
        group(m,'Document pages',[0,.12,0],.045);m.box((.015,.13,0),(.85,.14,1.29),'paper',.035)
        for y in (.08,.105,.13,.155,.18):m.box((.44,y,0),(.006,.002,1.18),'body',.0005)
        group(m,'Leather front cover',[0,.34,0],.095);m.box((0,.235,0),(.94,.05,1.38),'leather',.045)
        for x in (-.40,.40):seams(m,[(x,.263,-.60),(x,.263,.60)],.003,'body')
        for z in (-.60,.60):seams(m,[(-.40,.263,z),(.40,.263,z)],.003,'body')
        group(m,'Embossed travel emblem',[0,.49,0],.14);ring(m,(0,.267,-.12),.19,.177,.004,'metal');m.torus((0,.270,-.12),.13,.004,'metal');m.rod((-.18,.27,-.12),(.18,.27,-.12),.004,'metal');m.box((0,.269,.31),(.34,.006,.025),'metal',.007)
        group(m,'Bound spine',[-.18,.02,0],.02);m.box((-.44,.135,0),(.075,.24,1.39),'leather',.035)
    elif s=='folding-sunglasses':
        group(m,'Front acetate frame',[0,0,.07]);
        for x in (-.38,.38):ring(m,(x,.40,0),.30,.245,.07,'accent',(pi/2,0,0))
        cable(m,[(-.10,.46,0),(0,.51,0),(.10,.46,0)],.025,'accent')
        group(m,'Tinted optical lenses',[0,.025,.38],.07)
        for x in (-.38,.38):m.ball((x,.40,.015),.246,'lens',scale=(1,1,.07),seg=112,rings=32)
        for i,sign in enumerate((-1,1)):
            group(m,('Left' if i==0 else 'Right')+' folding temple',[sign*.24,.05,-.18],.11)
            cable(m,[(sign*.67,.44,0),(sign*.70,.44,-.14),(sign*.70,.44,-.56),(sign*.64,.35,-.73)],.023,'accent');m.box((sign*.66,.44,-.035),(.07,.05,.085),'metal',.014)
    elif s=='sun-cap':
        m.palette['secondary']=('#bcc8e9',.86,0);m.palette['accent']=('#a4b3dd',.86,0)
        group(m,'Six-panel sewn crown',[0,.13,-.04],.04)
        # Continuous hemispherical cloth shell, open at the sweatband.
        profile=[(.55*cos(pi/2*i/48),.08+.64*sin(pi/2*i/48)) for i in range(49)]
        profile +=[(.525*sin(pi/2*i/48),.08+.61*cos(pi/2*i/48)) for i in range(49)]
        m.lathe(profile,mat='secondary',seg=144,label='double-surface-smooth-cap-crown')
        for i in range(6):
            a=i*pi/3;points=[(.554*cos(t)*cos(a),.08+.644*sin(t),.554*cos(t)*sin(a)) for t in [j*pi/2/40 for j in range(41)]];m.tube(points,.0035,'body')
        group(m,'Sweatband',[0,-.13,0]);ring(m,(0,.08,0),.552,.515,.07,'fabric')
        group(m,'Curved sewn bill',[0,.03,.31],.085)
        pts=[];idx=[];rows=20;N=64
        for j in range(rows+1):
            t=j/rows
            for i in range(N+1):
                u=-1+2*i/N;x=.59*u*(.82+.18*t);z=.25+.70*t*sqrt(max(0,1-u*u));y=.055-.055*u*u+.025*t
                pts.append([x,y,z])
        for j in range(rows):
            for i in range(N):a=j*(N+1)+i;b=a+N+1;idx.extend([a,b,a+1,a+1,b,b+1])
        add_mesh(m,pts,idx,'accent','continuous-curved-cap-bill',rows+1,N+1)
        for t in (.84,.94):m.tube([(.59*u*(.82+.18*t),.061-.055*u*u+.025*t,.25+.70*t*sqrt(max(0,1-u*u))) for u in [-1+2*i/64 for i in range(65)]],.003,'body')
        group(m,'Top button',[0,.43,0],.13);m.ball((0,.73,0),.035,'accent',scale=(1,.5,1))
        m.presentation['viewDirection']=[.40,.45,1]
    elif s=='key-fob':
        group(m,'Leather fob',[-.15,0,.05]);m.box((-.23,.38,0),(.50,.70,.11),'leather',.20)
        for x in (-.41,-.05):seams(m,[(x,.15,.059),(x,.60,.059)],.003,'body')
        group(m,'Brass eyelet',[-.15,.13,.08],.035);ring(m,(-.23,.64,.065),.055,.030,.015,'metal',(pi/2,0,0))
        group(m,'Split keyring',[.12,.26,0],.085)
        for z in (-.012,.012):m.torus((.02,.72,z),.20,.016,'metal',(pi/2,0,0),arc=pi*1.94)
        group(m,'House key',[.32,-.06,.10],.12);ring(m,(.27,.66,.02),.14,.075,.045,'metal',(pi/2,0,0));m.box((.27,.37,.02),(.08,.39,.045),'metal',.015)
        for x,y in [(.325,.22),(.325,.29),(.325,.35)]:m.box((x,y,.02),(.08,.045,.045),'metal',.009)
    else:raise KeyError(s)
