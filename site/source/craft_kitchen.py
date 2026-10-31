"""Kitchen objects: continuous profiles, hollow vessels and fitted hardware."""
from quality_geometry import *

def build(m):
    s=m.slug
    if s=='pour-over-kettle':
        group(m,'Hollow enamel kettle',[0,-.08,0]);lathe(m,[(0,.03),(.34,.03),(.45,.08),(.51,.25),(.51,.47),(.45,.70),(.31,.84),(.27,.86),(.245,.84),(.29,.80),(.41,.67),(.47,.46),(.47,.26),(.41,.13),(.30,.09),(0,.09)],mat='secondary',label='double-wall-rounded-kettle',seg=128,steps=7)
        m.cyl((0,.035,0),.33,.03,'metal')
        group(m,'Gooseneck spout',[.30,.03,.07],.04)
        points=curve([(.43,.24,0),(.65,.28,0),(.72,.50,0),(.80,.80,0),(.96,.94,0),(1.08,.95,0)],10)
        m.tube(points,.044,'metal');m.tube(points,.032,'ink')
        ring(m,(1.075,.946,0),.044,.031,.014,'metal',(0,0,pi/2))
        group(m,'Arched handle',[-.13,.28,-.07],.07);cable(m,[(-.43,.57,-.08),(-.48,1.04,-.08),(-.25,1.27,-.08),(.25,1.27,-.08),(.43,.64,-.08)],.042,'rubber')
        group(m,'Fitted lid',[0,.51,0],.12);lathe(m,[(0,.86),(.24,.86),(.30,.88),(.31,.92),(.27,.94),(.15,.95),(0,.95)],mat='body')
        group(m,'Lid knob',[0,.68,0],.17);m.cyl((0,.985,0),.045,.08,'metal');m.ball((0,1.035,0),.066,'ink',scale=(1,.7,1))
    elif s=='stovetop-brewer':
        group(m,'Lower pressure chamber',[0,-.15,0]);lathe(m,[(0,.03),(.34,.03),(.41,.08),(.41,.18),(.30,.59),(.28,.63),(.245,.63),(.245,.57),(.35,.14),(.32,.09),(0,.09)],mat='metal',seg=64,steps=4)
        group(m,'Filter basket',[0,.17,0],.04);bowl(m,(0,.49,0),.24,.18,'metal',.018)
        for i in range(8):
            a=2*pi*i/8;front(m,(.13*cos(a),.62,.13*sin(a)),.009,.01,'ink')
        group(m,'Upper collecting chamber',[0,.39,0],.085)
        lathe(m,[(.26,.64),(.29,.68),(.43,.76),(.43,1.16),(.37,1.27),(.34,1.28),(.31,1.25),(.39,1.14),(.39,.80),(.26,.72),(.26,.64)],mat='metal',seg=96,steps=4)
        cable(m,[(.39,1.17,0),(.63,1.16,0),(.70,.99,0),(.57,.78,0),(.42,.79,0)],.058,'rubber')
        lathe(m,[(.05,-.13),(.10,-.10),(.12,.08),(.095,.13),(.06,.13),(.07,.06),(.05,-.13)],(-.42,1.16,0),'metal',(0,0,-.65),'hollow-pouring-spout',80)
        group(m,'Hinged lid',[0,.62,0],.13);lathe(m,[(0,1.26),(.34,1.26),(.42,1.28),(.40,1.32),(.12,1.34),(0,1.34)],mat='secondary');m.ball((0,1.40,0),.07,'rubber',scale=(1,.75,1))
        group(m,'Safety valve',[.19,-.04,.12],.03);front(m,(.17,.29,.34),.045,.05,'metal')
    elif s=='two-slot-toaster':
        group(m,'Enamel outer casing',[0,.04,-.09]);tray(m,(0,.52,0),(1.48,.88,.79),'body',.23,wall=.045,axis='y')
        group(m,'Heating carriage',[0,.27,0],.05)
        for z in (-.18,.18):
            tray(m,(0,.69,z),(1.11,.44,.16),'metal',.035,.015,axis='y')
            for i in range(9):m.box((-.44+i*.11,.73,z+.078),(.008,.24,.008),'ink',.003)
        group(m,'Top slot surrounds',[0,.48,0],.10)
        # Four rails per slot leave actual apertures and expose the carriages below.
        for z in (-.18,.18):
            for dz in (-.085,.085):m.box((0,.963,z+dz),(1.14,.035,.035),'metal',.016)
            for x in (-.55,.55):m.box((x,.963,z),(.045,.035,.19),'metal',.02)
        group(m,'Control dial and lever',[.21,.12,.15],.075)
        ring(m,(.36,.39,.407),.12,.09,.035,'metal',(pi/2,0,0));front(m,(.36,.39,.43),.09,.03,'accent');m.box((.36,.43,.448),(.008,.045,.004),'ink',.002)
        m.rod((.77,.34,0),(.77,.78,0),.018,'metal');m.box((.84,.71,0),(.19,.065,.13),'accent',.028)
        group(m,'Crumb tray and feet',[0,-.22,0],.025);m.box((0,.075,0),(1.31,.055,.64),'secondary',.027);feet(m,(-.5,.5),(-.23,.23),.028)
    elif s=='lidded-pot':
        group(m,'Hollow enamel body',[0,-.10,0]);bowl(m,(0,.045,0),.63,.62,'body',.045);m.cyl((0,.042,0),.43,.035,'metal')
        group(m,'Side handles',[.20,.03,0],.04)
        for sign in (-1,1):
            cable(m,[(sign*.55,.52,0),(sign*.82,.53,0),(sign*.89,.44,0),(sign*.82,.34,0),(sign*.55,.35,0)],.036,'secondary')
            for y in (.36,.51):m.ball((sign*.56,y,0),.044,'metal',scale=(.4,1,1))
        group(m,'Rolled rim',[0,.10,0],.03);m.torus((0,.66,0),.607,.013,'metal')
        group(m,'Domed lid',[0,.49,0],.095)
        lathe(m,[(.64,.665),(.65,.69),(.61,.72),(.48,.80),(.25,.86),(0,.87),(0,.839),(.25,.829),(.46,.77),(.59,.70),(.62,.673),(.64,.665)],mat='accent',label='double-walled-domed-pot-lid',seg=128,steps=7)
        group(m,'Lid knob',[0,.68,0],.15);m.cyl((0,.91,0),.04,.08,'metal');m.ball((0,.96,0),.075,'metal',scale=(1,.65,1))
    elif s=='countertop-blender':
        group(m,'Rounded motor enclosure',[0,-.09,0]);m.box((0,.25,0),(.87,.45,.74),'accent',.13,label='closed-rounded-blender-motor-base');feet(m,(-.28,.28),(-.21,.21),.035)
        front(m,(0,.27,.38),.115,.045,'metal');front(m,(0,.27,.409),.087,.035,'body');m.box((0,.31,.43),(.008,.05,.004),'ink',.002)
        group(m,'Motor enclosure top',[0,0,0]);
        from purposeful_motion import panel
        panel(m,(0,.474,0),(.83,.035,.70),'accent',.12,'y','fitted-blender-base-top')
        group(m,'Drive collar',[0,.17,0],.04);m.cyl((0,.51,0),.25,.10,'rubber');m.cyl((0,.57,0),.13,.06,'metal')
        group(m,'Glass jar',[0,.40,0],.09);lathe(m,[(0,.59),(.25,.59),(.29,.65),(.39,1.33),(.39,1.42),(.37,1.44),(.345,1.42),(.345,1.34),(.25,.69),(.21,.65),(0,.65)],mat='glass',label='double-walled-blender-pitcher',seg=128,steps=6)
        cable(m,[(.37,1.30,0),(.60,1.29,0),(.64,1.02,0),(.55,.83,0),(.30,.82,0)],.042,'body')
        for y in (.83,.97,1.11,1.25):m.box((-.10,y,.36),(.10,.008,.008),'body',.002)
        group(m,'Blade assembly',[0,.28,.20],.065);m.cyl((0,.70,0),.05,.10,'metal')
        for a in (0,pi/2):m.box((0,.70,0),(.43,.018,.07),'metal',.016,rot=(0,a,.12))
        group(m,'Sealed lid',[0,.64,0],.14);m.cyl((0,1.47,0),.405,.09,'rubber');m.cyl((0,1.53,0),.12,.05,'body')
    elif s=='espresso-cup':
        group(m,'Glazed saucer',[0,-.14,0]);lathe(m,[(0,.025),(.39,.025),(.59,.045),(.65,.085),(.63,.11),(.56,.10),(.31,.07),(0,.07)],mat='secondary',seg=128)
        group(m,'Hollow porcelain cup',[0,.18,0],.045);bowl(m,(0,.075,0),.35,.51,'body',.038);m.torus((.35,.39,0),.16,.043,'body',(pi/2,0,0));m.cyl((0,.095,0),.23,.025,'body')
        group(m,'Coffee and crema',[0,.34,0],.085);m.cyl((0,.51,0),.302,.01,'coffee');m.torus((0,.515,0),.278,.009,'sand')
        group(m,'Spoon',[.24,.06,.16],.05);m.ball((.47,.14,.17),.085,'metal',scale=(.62,.14,1));m.rod((.47,.14,.12),(.48,.14,-.39),.012,'metal')
    elif s=='insulated-bottle':
        group(m,'Vacuum bottle',[0,-.10,0]);lathe(m,[(0,.03),(.25,.03),(.31,.08),(.32,.24),(.32,1.05),(.28,1.18),(.22,1.23),(.22,1.30),(.19,1.30),(.19,1.22),(.25,1.15),(.28,1.03),(.28,.12),(0,.09)],mat='secondary',seg=128)
        group(m,'Silicone boot',[0,-.25,0],.025);ring(m,(0,.10,0),.326,.29,.14,'rubber')
        group(m,'Threaded neck',[0,.13,0],.04)
        for y in (1.245,1.265,1.285):m.torus((0,y,0),.218,.007,'metal')
        group(m,'Screw lid',[0,.47,0],.10);lathe(m,[(.18,1.30),(.18,1.41),(.25,1.41),(.26,1.38),(.26,1.29),(.24,1.27),(.22,1.28),(.22,1.36),(.18,1.36),(.18,1.30)],mat='accent');m.cyl((0,1.42,0),.22,.03,'accent')
        group(m,'Carrying loop',[0,.65,0],.15);m.torus((0,1.50,0),.11,.025,'metal',(pi/2,0,0),arc=pi)
    elif s=='citrus-press':
        group(m,'Catch bowl',[0,-.12,0]);bowl(m,(0,.035,0),.58,.31,'secondary',.04)
        group(m,'Strainer plate',[0,.23,0],.055);ring(m,(0,.36,0),.54,.18,.028,'body')
        for i in range(28):
            a=2*pi*i/28;m.box((.37*cos(a),.379,.37*sin(a)),(.018,.004,.12),'ink',.007,rot=(0,-a+pi/2,0))
        group(m,'Fluted reamer',[0,.47,0],.11)
        # Smooth ribs are in the surface, rather than rods crossing a cone.
        pts=[];idx=[];N=128;rows=40
        for j in range(rows+1):
            t=j/rows;y=.37+.45*t;rad=.23*(1-t*t)**.65
            for i in range(N+1):
                a=2*pi*i/N;r=rad*(1+.075*cos(12*a));pts.append([r*cos(a),y,r*sin(a)])
        for j in range(rows):
            for i in range(N):a=j*(N+1)+i;b=a+N+1;idx.extend([a,a+1,b,a+1,b+1,b])
        add_mesh(m,pts,idx,'accent','continuous-twelve-flute-reamer',rows+1,N+1)
    elif s=='kitchen-scale':
        group(m,'Weighted pedestal',[0,-.13,0]);m.box((0,.12,0),(.88,.17,.75),'secondary',.082);feet(m,(-.30,.30),(-.23,.23),.035)
        group(m,'Mechanical casing',[0,.05,-.16],.035);tray(m,(0,.49,-.02),(.69,.66,.53),'body',.19)
        group(m,'Dial and calibrated face',[0,.05,.30],.075);ring(m,(0,.51,.29),.275,.232,.05,'metal',(pi/2,0,0));front(m,(0,.51,.31),.23,.02,'paper');marks(m,(0,.51,.324),.198,40)
        group(m,'Needle and crystal',[0,.05,.48],.12);m.rod((0,.51,.337),(.11,.64,.337),.009,'accent');front(m,(0,.51,.341),.021,.009,'metal');m.ball((0,.51,.353),.23,'glass',scale=(1,1,.035),seg=96,rings=24)
        group(m,'Weighing platform',[0,.39,0],.095);m.cyl((0,.86,0),.08,.14,'metal');bowl(m,(0,.91,0),.58,.15,'metal',.025)
    elif s=='pepper-mill':
        group(m,'Turned grinder body',[0,-.10,0]);lathe(m,[(0,.03),(.27,.03),(.32,.07),(.32,.17),(.27,.25),(.21,.36),(.18,.63),(.20,.83),(.25,.95),(.27,.98),(.23,1.00),(.20,.92),(.15,.82),(.13,.35),(.20,.16),(0,.12)],mat='secondary',seg=128,steps=8)
        group(m,'Burr and spindle',[0,.18,0],.045);m.cyl((0,.48,0),.018,.76,'metal');ring(m,(0,.095,0),.18,.06,.05,'metal')
        for i in range(12):
            a=2*pi*i/12;m.rod((.07*cos(a),.07,.07*sin(a)),(.16*cos(a+.12),.11,.16*sin(a+.12)),.009,'metal')
        group(m,'Rounded mill crown',[0,.43,0],.095);lathe(m,[(0,.97),(.24,.97),(.32,1.04),(.35,1.17),(.31,1.31),(.20,1.39),(0,1.40)],mat='secondary',seg=128,steps=8);m.torus((0,.98,0),.245,.012,'metal')
        group(m,'Adjustment screw',[0,.64,0],.15);m.knurl((0,1.44,0),.045,.055,'metal',32)
    else:raise KeyError(s)
