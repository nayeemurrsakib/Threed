"""Authored device housings, controls, drivers and removable assemblies."""
from quality_geometry import *
from purposeful_motion import panel

def build(m):
    s=m.slug
    if s=='portable-radio':
        group(m,'Hollow rear enclosure',[.08,0,-.19]);tray(m,(0,.57,-.06),(1.66,1.04,.46),'secondary',.19)
        group(m,'Amplifier board',[0,.08,.02],.03);m.box((0,.56,.05),(1.39,.82,.028),'circuit',.10)
        for x in (-.45,-.12,.21):m.box((x,.44,.08),(.17,.15,.045),'ink',.018)
        group(m,'Speaker cone',[-.15,0,.20],.05)
        lathe(m,[(0,-.04),(.08,-.04),(.18,-.01),(.29,.035),(.31,.06),(.30,.075),(.27,.06),(.16,.015),(0,.01)],(-.27,.56,.16),'ink',(pi/2,0,0),'recessed-paper-speaker-cone')
        m.torus((-.27,.56,.21),.285,.026,'rubber',(pi/2,0,0))
        group(m,'Front cover and grille',[-.16,0,.48],.095)
        m.box((0,.57,.205),(1.56,.94,.045),'secondary',.14,label='fitted-radio-front-cover')
        m.box((-.28,.55,.255),(.94,.78,.025),'body',.09)
        m.box((-.28,.55,.273),(.80,.65,.009),'ink',.026)
        m.grille((-.64,.262,.286),12,10,.064,.018,'body')
        group(m,'Tuner display',[.12,.14,.36],.07)
        m.box((.48,.86,.205),(.45,.125,.035),'ink',.035);m.box((.48,.86,.226),(.38,.075,.009),'lens',.02)
        for i in range(9):m.box((.33+i*.037,.86,.235),(.004,.023 if i%2 else .04,.003),'paper',.001)
        m.box((.51,.86,.239),(.006,.058,.004),'accent',.002)
        group(m,'Tuning dial',[.18,0,.67],.15)
        ring(m,(.51,.44,.25),.177,.135,.06,'metal',(pi/2,0,0));front(m,(.51,.44,.277),.143,.043,'body');m.box((.51,.495,.303),(.009,.075,.004),'ink',.002)
        group(m,'Handle and antenna',[.06,.37,-.09],.11)
        cable(m,[(-.49,1.06,-.1),(-.39,1.27,-.1),(.39,1.27,-.1),(.49,1.06,-.1)],.025,'leather')
        m.cyl((-.58,1.11,-.14),.035,.09,'metal');m.rod((-.58,1.15,-.14),(-.10,1.58,-.14),.012,'metal');m.rod((-.10,1.58,-.14),(.21,1.86,-.14),.007,'metal');m.ball((.21,1.86,-.14),.012,'metal')
        group(m,'Rubber feet',[0,-.17,0],.02);feet(m,(-.52,.52),(-.13,.13),.035)
    elif s=='over-ear-headphones':
        group(m,'Spring headband',[0,.27,0],.055)
        points=[(.64*cos(pi*i/64),.69+.78*sin(pi*i/64),0) for i in range(65)];m.tube(points,.044,'metal')
        group(m,'Padded headband',[0,.43,0],.095)
        m.tube([(.60*cos(.12+(pi-.24)*i/64),.69+.72*sin(.12+(pi-.24)*i/64),0) for i in range(65)],.068,'leather')
        for sign in (-1,1):
            group(m,('Left' if sign<0 else 'Right')+' earcup',[sign*.31,0,0],.035)
            m.box((sign*.64,.49,0),(.24,.63,.45),'body',.115);m.box((sign*.775,.49,0),(.045,.43,.32),'accent',.02)
            for z in (-.16,.16):m.rod((sign*.65,.72,z),(sign*.65,.92,z),.016,'metal')
            group(m,('Left' if sign<0 else 'Right')+' acoustic cushion',[sign*.12,-.10,.28],.085)
            # Annular ear pads have real openings rather than solid rubber slabs.
            ring(m,(sign*.49,.49,0),.255,.16,.105,'rubber',(0,0,pi/2));m.cyl((sign*.495,.49,0),.16,.018,'fabric',(0,0,pi/2))
    elif s=='game-controller':
        contour=[(-.76,-.11),(-.65,.23),(-.38,.31),(0,.28),(.38,.31),(.65,.23),(.76,-.11),(.67,-.40),(.48,-.41),(.30,-.12),(-.30,-.12),(-.48,-.41),(-.67,-.40)]
        group(m,'Sculpted lower grip',[0,-.15,-.08]);shape_loft(m,contour,.28,(0,.52,0),'body','continuous-ergonomic-controller-shell')
        group(m,'Upper control surface',[0,.19,.07],.05);shape_loft(m,[(x*.97,y*.96) for x,y in contour],.08,(0,.54,.18),'secondary','continuous-control-face')
        group(m,'Analog modules',[0,.37,.12],.09)
        for x,y in [(-.25,.43),(.23,.38)]:
            front(m,(x,y,.25),.122,.045,'ink');front(m,(x,y,.30),.083,.06,'rubber');m.torus((x,y,.334),.061,.008,'rubber',(pi/2,0,0))
        group(m,'Action keys',[.16,.48,.16],.13)
        for dx,dy in [(0,.09),(.09,0),(0,-.09),(-.09,0)]:front(m,(.49+dx,.64+dy,.255),.036,.043,'accent')
        m.box((-.47,.65,.26),(.24,.065,.05),'ink',.022);m.box((-.47,.65,.26),(.065,.24,.05),'ink',.022)
        for x in (-.43,.43):m.box((x,.86,-.03),(.32,.07,.13),'rubber',.035)
        group(m,'Status strip',[0,.28,.29],.07);m.box((0,.69,.258),(.14,.023,.018),'paper',.01)
        m.presentation['viewDirection']=[.40,.42,1]
    elif s=='bookshelf-speaker':
        group(m,'Rounded speaker cabinet',[.05,0,-.19]);tray(m,(0,.80,-.08),(.98,1.48,.63),'secondary',.15,wall=.045)
        group(m,'Acoustic baffle',[0,0,.26],.035);panel(m,(0,.80,.26),(.86,1.35,.055),'ink',.11)
        group(m,'Woofer basket',[0,-.04,.47],.065)
        ring(m,(0,.57,.31),.31,.24,.07,'metal',(pi/2,0,0));m.torus((0,.57,.365),.265,.034,'rubber',(pi/2,0,0))
        lathe(m,[(0,-.05),(.07,-.05),(.16,-.01),(.23,.025),(.24,.05),(.20,.045),(.10,.01),(0,.01)],(0,.57,.35),'ink',(pi/2,0,0),'continuous-woofer-cone');m.ball((0,.57,.365),.10,'rubber',scale=(1,1,.35))
        group(m,'Tweeter assembly',[0,.09,.61],.11);ring(m,(0,1.16,.32),.145,.09,.04,'metal',(pi/2,0,0));m.ball((0,1.16,.36),.09,'ink',scale=(1,1,.4))
        group(m,'Cabinet feet',[0,-.15,0]);feet(m,(-.29,.29),(-.20,.20),.035)
        group(m,'Fasteners and status',[0,0,.27],.035);screws(m,[(-.35,.23,.294),(.35,.23,.294),(-.35,1.38,.294),(.35,1.38,.294)],.013);front(m,(.30,.22,.31),.012,.01,'accent')
    elif s=='desktop-display':
        group(m,'Weighted foot',[0,-.12,0]);lathe(m,[(0,.025),(.30,.025),(.43,.05),(.46,.09),(.42,.13),(0,.13)],mat='secondary');m.cyl((0,.022,0),.32,.025,'rubber')
        group(m,'Stand and hinge',[0,.09,-.13],.035);m.box((0,.48,-.14),(.14,.78,.13),'metal',.055);front(m,(0,.88,-.10),.12,.24,'metal')
        group(m,'Rear display enclosure',[0,.13,-.31],.07);tray(m,(0,1.15,-.045),(1.82,1.13,.15),'body',.12,wall=.025)
        for i in range(12):m.box((-.40+i*.073,.69,-.127),(.038,.009,.009),'ink',.003)
        group(m,'LCD module',[0,.13,.22],.11);panel(m,(0,1.17,.051),(1.66,.96,.024),'ink',.065);panel(m,(0,1.17,.068),(1.58,.88,.012),'lens',.045)
        group(m,'Edge frame',[0,.13,.38],.15)
        for x in (-.875,.875):m.box((x,1.15,.08),(.06,1.02,.045),'body',.027)
        for y in (.62,1.68):m.box((0,y,.08),(1.77,.06,.045),'body',.027)
        front(m,(.72,.64,.11),.008,.007,'accent')
    elif s=='mechanical-keyboard':
        group(m,'Aluminum lower tray',[0,-.12,0]);tray(m,(0,.13,0),(1.92,.20,.82),'metal',.095,axis='y');feet(m,(-.7,.7),(-.23,.23),.033)
        group(m,'PCB and switch plate',[0,.14,0],.035);m.box((0,.235,0),(1.77,.026,.68),'circuit',.055);m.box((0,.257,0),(1.80,.018,.71),'body',.045)
        group(m,'Mechanical switches',[0,.30,0],.08)
        for row in range(4):
            for col in range(10):
                if row==3 and 2<=col<=6:continue
                m.box((-.825+col*.183,.282,-.27+row*.18),(.08,.045,.075),'ink',.015)
        group(m,'Sculpted keycaps',[0,.49,0],.13)
        for row in range(4):
            for col in range(10):
                if row==3 and 2<=col<=6:continue
                # Separate lip and crowned cap catch light without painted key outlines.
                m.box((-.825+col*.183,.333,-.27+row*.18),(.151,.083,.143),'accent' if col in (0,9) else 'secondary',.024)
        m.box((-.09,.332,.27),(.88,.083,.143),'body',.027)
        group(m,'USB connector',[.12,.02,-.17],.03);m.box((.63,.16,-.416),(.13,.045,.016),'ink',.02)
        m.presentation['viewDirection']=[.40,.72,1]
    elif s=='pocket-console':
        group(m,'Rear enclosure',[.05,0,-.17]);tray(m,(0,.83,-.035),(.98,1.57,.23),'secondary',.17)
        group(m,'Logic board',[0,.05,.07],.035);m.box((0,.83,.045),(.81,1.36,.025),'circuit',.08)
        group(m,'Display unit',[0,.12,.28],.07);m.box((0,1.12,.085),(.81,.64,.03),'ink',.065);m.box((0,1.13,.105),(.66,.47,.012),'lens',.03)
        group(m,'Control face',[0,.035,.40],.10)
        # Display surround and lower control deck leave an actual screen opening.
        for x in (-.45,.45):m.box((x,1.12,.087),(.075,.73,.06),'secondary',.035)
        for y in (.75,1.49):m.box((0,y,.087),(.88,.075,.06),'secondary',.035)
        panel(m,(0,.39,.085),(.96,.66,.065),'secondary',.14)
        for i in range(5):m.box((.08+i*.055,.21,.121),(.015,.10,.009),'ink',.006)
        group(m,'D-pad and action keys',[0,.17,.57],.145)
        m.box((-.25,.49,.14),(.27,.085,.05),'ink',.022);m.box((-.25,.49,.14),(.085,.27,.05),'ink',.022)
        for x,y in [(.20,.44),(.34,.57)]:front(m,(x,y,.14),.066,.05,'accent')
        for x in (-.065,.065):m.box((x,.26,.145),(.07,.021,.025),'rubber',.01,rot=(0,0,.2))
    elif s=='studio-microphone':
        group(m,'Weighted desktop base',[0,-.16,0]);lathe(m,[(0,.02),(.31,.02),(.40,.06),(.40,.11),(.32,.16),(0,.16)],mat='ink');m.cyl((0,.026,0),.29,.035,'rubber')
        group(m,'Stand and yoke',[0,.04,-.10],.03);m.cyl((0,.42,0),.035,.60,'metal');cable(m,[(-.32,1.12,0),(-.32,.72,0),(-.22,.64,0),(.22,.64,0),(.32,.72,0),(.32,1.12,0)],.027,'accent')
        group(m,'Microphone body',[0,.20,0],.065);tray(m,(0,1.07,-.03),(.48,.77,.36),'secondary',.21,wall=.025)
        panel(m,(0,1.07,.142),(.475,.765,.024),'secondary',.205,label='fitted-capsule-microphone-front')
        for x in (-.29,.29):m.cyl((x,1.08,0),.06,.05,'metal',(0,0,pi/2))
        group(m,'Condenser capsule',[0,.36,.19],.10);front(m,(0,1.20,.08),.15,.055,'metal');m.ball((0,1.20,.112),.125,'ink',scale=(1,1,.15))
        group(m,'Perforated grille',[0,.48,.35],.15)
        panel(m,(0,1.18,.155),(.41,.46,.025),'ink',.085);m.grille((-.153,1.014,.174),10,11,.034,.009,'metal')
        m.box((0,.89,.17),(.39,.12,.025),'secondary',.055);front(m,(0,.89,.195),.038,.025,'metal')
    elif s=='web-camera':
        group(m,'Monitor clip',[0,-.12,0]);tray(m,(0,.08,0),(.64,.10,.43),'ink',.045,axis='y');m.box((0,.20,-.11),(.15,.28,.10),'metal',.045)
        group(m,'Camera housing',[.04,.10,-.20],.035);tray(m,(0,.55,-.025),(1.16,.48,.35),'body',.22)
        group(m,'Image sensor',[0,.11,.10],.065);m.box((0,.55,.10),(.19,.19,.035),'circuit',.02);front(m,(0,.55,.135),.08,.02,'lens')
        group(m,'Optical barrel',[0,.11,.34],.10);ring(m,(0,.55,.18),.185,.11,.095,'ink',(pi/2,0,0));m.torus((0,.55,.235),.16,.008,'metal',(pi/2,0,0))
        optical(m,(0,.55,.24),.12,(0,.11,.53))
        group(m,'Privacy slide',[.22,.22,.31],.14);m.box((.28,.55,.166),(.27,.30,.025),'secondary',.12)
        group(m,'Status light',[0,.11,.25],.07);front(m,(-.43,.55,.16),.017,.01,'accent')
    else:raise KeyError(s)
