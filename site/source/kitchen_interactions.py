"""Lids, pouring and toast: functional actions with attached fittings."""
from purposeful_motion import *

def kettle(m):
    from craft_kitchen import build
    build(m);freeze(m)
    presentation(m,'Tilt the kettle and pour from its spout','HOVER TO POUR · DRAG TO EXPLORE',view=[.45,.30,1],frame=.08)
    m.description='A hollow enamel kettle that pours with its handle, spout and fitted lid remaining attached.'
    bind(m.parts,'Intact pouring kettle',(0,.50,0),angle=-.28)
    m.palette['water']=('#a7ccdf',.10,0)
    follow={'pivot':[0,.50,0],'point':[1.08,.95,0],'axis':[0,0,1],'angle':-.28}
    action(m,'Pouring water',(1.08,.95,0),scaleFrom=[.001,.001,.001],scaleTo=[1,1,1],follow=follow,activation=[.25,1])
    lathe(m,[(0,-.37),(.009,-.35),(.012,-.16),(.015,-.015),(0,0)],(1.08,.95,0),'water',label='slender-pouring-water-stream',seg=48)
    for i in range(4):
        action(m,f'Water drop {i+1}',(1.08,.95,0),scaleFrom=[.001,.001,.001],scaleTo=[1,1,1],follow=follow,activation=[.40,1],wave={'axis':[0,1,0],'amplitude':.018,'lift':0,'frequency':2.1,'phase':i*1.3})
        m.ball((1.08,.53-i*.041,0),.012,'water',scale=(.6,1,.6),seg=20,rings=12)

def slot_deck(m,cz):
    outer=outline(1.405,.34,.095,20);inner=outline(1.08,.135,.065,20);N=len(outer);pts=[];idx=[]
    for contour,y in [(inner,.958),(outer,.958),(outer,.938),(inner,.938)]:
        for x,z in contour:pts.append([x,y,z+cz])
    for j in range(4):
        for i in range(N-1):a=j*N+i;b=((j+1)%4)*N+i;idx.extend([a,a+1,b,a+1,b+1,b])
    add_mesh(m,pts,idx,'metal','fitted-slot-deck-with-real-opening',4,N)

def toaster(m):
    presentation(m,'Two slices of toast pop up','HOVER FOR TOAST · DRAG TO EXPLORE',view=[.48,.38,1],frame=.08)
    m.description='A rounded two-slot toaster with real slot openings, a connected lever and two rising slices of toast.'
    m.palette.update(crust=('#b97943',.80,0),crumb=('#ebca8d',.88,0),toast=('#d4a361',.85,0))
    still(m,'Closed enamel toaster');tray(m,(0,.52,0),(1.48,.88,.79),'body',.23,.045,axis='y')
    m.box((0,.095,0),(1.32,.09,.65),'secondary',.04);feet(m,(-.50,.50),(-.23,.23),.032)
    still(m,'Fitted metal slot deck')
    for z in (-.17,.17):slot_deck(m,z)
    still(m,'Browning dial and lever guide');ring(m,(.36,.39,.407),.12,.09,.035,'metal',(pi/2,0,0));front(m,(.36,.39,.43),.09,.03,'accent');m.box((.36,.43,.448),(.008,.045,.004),'ink',.002)
    m.rod((.77,.34,0),(.77,.78,0),.016,'metal')
    action(m,'Popping lever',translate=[0,.145,0]);m.box((.84,.59,0),(.19,.065,.13),'accent',.028)
    contour=[(-.40,-.29),(-.41,.16),(-.44,.23),(-.39,.33),(-.23,.37),(0,.38),(.23,.37),(.39,.33),(.44,.23),(.41,.16),(.40,-.29)]
    for i,z in enumerate((-.17,.17)):
        action(m,f'Popping toast slice {i+1}',translate=[0,.49,0],delay=i*.035)
        shape_loft(m,contour,.082,(0,.56,z),'crust','rounded-bread-crust')
        shape_loft(m,[(x*.89,y*.86) for x,y in contour],.087,(0,.56,z),'crumb','soft-toasted-bread-face')
        for j in range(13):
            x=-.29+(j*37%59)/100;y=.39+(j*19%37)/100
            m.ball((x,y,z+.046),.007+(j%3)*.0015,'toast',scale=(1,.7,.12),seg=12,rings=6,label='subtle-bread-pore')

def pot(m):
    from craft_kitchen import build
    build(m);freeze(m)
    presentation(m,'Lift the fitted lid; handles stay attached','HOVER TO LIFT THE LID · DRAG TO EXPLORE',view=[.43,.40,1],frame=.06)
    bind([p for p in m.parts if p['layer'] in ('Domed lid','Lid knob')],'Lid with attached knob',(0,.67,0),angle=-.045,translate=[0,.34,0])
    m.description='An open enamel cooking pot with fixed side handles, a seated rolled rim and a lifting lid with its knob attached.'

def bottle(m):
    from craft_kitchen import build
    build(m);m.parts=[p for p in m.parts if p['layer']!='Carrying loop'];freeze(m)
    presentation(m,'Unscrew the lid with its carrying loop attached','HOVER TO UNSCREW · DRAG TO EXPLORE',view=[.42,.33,1],frame=.08)
    bind([p for p in m.parts if p['layer']=='Screw lid'],'Lid and attached carrying loop',(0,1.39,0),(0,1,0),-2.3,translate=[0,.35,0])
    action(m,'Lid and attached carrying loop',(0,1.39,0),(0,1,0),-2.3,translate=[0,.35,0])
    m.torus((0,1.44,0),.115,.021,'metal',(-pi/2,0,0),arc=pi,seg=80)
    m.description='A hollow insulated bottle with an unscrewing fitted lid and a complete upward-arched carrying loop.'

BUILDERS={'pour-over-kettle':kettle,'two-slot-toaster':toaster,'lidded-pot':pot,'insulated-bottle':bottle}
