"""Individually proportioned desk collection and its assembly choreography."""
from quality_geometry import *

def build(m):
    s=m.slug
    if s=='dome-lamp':
        group(m,'Ceramic pedestal',[0,-.08,0])
        lathe(m,[(0,.035),(.31,.035),(.35,.055),(.33,.10),(.25,.14),(.20,.23),(.18,.40),(.15,.75),(.115,1.05),(.10,1.10),(0,1.10)],mat='body',label='continuous-flared-ceramic-pedestal',seg=128)
        group(m,'Silicone foot',[0,-.20,0],.04);m.cyl((0,.025,0),.28,.04,'rubber')
        group(m,'Light engine',[0,.23,0],.035);m.cyl((0,1.045,0),.10,.13,'metal');m.cyl((0,1.10,0),.17,.04,'paper')
        group(m,'Hollow enamel shade',[0,.56,0],.08)
        profile=[(.703,1.055),(.72,1.065)]
        profile +=[(.72*cos(pi/2*i/48),1.08+.42*sin(pi/2*i/48)) for i in range(49)]
        profile +=[(0,1.46)] +[(.686*sin(pi/2*i/48),1.08+.384*cos(pi/2*i/48)) for i in range(1,49)]
        profile +=[(.70,1.065),(.703,1.055)]
        # The central clearance is hidden by the diffuser when assembled.
        m.lathe(profile,mat='accent',seg=144,label='double-walled-enamel-dome')
        group(m,'Opal diffuser',[0,.36,0],.055);m.cyl((0,1.065,0),.59,.018,'paper')
        group(m,'Shade finial',[0,.74,0],.13);m.ball((0,1.535,0),.035,'body',scale=(1,1.3,1))
    elif s=='task-lamp':
        group(m,'Weighted base',[0,-.12,0]);lathe(m,[(0,.04),(.43,.04),(.49,.08),(.48,.14),(.40,.19),(0,.19)],mat='body')
        feet(m,(-.28,.28),(-.23,.23),.022)
        group(m,'Lower arm',[-.14,.06,0],.025)
        for z in (-.045,.045):m.rod((0,.19,z),(-.34,.84,z),.022,'metal')
        for p in [(0,.21,0),(-.34,.84,0)]:front(m,p,.075,.15,'accent')
        screws(m,[(-.34,.84,.08),(0,.21,.08)],.023)
        group(m,'Upper arm',[.06,.22,0],.055)
        for z in (-.045,.045):m.rod((-.34,.84,z),(.18,1.33,z),.022,'metal')
        front(m,(.18,1.33,0),.075,.16,'accent')
        group(m,'Reflector shade',[.20,.43,.07],.095)
        # A rounded double-wall bell with a continuous rolled mouth; the light
        # disk shares its axis and sits inside the opening rather than above it.
        origin=(.23,1.33,0);tilt=-2.25
        profile=[(0,-.055),(.055,-.055),(.082,-.03),(.098,.035),(.13,.14),(.19,.275),(.225,.325),(.235,.345),(.231,.36),(.214,.366),(.205,.349),(.186,.29),(.125,.15),(.087,.04),(.064,-.005),(0,-.005)]
        lathe(m,profile,origin,'secondary',(0,0,tilt),'smooth-double-wall-bell-shade',144,8)
        m.ball(origin,.067,'secondary',seg=80,rings=40)
        group(m,'Lamp diffuser',[.27,.30,.08],.075)
        mouth=(origin[0]-sin(tilt)*.321,origin[1]+cos(tilt)*.321,0)
        m.cyl(mouth,.203,.014,'paper',(0,0,tilt),label='recessed-opal-light-disk')
    elif s=='pencil-cup':
        group(m,'Glazed cup',[0,-.08,0]);bowl(m,(0,.025,0),.40,.76,'secondary',.045);m.cyl((0,.022,0),.29,.035,'rubber')
        for i,(x,z,h,mat) in enumerate([(-.16,.06,1.37,'accent'),(.10,-.10,1.58,'metal'),(.18,.12,1.25,'ink')]):
            group(m,['Colored pencil','Mechanical pencil','Fineliner'][i],[(i-1)*.18,.46+i*.10,0],.04*i)
            m.cyl((x,(h+.13)/2,z),.033,h-.13,mat,label='continuous-pencil-barrel')
            m.cyl((x,h+.065,z),.033,.13,'paper',top=.004);m.cyl((x,h+.13,z),.008,.025,'ink',top=0)
            m.cyl((x,.19,z),.035,.07,'metal')
    elif s=='stapler':
        group(m,'Weighted lower shell',[0,-.12,0]);tray(m,(0,.145,0),(1.48,.24,.49),'ink',.12,axis='y')
        feet(m,(-.52,.52),(-.16,.16),.027)
        group(m,'Staple magazine',[0,.14,.10],.04);tray(m,(.02,.28,0),(1.15,.12,.29),'metal',.025,wall=.018,axis='y')
        for i in range(16):m.box((-.44+i*.055,.34,0),(.035,.035,.235),'metal',.008)
        group(m,'Sculpted upper lever',[0,.38,0],.09);lid(m,(-.01,.40,0),(1.43,.26,.47),'accent',.14)
        group(m,'Hinge pin',[-.24,.08,.16],.02);front(m,(-.56,.30,0),.07,.55,'metal');screws(m,[(-.56,.30,.28)],.025)
        group(m,'Anvil',[.18,.04,.09],.03);m.box((.48,.28,0),(.18,.025,.20),'metal',.024)
    elif s=='pocket-notebook':
        group(m,'Clothbound back',[0,-.10,0]);m.box((0,.045,0),(1.12,.065,1.52),'fabric',.055)
        group(m,'Sewn page block',[0,.10,0],.045);m.box((.015,.155,0),(1.04,.17,1.43),'paper',.04)
        for y in [.09+i*.014 for i in range(10)]:m.box((.534,y,0),(.006,.002,1.30),'body',.0008)
        group(m,'Clothbound front',[0,.31,0],.085);m.box((0,.275,0),(1.12,.065,1.52),'fabric',.055)
        group(m,'Spine and headbands',[-.20,.02,0],.02);m.box((-.52,.16,0),(.12,.27,1.53),'fabric',.055)
        for z in (-.72,.72):m.rod((-.47,.19,z),(.43,.19,z),.008,'accent')
        group(m,'Elastic and bookmark',[.13,.43,.06],.12);m.box((.34,.315,0),(.06,.015,1.51),'rubber',.006);m.box((.08,.13,.82),(.065,.012,.33),'accent',.006)
    elif s=='calculator':
        group(m,'Lower casing',[0,-.12,0]);tray(m,(0,.13,0),(1.02,.23,1.57),'body',.13,axis='y');feet(m,(-.33,.33),(-.54,.54),.025)
        group(m,'PCB and display',[0,.14,0],.035);m.box((0,.25,0),(.83,.025,1.30),'circuit',.055)
        m.box((0,.30,-.47),(.89,.028,.43),'ink',.035);m.box((0,.319,-.47),(.73,.009,.29),'lens',.025)
        for col in range(6):
            for dz in (-.06,.06):m.box((-.27+col*.105,.325,-.47+dz),(.06,.002,.009),'secondary',.002)
        group(m,'Top faceplate',[0,.29,0],.07)
        # Individual rails frame the display instead of a plate covering it.
        for x in (-.47,.47):m.box((x,.29,-.47),(.07,.08,.43),'body',.032)
        for z in (-.73,-.23):m.box((0,.29,z),(.96,.08,.08),'body',.035)
        m.box((0,.29,.23),(.97,.08,.90),'body',.035)
        group(m,'Tactile key set',[0,.49,0],.12)
        for row in range(4):
            for col in range(3):m.box((-.30+col*.30,.365,-.05+row*.23),(.23,.09,.18),'accent' if col==2 else 'secondary',.035)
    elif s=='tape-dispenser':
        group(m,'Weighted cast base',[0,-.10,0]);shape_loft(m,[(-.67,-.12),(-.66,.05),(-.52,.10),(-.49,.35),(-.33,.50),(-.05,.45),(.12,.16),(.51,.14),(.57,.36),(.68,.33),(.68,-.12)],.44,(0,.18,0),'secondary')
        feet(m,(-.45,.48),(-.13,.13),.025)
        group(m,'Tape core',[0,.22,0],.045);ring(m,(-.28,.53,0),.23,.14,.31,'paper',(pi/2,0,0))
        group(m,'Tape roll',[-.08,.44,.05],.085);ring(m,(-.28,.53,0),.31,.235,.28,'body',(pi/2,0,0))
        for z in (-.145,.145):m.torus((-.28,.53,z),.274,.004,'paper',(pi/2,0,0))
        group(m,'Feed strip',[.11,.52,.05],.11);m.box((.12,.69,0),(.68,.012,.25),'paper',.005,rot=(0,0,-.20))
        group(m,'Serrated cutter',[.24,.21,0],.04);m.box((.58,.55,0),(.11,.018,.36),'metal',.009)
        for i in range(12):m.cyl((.63,.559,-.16+i*.029),.009,.018,'metal',top=0)
    elif s=='alarm-clock':
        group(m,'Clock housing',[0,-.07,-.13]);lathe(m,[(0,-.19),(.42,-.19),(.52,-.14),(.55,-.04),(.55,.10),(.52,.18),(.46,.19),(.46,-.10),(0,-.10)],(0,.73,0),'secondary',(pi/2,0,0),'hollow-clock-case')
        for x in (-.34,.34):m.rod((x*.8,.32,0),(x*1.12,.06,0),.037,'metal')
        group(m,'Clock face',[0,.025,.34],.035);front(m,(0,.73,.16),.462,.024,'paper');marks(m,(0,.73,.177),.41)
        group(m,'Hands and spindle',[0,.025,.53],.075)
        for end,r,c in [((-.19,.91,.206),.015,'ink'),((.23,.88,.214),.011,'accent')]:m.rod((0,.73,end[2]),end,r,c)
        front(m,(0,.73,.221),.032,.017,'metal')
        group(m,'Front crystal',[0,.025,.70],.12);m.ball((0,.73,.235),.465,'glass',scale=(1,1,.045),seg=112,rings=32)
        group(m,'Bells and hammer',[0,.44,-.04],.09)
        for x in (-.33,.33):
            bowl(m,(x,1.17,0),.22,.14,'accent',.024);m.rod((x*.75,1.12,0),(x,1.22,0),.022,'metal')
        cable(m,[(-.29,1.24,-.08),(-.22,1.48,-.08),(.22,1.48,-.08),(.29,1.24,-.08)],.019,'metal');m.rod((0,1.20,0),(0,1.37,0),.016,'metal')
    elif s=='sand-timer':
        group(m,'Lower turned plinth',[0,-.16,0]);lathe(m,[(0,.02),(.38,.02),(.43,.06),(.43,.12),(.38,.16),(0,.16)],mat='secondary')
        group(m,'Glass hourglass',[0,.14,0],.04)
        lathe(m,[(0,.18),(.25,.18),(.30,.23),(.30,.37),(.21,.54),(.065,.72),(.045,.78),(.065,.84),(.21,1.02),(.30,1.19),(.30,1.32),(.25,1.37),(0,1.37)],mat='glass',label='continuous-blown-hourglass',seg=128,steps=8)
        group(m,'Fine sand',[0,.14,0],.04);lathe(m,[(0,.19),(.26,.19),(.27,.24),(.20,.31),(.02,.56),(0,.56)],mat='sand');m.cyl((0,.73,0),.009,.29,'sand')
        group(m,'Protective frame',[.26,.03,-.09],.07)
        for a in (pi/6,5*pi/6,3*pi/2):m.rod((.35*cos(a),.12,.35*sin(a)),(.35*cos(a),1.43,.35*sin(a)),.021,'metal')
        group(m,'Upper turned plinth',[0,.46,0],.10);lathe(m,[(0,1.37),(.38,1.37),(.43,1.41),(.43,1.47),(.38,1.51),(0,1.51)],mat='secondary')
    elif s=='fountain-pen':
        group(m,'Lacquer barrel',[0,-.12,0]);lathe(m,[(0,.04),(.07,.04),(.11,.10),(.12,.32),(.115,.86),(.10,.94),(0,.94)],mat='secondary')
        group(m,'Grip and feed',[0,.19,0],.04);m.cyl((0,1.015,0),.094,.19,'ink',top=.075);m.cyl((0,.925,0),.105,.035,'metal')
        group(m,'Gold nib',[0,.39,.035],.095)
        shape_loft(m,[(-.071,0),(-.055,.12),(0,.30),(.055,.12),(.071,0)],.025,(0,1.075,.015),'metal','sculpted-fountain-nib')
        m.box((0,1.23,.032),(.003,.22,.003),'ink',.0008);front(m,(0,1.14,.033),.012,.005,'ink')
        group(m,'Posted cap',[.27,.05,-.08],.065);lathe(m,[(0,.02),(.13,.02),(.145,.07),(.145,.51),(.125,.56),(.105,.54),(.105,.10),(0,.10)],(.27,0,-.08),'accent')
        m.cyl((.27,.08,-.08),.149,.03,'metal');cable(m,[(.27,.52,.065),(.27,.49,.09),(.27,.18,.09),(.27,.16,.065)],.013,'metal')
    else:raise KeyError(s)
