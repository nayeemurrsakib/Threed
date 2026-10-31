"""Individual desk revisions driven by observed shape and use problems."""
from purposeful_motion import *

def tape(m):
    presentation(m,'Unroll a connected length of tape','HOVER TO UNROLL · DRAG TO EXPLORE',view=[.62,.40,1],frame=.06)
    m.description='A weighted dispenser with a rotating paper core, connected tape feed and fixed serrated cutter.'
    still(m,'Weighted enamel base');m.box((0,.115,0),(1.48,.18,.48),'secondary',.085);feet(m,(-.48,.48),(-.14,.14),.025)
    panel(m,(-.31,.32,-.17),(.49,.44,.10),'secondary',.18,label='rounded-rear-axle-support')
    m.box((.58,.33,0),(.14,.38,.42),'secondary',.06,label='fixed-cutter-pedestal')
    front(m,(-.30,.49,-.04),.103,.30,'secondary',label='recessed-fixed-spool-axle')
    action(m,'Turning tape roll',(-.30,.49,0),angle=-1.36)
    ring(m,(-.30,.49,0),.234,.125,.285,'paper',(pi/2,0,0),label='open-paper-tape-core')
    ring(m,(-.30,.49,0),.310,.235,.265,'body',(pi/2,0,0),label='wound-satin-tape-roll')
    for z in (-.135,.135):m.torus((-.30,.49,z),.274,.003,'paper',(pi/2,0,0),seg=112)
    for a in (.5,2.4,4.3):
        x=-.30+.18*cos(a);y=.49+.18*sin(a)
        m.box((x,y,.147),(.035,.006,.003),'secondary',.001,rot=(0,0,a),label='paper-core-registration-mark')
    # Exact upper tangent from spool to cutter, sampled as a continuous strip.
    a=math.atan2(.04,.90)+math.acos(.31/math.hypot(.90,.04));start=(-.30+.31*cos(a),.49+.31*sin(a),0)
    still(m,'Connected feed span');ribbon(m,[(start[0]+(.60-start[0])*t,start[1]+(.53-start[1])*t,0) for t in [i/32 for i in range(33)]],.245,label='tape-connected-to-roll-and-cutter')
    action(m,'Unrolling tape tail',(.60,.53,0),scaleFrom=[.001,.001,1],scaleTo=[1,1,1])
    ribbon(m,[(.60+.28*t,.53-.11*t-.22*t*t,0) for t in [i/48 for i in range(49)]],.245,label='fed-curving-tape-tail')
    still(m,'Fixed serrated cutter');m.box((.60,.515,0),(.10,.014,.34),'metal',.006)
    for i in range(14):m.cyl((.641,.526,-.153+i*.0235),.007,.013,'metal',top=0)

def calculator(m):
    presentation(m,'A flowing wave across the keys','HOVER FOR A KEY WAVE · DRAG TO EXPLORE',view=[.40,.95,1],frame=.02)
    m.description='A fitted rounded calculator with a stationary display and individually animated tactile keys.'
    still(m,'Closed calculator case');m.box((0,.165,0),(1.02,.27,1.57),'body',.12);feet(m,(-.33,.33),(-.54,.54),.028)
    panel(m,(0,.305,0),(.96,.055,1.49),'body',.105,'y','matching-radius-calculator-top-deck')
    still(m,'Recessed LCD');panel(m,(0,.341,-.47),(.80,.019,.35),'ink',.035,'y');panel(m,(0,.354,-.47),(.72,.010,.27),'lens',.025,'y')
    for col in range(6):
        x=-.27+col*.105
        for dz in (-.065,0,.065):m.box((x,.361,-.47+dz),(.058,.002,.009),'secondary',.001)
        for dx in (-.03,.03):m.box((x+dx,.361,-.502),(.008,.002,.047),'secondary',.001)
    for row in range(4):
        for col in range(3):
            action(m,f'Key {row+1}-{col+1}',wave={'axis':[0,1,0],'amplitude':.022,'lift':.024,'frequency':.85,'phase':-row*.65-col*.48})
            m.box((-.30+col*.30,.378,-.05+row*.23),(.23,.085,.18),'accent' if col==2 else 'secondary',.035,label=f'wave-keycap-{row+1}-{col+1}')

def clock(m):
    presentation(m,'The hands turn and the alarm bells ring','HOVER TO RING · DRAG TO EXPLORE',view=[.40,.25,1])
    m.description='A rounded twin-bell clock with a clear uncovered dial, moving hands and attached ringing bells.'
    still(m,'Clock case and legs');lathe(m,[(0,-.19),(.42,-.19),(.52,-.14),(.55,-.04),(.55,.10),(.52,.18),(.46,.19),(.46,-.10),(0,-.10)],(0,.73,0),'secondary',(pi/2,0,0),'rounded-clock-case')
    for x in (-.34,.34):m.rod((x*.8,.32,0),(x*1.12,.06,0),.037,'metal')
    still(m,'Exposed clock dial');front(m,(0,.73,.17),.463,.026,'paper');marks(m,(0,.73,.185),.41)
    action(m,'Hour hand',(0,.73,.209),angle=-.30);m.rod((0,.73,.209),(-.18,.91,.209),.014,'ink')
    action(m,'Minute hand',(0,.73,.220),angle=-1.7);m.rod((0,.73,.220),(.24,.87,.220),.010,'accent')
    still(m,'Hand spindle');front(m,(0,.73,.232),.027,.012,'metal')
    still(m,'Fixed bell supports')
    for x in (-.33,.33):m.rod((x*.77,1.12,0),(x,1.23,0),.020,'metal')
    cable(m,[(-.29,1.25,-.08),(-.22,1.47,-.08),(.22,1.47,-.08),(.29,1.25,-.08)],.018,'metal')
    for x in (-.33,.33):
        action(m,('Left' if x<0 else 'Right')+' ringing bell',(x,1.23,0),angle=.055,oscillate=9,phase=0 if x<0 else pi)
        lathe(m,[(.22,1.18),(.22,1.21),(.19,1.29),(.10,1.34),(0,1.35),(0,1.326),(.09,1.315),(.17,1.27),(.195,1.21),(.195,1.18),(.22,1.18)],(x,0,0),'accent',label='hollow-domed-alarm-bell',steps=6)
    action(m,'Oscillating alarm hammer',(0,1.15,0),angle=.22,oscillate=9);m.rod((0,1.15,0),(0,1.30,0),.014,'metal');m.box((0,1.31,0),(.11,.028,.035),'metal',.012)

def sand_timer(m):
    presentation(m,'Sand drains through the neck into the lower chamber','HOVER TO RUN · LEAVE TO PAUSE · RESET TO REFILL',view=[.42,.22,1])
    m.description='A fitted blown-glass hourglass with fixed support rods and a visible stream transferring sand between chambers.'
    m.alpha['glass']=.065
    still(m,'Fixed turned frame')
    for y in (.09,1.48):
        lathe(m,[(0,-.065),(.34,-.065),(.40,-.035),(.405,.025),(.37,.065),(0,.065)],(0,y,0),'secondary',label='single-fitted-turned-end-cap')
    for a in (pi/6,5*pi/6,3*pi/2):m.rod((.35*cos(a),.12,.35*sin(a)),(.35*cos(a),1.45,.35*sin(a)),.018,'metal')
    for y in (.17,1.407):ring(m,(0,y,0),.232,.19,.028,'rubber',label='fitted-glass-seat')
    still(m,'Fitted glass vessel')
    profile=[(0,.18),(.22,.18),(.274,.23),(.279,.35),(.224,.49),(.117,.65),(.030,.77),(.022,.80),(.030,.83),(.117,.95),(.224,1.11),(.279,1.25),(.274,1.36),(.22,1.40),(0,1.40)]
    lathe(m,profile,mat='glass',label='continuous-clear-hourglass-skin',seg=144,steps=7)
    action(m,'Draining upper sand',(0,.805,0),timeline=8,scaleFrom=[1,1,1],scaleTo=[.24,.24,.24])
    lathe(m,[(0,.81),(.017,.81),(.074,.94),(.17,1.08),(.235,1.20),(.235,1.23),(0,1.23)],mat='sand',label='upper-sand-reservoir',seg=112)
    action(m,'Growing lower sand',(0,.205,0),timeline=8,scaleFrom=[.24,.24,.24],scaleTo=[1,1,1])
    lathe(m,[(0,.205),(.21,.205),(.235,.225),(.20,.275),(.135,.35),(.025,.505),(0,.51)],mat='sand',label='lower-sand-mound',seg=112)
    action(m,'Falling sand stream',(0,.80,0),timeline=8,scaleFrom=[1,1,1],scaleTo=[1,.57,1])
    m.cyl((0,.535,0),.0035,.53,'sand',label='fine-continuous-sand-stream')
    for i in range(13):
        action(m,f'Falling grain {i+1}',wave={'axis':[0,1,0],'amplitude':.012,'lift':0,'frequency':7,'phase':i*.81})
        m.ball((.002*sin(i*1.7),.30+i*.034,.002*cos(i*1.7)),.004,'sand',seg=8,rings=4,label='falling-sand-grain')

def pen(m):
    presentation(m,'Lift the nib and feed from the open barrel','HOVER TO LIFT THE NIB · DRAG TO EXPLORE',view=[.48,.38,1],frame=.12)
    m.description='A hollow lacquer pen barrel with a continuous open bore, attached nib-and-feed assembly and a separate fitted cap.'
    still(m,'Open lacquer barrel')
    lathe(m,[(0,.04),(.07,.04),(.11,.10),(.12,.32),(.115,.86),(.10,.94),(.076,.94),(.075,.86),(.077,.30),(.068,.14),(0,.12)],mat='secondary',label='hollow-pen-barrel-with-open-bore',seg=128,steps=7)
    m.torus((0,.933,0),.088,.004,'metal',seg=112)
    action(m,'Nib and attached feed',translate=[0,.32,0])
    m.cyl((0,.91,0),.068,.24,'ink',label='inserting-feed-tenon');m.cyl((0,1.025,0),.094,.19,'ink',top=.075);m.cyl((0,.935,0),.105,.035,'metal')
    shape_loft(m,[(-.071,0),(-.055,.12),(0,.30),(.055,.12),(.071,0)],.025,(0,1.085,.015),'metal','sculpted-fountain-nib')
    m.box((0,1.24,.032),(.003,.22,.003),'ink',.0008);front(m,(0,1.15,.033),.012,.005,'ink')
    still(m,'Fitted open pen cap');lathe(m,[(0,.02),(.13,.02),(.145,.07),(.145,.51),(.125,.56),(.105,.54),(.105,.10),(0,.10)],(.30,0,-.05),'accent',label='hollow-pen-cap')
    m.cyl((.30,.08,-.05),.149,.03,'metal');cable(m,[(.30,.52,.095),(.30,.49,.12),(.30,.18,.12),(.30,.16,.095)],.013,'metal')

BUILDERS={'tape-dispenser':tape,'calculator':calculator,'alarm-clock':clock,'sand-timer':sand_timer,'fountain-pen':pen}
