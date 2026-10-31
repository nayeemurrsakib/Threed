"""Sculptural pieces with continuous skins and object-specific layer motion."""
from quality_geometry import *

def build(m):
    s=m.slug
    if s=='orbit-sculpture':
        group(m,'Turned ceramic plinth',[0,-.17,0]);lathe(m,[(0,.025),(.29,.025),(.36,.06),(.35,.13),(.28,.17),(0,.17)],mat='body');m.cyl((0,.42,0),.018,.54,'metal')
        group(m,'Outer orbital ring',[-.13,.14,-.10],.05);m.torus((0,.90,0),.56,.022,'metal',(pi/2,.3,.2),seg=128)
        group(m,'Inner orbital ring',[.13,.29,.10],.10);m.torus((0,.90,0),.44,.018,'secondary',(.55,0,-.6),seg=128)
        group(m,'Polished central sphere',[0,.46,.08],.14);m.ball((0,.90,0),.23,'accent',seg=112,rings=56)
        group(m,'Orbiting satellites',[.19,.20,.19],.08);m.ball((-.49,1.13,.12),.075,'body');m.ball((.43,.62,.08),.055,'metal')
    elif s=='stacking-rings':
        group(m,'Rounded wooden base',[0,-.16,0]);lathe(m,[(0,.03),(.42,.03),(.49,.065),(.49,.12),(.43,.16),(0,.16)],mat='body')
        group(m,'Central spindle',[0,.05,0],.025);m.cyl((0,.55,0),.055,.80,'body',top=.035);m.ball((0,.95,0),.037,'body')
        for i,(r,y,mat) in enumerate([(.37,.24,'secondary'),(.31,.406,'accent'),(.25,.572,'body'),(.19,.738,'secondary')]):
            group(m,f'Stacking ring {i+1}',[(i-1.5)*.07,.16+i*.14,0],.03+i*.035)
            major=(r+.075)/2;minor=(r-.075)/2
            profile=[(major+minor*cos(2*pi*j/64),.083*sin(2*pi*j/64)) for j in range(65)]
            m.lathe(profile,(0,y,0),mat,seg=112,label=f'soft-rounded-stacking-ring-{i+1}')
        group(m,'Rounded top bead',[0,.84,0],.18);m.ball((0,.886,0),.10,'accent',scale=(1,.7,1))
    elif s=='little-rocket':
        group(m,'Continuous rocket fuselage',[0,.03,0]);lathe(m,[(.16,.24),(.24,.29),(.29,.51),(.29,.99),(.25,1.24),(.17,1.43),(0,1.60),(0,1.56),(.13,1.40),(.21,1.22),(.25,.98),(.25,.51),(.20,.33),(.16,.30),(.16,.24)],mat='body',seg=144,steps=7)
        group(m,'Nose cap',[0,.47,0],.11);lathe(m,[(0,1.60),(.14,1.45),(.21,1.31),(.22,1.28),(.19,1.27),(.11,1.43),(0,1.57)],mat='accent',seg=128)
        group(m,'Engine bell',[0,-.28,0],.035);lathe(m,[(.10,.32),(.12,.24),(.19,.12),(.20,.10),(.17,.09),(.13,.15),(.08,.28),(.10,.32)],mat='metal')
        group(m,'Landing fins',[.18,-.04,0],.055)
        for i in range(3):
            before=len(m.parts);shape_loft(m,[(-.03,.0),(.07,.35),(.20,.43),(.36,.10),(.34,-.16),(.23,-.14)],.065,(.20,.23,0),'secondary','soft-sculpted-landing-fin')
            a=2*pi*i/3;c,sn=cos(a),sin(a)
            for p in m.parts[before:]:p['p']=[[v[0]*c+v[2]*sn,v[1],-v[0]*sn+v[2]*c] for v in p['p']];p['n']=[[v[0]*c+v[2]*sn,v[1],-v[0]*sn+v[2]*c] for v in p['n']]
        optical(m,(0,.98,.275),.13,(0,.08,.48),'Porthole assembly')
        group(m,'Porthole fasteners',[0,.08,.48],.10)
        for i in range(6):
            a=i*pi/3;front(m,(.113*cos(a),.98+.113*sin(a),.31),.008,.006,'metal')
    elif s=='rubber-duck':
        m.palette['body']=('#f5f5f1',.44,0);m.palette['accent']=('#a4b3dd',.42,0)
        group(m,'Continuous soft duck body',[0,-.06,0]);organic(m,[((-.13,.43,0),(.54,.35,.35)),((.24,.68,0),(.25,.36,.24)),((.36,.96,0),(.28,.26,.26)),((-.48,.54,0),(.24,.14,.19))],'body','seamless-body-neck-and-head')
        group(m,'Molded bill',[.25,.02,.04],.065);m.ball((.59,.89,0),.18,'accent',scale=(1,.30,.77),seg=96,rings=32)
        for z in (-.24,.24):
            group(m,('Near' if z>0 else 'Far')+' eye inlay',[.06,.15,z*.65],.11);m.ball((.43,1.03,z),.023,'ink',seg=32,rings=16)
        group(m,'Wing panels',[-.08,.12,.23],.085)
        for z in (-.31,.31):m.ball((-.15,.48,z),.23,'secondary',scale=(1.3,.60,.15),rot=(0,0,.15))
        group(m,'Underside plug',[0,-.24,0],.035);m.cyl((-.10,.13,0),.075,.025,'rubber')
    elif s=='tiny-robot':
        group(m,'Lower chassis',[0,-.12,0]);m.box((0,.62,0),(.62,.61,.43),'secondary',.14)
        for x in (-.21,.21):m.box((x,.16,.055),(.27,.23,.39),'ink',.09);m.cyl((x,.32,0),.06,.19,'metal')
        group(m,'Chest cover',[0,.06,.32],.05);tray(m,(0,.63,.24),(.54,.48,.08),'body',.10,.02,flip=True);m.box((0,.64,.29),(.21,.13,.025),'accent',.035)
        group(m,'Head assembly',[0,.44,0],.12);tray(m,(0,1.18,0),(.78,.57,.45),'body',.16,.03)
        group(m,'Faceplate',[0,.44,.37],.16);m.box((0,1.18,.245),(.63,.35,.035),'ink',.11)
        for x in (-.16,.16):front(m,(x,1.21,.27),.044,.014,'secondary');m.ball((x-.009,1.224,.28),.009,'paper',seg=16,rings=8)
        m.box((0,1.08,.27),(.10,.015,.012),'metal',.006)
        group(m,'Articulated arms',[.23,.15,0],.08)
        for sign in (-1,1):m.ball((sign*.36,.83,0),.07,'metal');m.rod((sign*.36,.83,0),(sign*.47,.52,0),.032,'metal');m.ball((sign*.48,.46,0),.09,'accent')
        group(m,'Antenna',[0,.70,0],.20);m.cyl((0,1.52,0),.012,.15,'metal');m.ball((0,1.61,0),.042,'accent')
    elif s=='cloud-sculpture':
        group(m,'Continuous glazed cloud',[0,.12,0],.055)
        organic(m,[((-.48,.37,0),(.30,.29,.23)),((-.13,.58,0),(.39,.40,.27)),((.31,.45,0),(.35,.34,.24)),((.59,.31,0),(.23,.20,.18)),((0,.25,0),(.56,.18,.22))],'body','single-skin-soft-cloud',128,72)
        group(m,'Hidden mounting pins',[0,-.18,0],.025)
        for x in (-.27,.27):m.cyl((x,.12,0),.018,.16,'metal')
        group(m,'Display plinth',[0,-.32,0]);m.box((0,.035,0),(.83,.07,.34),'secondary',.034)
    elif s=='ceramic-rainbow':
        group(m,'Rounded stone plinth',[0,-.14,0]);m.box((0,.055,0),(1.48,.10,.40),'body',.048)
        for i,(r,mat) in enumerate([(.61,'accent'),(.43,'body'),(.25,'secondary')]):
            group(m,f'Glazed arch {i+1}',[(i-1)*.12,.18+i*.17,0],.035+i*.045)
            # The dense sweep has continuous rounded cross sections at every bend.
            m.tube([(r*cos(pi*j/96),.12+r*sin(pi*j/96),0) for j in range(97)],.073,mat)
            for x in (-r,r):m.ball((x,.12,0),.073,mat,scale=(1,.15,1),seg=40,rings=12)
    elif s=='flower-vase':
        group(m,'Hollow glazed bud vase',[0,-.10,0]);lathe(m,[(0,.025),(.20,.025),(.33,.10),(.38,.28),(.34,.46),(.22,.60),(.12,.70),(.115,.85),(.095,.87),(.074,.85),(.08,.69),(.19,.57),(.30,.43),(.33,.28),(.28,.13),(0,.09)],mat='secondary',seg=144,steps=7)
        group(m,'Stem and leaves',[0,.21,0],.05);cable(m,[(0,.61,0),(.02,.90,0),(.06,1.18,0),(.05,1.49,0)],.012,'metal')
        for sign,y in [(-1,1.00),(1,1.18)]:m.ball((sign*.10,y,0),.13,'secondary',scale=(1,.28,.20),rot=(0,0,sign*.40))
        group(m,'Curved ceramic petals',[0,.48,0],.11)
        for i in range(5):
            a=2*pi*i/5;m.ball((.05+.18*sin(a),1.49+.18*cos(a),0),.14,'accent',scale=(.79,1,.28),rot=(0,0,-a),seg=80,rings=40)
        group(m,'Flower center',[0,.53,.24],.15);m.ball((.05,1.49,.055),.085,'metal',scale=(1,1,.38),seg=80,rings=40)
    elif s=='wind-up-bird':
        group(m,'Seamless glazed bird',[0,-.04,0]);organic(m,[((-.12,.58,0),(.46,.30,.28)),((.26,.85,0),(.23,.29,.22)),((.37,1.02,0),(.24,.22,.21)),((-.46,.69,0),(.25,.12,.15))],'secondary','continuous-bird-body-and-neck')
        group(m,'Beak and eyes',[.20,.13,0],.08);m.ball((.59,.99,0),.12,'accent',scale=(1,.38,.44))
        for z in (-.19,.19):m.ball((.43,1.07,z),.018,'ink',seg=24,rings=12)
        group(m,'Sculpted wings',[0,.10,.22],.055)
        for z in (-.25,.25):m.ball((-.10,.63,z),.22,'body',scale=(1.25,.65,.17),rot=(0,0,-.15))
        group(m,'Mechanical feet',[0,-.20,0],.035)
        for z in (-.15,.15):m.rod((0,.40,z),(0,.12,z),.016,'metal');m.box((.065,.08,z),(.25,.045,.10),'metal',.022)
        group(m,'Wind-up key',[-.28,.05,-.05],.11);m.rod((-.42,.56,0),(-.61,.56,0),.018,'metal');m.torus((-.65,.56,0),.085,.018,'metal',(pi/2,0,0));m.torus((-.65,.70,0),.065,.018,'metal',(pi/2,0,0))
    elif s=='balance-mobile':
        group(m,'Sculpted ceramic base',[0,-.15,0]);lathe(m,[(0,.025),(.28,.025),(.36,.06),(.35,.12),(.27,.16),(0,.16)],mat='body')
        group(m,'Fulcrum',[0,.12,0],.04);m.cyl((0,.75,0),.021,1.18,'metal');m.ball((0,1.36,0),.045,'metal')
        group(m,'Balancing beam',[0,.35,0],.09);m.rod((-.63,1.49,0),(.69,1.23,0),.016,'metal')
        group(m,'Sphere counterweight',[-.13,.18,0],.12);m.rod((-.63,1.49,0),(-.63,.95,0),.010,'metal');m.ball((-.63,.80,0),.17,'accent',seg=96,rings=48)
        group(m,'Ring counterweight',[.13,.18,0],.15);m.rod((.69,1.23,0),(.69,.73,0),.010,'metal');m.torus((.69,.57,0),.16,.040,'secondary',(pi/2,0,0),seg=112)
    else:raise KeyError(s)
