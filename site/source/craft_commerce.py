"""Commerce: folded packaging, stitched surfaces and fitted product parts."""
from quality_geometry import *
from purposeful_motion import panel

def build(m):
    s=m.slug
    if s=='shopping-tote':
        m.palette['secondary']=('#bcc8e9',.88,0);m.palette['body']=('#f5f5f1',.86,0)
        group(m,'Sewn canvas body',[0,-.08,0]);tray(m,(0,.61,0),(1.12,1.14,.53),'secondary',.13,.025,axis='y')
        for z in (-.267,.267):
            seams(m,[(-.46,.10,z),(-.49,.18,z),(-.49,1.10,z)],.004,'body');seams(m,[(.46,.10,z),(.49,.18,z),(.49,1.10,z)],.004,'body')
        group(m,'Reinforced top binding',[0,.18,0],.04)
        for z in (-.25,.25):m.box((0,1.18,z),(1.04,.065,.032),'body',.015)
        group(m,'Woven handles',[0,.45,0],.10)
        for z in (-.23,.23):
            cable(m,[(-.28,.97,z),(-.28,1.39,z),(-.18,1.55,z),(.18,1.55,z),(.28,1.39,z),(.28,.97,z)],.022,'body')
            for x in (-.28,.28):m.box((x,1.05,z),(.07,.19,.018),'body',.013)
        group(m,'Front label pocket',[0,.08,.29],.065);tray(m,(0,.61,.276),(.40,.34,.035),'body',.045,.015,axis='y')
        for x in (-.16,.16):seams(m,[(x,.48,.300),(x,.71,.300)],.003,'secondary')
    elif s=='ribbon-gift':
        group(m,'Open gift box',[0,-.13,0]);tray(m,(0,.49,0),(.98,.90,.98),'body',.095,.04,axis='y')
        group(m,'Folded tissue',[0,.18,0],.04);m.box((0,.77,0),(.83,.035,.82),'paper',.035,rot=(0,.10,0));m.box((.06,.81,0),(.70,.026,.77),'paper',.025,rot=(0,-.12,.025))
        group(m,'Fitted lid',[0,.44,0],.09);lid(m,(0,.98,0),(1.055,.14,1.055),'secondary',.085)
        group(m,'Satin ribbon',[0,.59,0],.13)
        for z in (-.505,.505):m.box((0,.51,z),(.13,.88,.015),'accent',.006)
        m.box((0,1.06,0),(.13,.015,1.07),'accent',.006);m.box((0,1.061,0),(1.07,.015,.13),'accent',.006)
        # Flat ribbon loops, lofted with a thin section rather than doughnut bows.
        for sign in (-1,1):
            cable(m,[(0,1.10,0),(sign*.21,1.24,-.02),(sign*.34,1.20,.02),(sign*.26,1.10,.07),(0,1.10,0)],.026,'accent')
        m.box((0,1.115,0),(.11,.07,.11),'accent',.03)
    elif s=='payment-terminal':
        group(m,'Lower terminal enclosure',[0,-.13,0]);tray(m,(0,.23,0),(.78,.38,1.26),'secondary',.13,axis='y');feet(m,(-.25,.25),(-.43,.43),.034)
        group(m,'Controller board',[0,.15,0],.035);m.box((0,.41,0),(.63,.025,1.07),'circuit',.06)
        group(m,'Display and face',[0,.31,0],.08);panel(m,(0,.435,0),(.74,.045,1.17),'secondary',.11,'y','fitted-terminal-control-deck');m.box((0,.465,-.30),(.60,.025,.45),'ink',.04);m.box((0,.483,-.30),(.52,.012,.36),'lens',.03)
        group(m,'Payment keys',[0,.48,0],.13)
        for row in range(3):
            for col in range(3):m.box((-.21+col*.21,.50,.06+row*.20),(.15,.065,.135),'accent' if row==2 else 'body',.025)
        group(m,'Card reader',[0,.05,.23],.05);m.box((0,.22,.641),(.53,.055,.018),'ink',.022);m.box((0,.187,.652),(.53,.015,.015),'metal',.006)
        for i in range(3):m.torus((0,.494,-.30),.065+i*.028,.003,'body',arc=pi,seg=48)
    elif s=='delivery-parcel':
        m.palette['secondary']=('#bcc8e9',.82,0)
        group(m,'Folded carton',[0,-.08,0]);tray(m,(0,.54,0),(1.26,1.03,.92),'secondary',.055,.025,axis='y')
        for x in (-.61,.61):seams(m,[(x,.10,.44),(x,.93,.44)],.003,'body')
        group(m,'Inner flap pair',[0,.24,0],.04)
        for x in (-.32,.32):m.box((x,1.06,0),(.60,.025,.84),'secondary',.012)
        group(m,'Outer flap pair',[0,.43,0],.09)
        for z in (-.225,.225):m.box((0,1.09,z),(1.24,.025,.44),'secondary',.012)
        group(m,'Paper sealing tape',[0,.59,0],.14);m.box((0,1.11,0),(.20,.009,.90),'paper',.004);m.box((0,.72,.466),(.20,.72,.009),'paper',.004)
        group(m,'Shipping label',[.16,.03,.22],.065);m.box((.30,.70,.47),(.38,.29,.008),'body',.012)
        for i in range(11):m.box((.16+i*.025,.69,.477),(.006 if i%3 else .012,.14,.003),'ink',.0006)
        for y,w in [(.80,.23),(.77,.17)]:m.box((.29,y,.477),(w,.008,.003),'ink',.002)
    elif s=='market-basket':
        group(m,'Basket base',[0,-.12,0]);m.box((0,.09,0),(1.11,.13,.73),'secondary',.06)
        group(m,'Slotted sidewalls',[0,.12,0],.04)
        for z in (-.36,.36):
            for i in range(10):m.box((-.51+i*.113,.37,z),(.046,.49,.045),'secondary',.02)
            for y in (.15,.59):m.box((0,y,z),(1.18,.06,.07),'secondary',.025)
        for x in (-.56,.56):
            for z in (-.25,-.083,.083,.25):m.box((x,.37,z),(.055,.49,.045),'secondary',.02)
        group(m,'Reinforced rim',[0,.29,0],.08)
        for z in (-.37,.37):m.box((0,.65,z),(1.23,.085,.09),'body',.04)
        for x in (-.57,.57):m.box((x,.65,0),(.09,.085,.76),'body',.04)
        group(m,'Folding handle',[0,.52,0],.13);cable(m,[(-.59,.64,0),(-.54,.98,0),(-.37,1.20,0),(.37,1.20,0),(.54,.98,0),(.59,.64,0)],.035,'accent')
        for x in (-.60,.60):m.cyl((x,.65,0),.055,.035,'metal',(0,0,pi/2))
    elif s=='price-tag':
        group(m,'Tag stock',[0,-.07,-.07]);shape_loft(m,[(-.37,-.52),(.37,-.52),(.39,.26),(.20,.54),(-.20,.54),(-.39,.26)],.065,(0,.58,0),'body','die-cut-soft-corner-tag')
        group(m,'Eyelet',[0,.17,.14],.05);ring(m,(0,.94,.045),.068,.037,.016,'metal',(pi/2,0,0))
        group(m,'Braided cord',[0,.40,0],.11);cable(m,[(0,.94,.065),(-.13,1.22,.06),(-.08,1.49,0),(.22,1.48,-.04),(.27,1.20,-.04),(0,.94,-.04)],.012,'accent')
        group(m,'Embossed seal',[0,.03,.35],.075);front(m,(0,.47,.047),.21,.017,'secondary');ring(m,(0,.47,.060),.18,.17,.007,'metal',(pi/2,0,0));m.box((0,.47,.07),(.17,.035,.01),'paper',.012)
    elif s=='coin-stack':
        for stack,(x,n,z) in enumerate([(-.26,6,0),(.42,3,.14)]):
            for i in range(n):
                group(m,('Tall' if stack==0 else 'Short')+f' stack coin {i+1}',[(-.11 if stack==0 else .13),i*.065,0],min(.16,i*.025))
                y=.061+i*.105;m.cyl((x,y,z),.31,.09,'metal');m.knurl((x,y,z),.312,.056,'metal',64)
                for sy in (-1,1):m.torus((x,y+sy*.043,z),.275,.006,'metal')
                if i==n-1:
                    m.cyl((x,y+.047,z),.19,.005,'accent');m.torus((x,y+.052,z),.16,.004,'metal');m.box((x,y+.055,z),(.14,.007,.027),'metal',.006)
    elif s=='store-awning':
        group(m,'Store foundation',[0,-.14,0]);m.box((0,.065,.04),(1.43,.10,.91),'secondary',.045)
        group(m,'Store shell',[0,.03,-.17],.035);tray(m,(0,.70,-.015),(1.22,1.17,.62),'body',.075,.045)
        group(m,'Shopfront glazing',[0,.08,.26],.075);m.box((-.19,.63,.312),(.62,.72,.021),'lens',.035)
        for x in (-.52,.15):m.box((x,.63,.33),(.04,.79,.04),'secondary',.015)
        for y in (.24,1.02):m.box((-.185,y,.33),(.71,.04,.04),'secondary',.015)
        m.box((.40,.58,.321),(.30,.92,.035),'secondary',.035);m.box((.40,.66,.345),(.23,.57,.01),'lens',.02);front(m,(.49,.48,.35),.017,.025,'metal')
        group(m,'Striped curved awning',[0,.44,.12],.13)
        for i in range(7):
            x=-.60+i*.20;pts=[];idx=[]
            for j in range(25):
                a=pi/2*j/24;y=1.19+.18*cos(a);z=.08+.62*sin(a)
                pts.extend([[x,y,z],[x+.20,y,z]])
            for j in range(24):a=j*2;idx.extend([a,a+1,a+2,a+1,a+3,a+2])
            add_mesh(m,pts,idx,'accent' if i%2==0 else 'paper','curved-awning-panel')
            m.box((x+.10,1.15,.70),(.20,.10,.025),'accent' if i%2==0 else 'paper',.035)
    elif s=='receipt-printer':
        group(m,'Printer lower case',[0,-.10,0]);tray(m,(0,.40,0),(1.05,.72,.90),'secondary',.17,axis='y');feet(m,(-.34,.34),(-.27,.27),.035)
        group(m,'Paper roll',[0,.18,0],.04);m.cyl((0,.59,-.08),.23,.62,'paper',(0,0,pi/2));ring(m,(.316,.59,-.08),.20,.08,.008,'body',(0,0,pi/2))
        group(m,'Feed mechanism',[0,.32,.05],.075);m.cyl((0,.67,.30),.045,.72,'rubber',(0,0,pi/2));m.box((0,.71,.35),(.77,.035,.08),'metal',.015)
        group(m,'Rounded top cover',[0,.50,-.02],.12);lid(m,(0,.79,-.07),(1.02,.18,.72),'secondary',.13);m.cyl((.32,.89,.13),.055,.025,'accent')
        group(m,'Curled receipt',[0,.63,.17],.17)
        pts=[];idx=[]
        for j in range(41):
            t=j/40;y=.70+.72*t;z=.34+.10*sin(t*pi*1.4)
            pts.extend([[-.29,y,z],[.29,y,z]])
        for j in range(40):a=j*2;idx.extend([a,a+1,a+2,a+1,a+3,a+2])
        add_mesh(m,pts,idx,'paper','continuous-curled-receipt')
        for j in range(8):
            t=.25+j*.075;m.box((-.035,.70+.72*t,.349+.10*sin(t*pi*1.4)),(.36 if j%3 else .23,.008,.004),'ink',.0015)
    elif s=='piggy-bank':
        group(m,'Glazed ceramic body',[0,-.08,0]);m.ball((0,.53,0),.48,'secondary',scale=(1.25,1,.91),seg=96,rings=48)
        for x in (-.28,.28):
            for z in (-.24,.24):lathe(m,[(0,.035),(.066,.035),(.085,.08),(.08,.23),(.055,.27),(0,.27)],(x,0,z),'secondary')
        group(m,'Sculpted snout',[.26,.02,.03],.04);m.ball((.57,.55,0),.18,'accent',scale=(.53,.85,1))
        for z in (-.065,.065):m.ball((.664,.56,z),.018,'ink',scale=(.25,1,1),seg=24,rings=12)
        group(m,'Ears and eye inlays',[0,.26,0],.085)
        for z in (-.23,.23):shape_loft(m,[(-.06,0),(-.08,.12),(0,.24),(.08,.12),(.06,0)],.065,(.26,.84,z),'secondary','soft-ceramic-ear');m.ball((.39,.72,z*1.55),.021,'ink',seg=24,rings=12)
        group(m,'Savings slot and coin',[0,.52,0],.14);m.box((-.08,1.008,0),(.26,.008,.035),'ink',.015);m.cyl((-.08,1.07,0),.14,.024,'metal',(pi/2,0,0))
        group(m,'Curled tail',[-.24,.04,0],.055);m.torus((-.60,.59,0),.085,.018,'accent',(0,0,pi/2),arc=pi*1.8)
    else:raise KeyError(s)
