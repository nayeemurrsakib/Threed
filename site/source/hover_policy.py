"""Collection-wide rule: small functional gestures, never detached assemblies.

Apply to authored geometry before normalization. Any new recipe must opt into an
explicit action here; an unreviewed ID fails rather than inheriting an explosion.
"""
from purposeful_motion import *
from copy import deepcopy

REFINED={'tape-dispenser','calculator','alarm-clock','sand-timer','fountain-pen','over-ear-headphones','game-controller','portable-radio','web-camera','pour-over-kettle','two-slot-toaster','lidded-pot','insulated-bottle','ribbon-gift','delivery-parcel','shopping-tote','receipt-printer','camp-lantern','sun-cap','little-rocket'}

def center(p):return [sum(v[i] for v in p['p'])/len(p['p']) for i in range(3)]

def apply(m):
    s=m.slug
    # A construction group may share metadata between meshes; tune each once.
    for p in m.parts:
        if p.get("motion"):p["motion"]=deepcopy(p["motion"])
    if s in REFINED:
        for p in m.parts:
            p['explode']=[0,0,0];k=p.get('motion')
            if not k:continue
            k['angle']=k.get('angle',0)*.35
            if k.get('translate'):k['translate']=[v*.35 for v in k['translate']]
            if k.get('follow'):k['follow']['angle']*=.35
            if k.get('wave'):
                for key in ('amplitude','lift'):k['wave'][key]=k['wave'].get(key,0)*.6
            if k.get('glow'):k['glow']=[v*.65 for v in k['glow']]
            if s=='delivery-parcel':
                if 'inner flap' in p['layer']:p.pop('motion',None);p['delay']=0
                else:k['angle']=math.copysign(.12,k['angle']) if k['angle'] else 0
            if s=='little-rocket' and k.get('scaleTo'):k['scaleTo']=[7,8,7]
        if s=='insulated-bottle':
            for p in m.parts:
                if p.get('motion'):p['motion']['translate']=[0,.025,0];p['motion']['angle']=-.25
        if s=='fountain-pen':
            moving=[p for p in m.parts if p['layer']!='Fitted open pen cap']
            freeze(m);bind(moving,'Assembled writing pen',(0,.10,0),angle=.025)
            m.interaction='Gently lean the assembled pen as if writing'
            m.description='A complete fountain pen with its nib and feed seated in a hollow barrel, beside its fitted open cap.'
        if s=='delivery-parcel':m.interaction='Gently lift the top flaps; inner flaps and front tape stay fixed'
    elif s in ('pocket-notebook','passport-wallet'):
        for p in m.parts:
            p['explode']=[0,0,0]
            if p.get('motion'):
                p['motion']['angle']*=.15
                if p['motion'].get('page'):p['motion']['page']['bend']*=.3
        m.interaction='Gently lift the cover and flutter the bound pages'
    else:
        freeze(m)
        def move(layers,pivot=(0,0,0),axis=(0,0,1),angle=0,**kw):
            if isinstance(layers,str):layers=[layers]
            bind([p for p in m.parts if p['layer'] in layers], ' / '.join(layers),pivot,axis,angle,**kw)
        def keys(layer,axis,depth):
            for i,p in enumerate([p for p in m.parts if p['layer']==layer]):
                c=center(p);bind([p],f'{layer} {i+1}',wave={'axis':list(axis),'amplitude':depth/2,'lift':-depth/2,'frequency':.65,'phase':c[0]*5+c[2]*6})
        if s=='rangefinder-camera':
            move(['Focus sleeve','Optical glass'],translate=[0,0,.014]);move('Front sculpted cover')
            for p in m.parts:
                if p['name']=='rounded-front-shutter':bind([p],'Shutter press',translate=[0,0,-.006])
            m.interaction='Gently focus the lens and press the shutter'
        elif s=='dome-lamp':move(['Opal diffuser','Light engine'],glow=[1.3,.72,.24]);m.interaction='Warm the lamp light'
        elif s=='task-lamp':move(['Reflector shade','Lamp diffuser'],(.18,1.33,0),angle=.045);m.interaction='Gently aim the lamp shade'
        elif s=='pencil-cup':
            for layer,sign in [('Colored pencil',-1),('Mechanical pencil',1),('Fineliner',-1)]:move(layer,(0,.45,0),angle=sign*.018)
            m.interaction='A small movement of the pencils in their cup'
        elif s=='stapler':move('Sculpted upper lever',(-.56,.30,0),angle=-.025);m.interaction='Gently press the stapler lever'
        elif s=='bookshelf-speaker':
            for p in m.parts:
                if p['name']=='continuous-woofer-cone' or (p['layer']=='Woofer basket' and p['mat']=='rubber'):bind([p],'Vibrating speaker cone',wave={'axis':[0,0,1],'amplitude':.010,'frequency':2.2,'phase':0})
            m.interaction='A gentle bass bounce of the cone and flexible surround'
            m.hint='HOVER FOR A BASS BOUNCE · DRAG TO EXPLORE'
        elif s=='desktop-display':move(['Rear display enclosure','LCD module','Edge frame'],(0,.88,-.1),(1,0,0),-.035);m.interaction='Gently tilt the screen on its hinge'
        elif s=='mechanical-keyboard':keys('Sculpted keycaps',(0,1,0),.012);m.interaction='A gentle wave of key presses'
        elif s=='pocket-console':keys('D-pad and action keys',(0,0,1),.008);m.interaction='Gently press the console controls'
        elif s=='studio-microphone':move(['Microphone body','Condenser capsule','Perforated grille'],(0,1.08,0),(1,0,0),-.04);m.interaction='Gently tilt the microphone in its yoke'
        elif s=='stovetop-brewer':move('Hinged lid',(.40,1.27,0),angle=-.10);m.interaction='Gently lift the hinged brewer lid'
        elif s=='countertop-blender':
            move('Blade assembly',(0,.70,0),(0,1,0),spin=9)
            m.interaction='Spin the blades inside the closed blender'
        elif s=='espresso-cup':move(['Hollow porcelain cup','Coffee and crema'],translate=[0,.018,0]);m.interaction='Slightly lift the cup from its saucer'
        elif s=='citrus-press':move('Fluted reamer',(0,.37,0),(0,1,0),.18);m.interaction='Gently twist the citrus reamer'
        elif s=='kitchen-scale':
            move('Weighing platform',translate=[0,-.028,0],wave={'axis':[0,1,0],'amplitude':.014,'frequency':3,'phase':-pi/2,'decay':4.5})
            m.presentation['restartMotionOnActivate']=True
            for p in m.parts:
                if p['layer']=='Needle and crystal' and p['mat']!='glass':bind([p],'Responding scale needle',(0,.51,.337),angle=-.09)
            m.interaction='The plate dips under weight, softly bounces and settles while the needle responds'
            m.hint='HOVER TO WEIGH · DRAG TO EXPLORE'
        elif s=='pepper-mill':move(['Rounded mill crown','Adjustment screw'],(0,1,0),(0,1,0),.18);m.interaction='A small twist of the grinder crown'
        elif s=='payment-terminal':
            keys('Payment keys',(0,1,0),.012)
            action(m,'Sliding payment card',wave={'axis':[0,0,1],'amplitude':.10,'lift':.11,'frequency':.40,'phase':-pi/2})
            panel(m,(0,.22,.435),(.46,.012,.40),'body',.035,'y','rounded-payment-card')
            m.box((0,.228,.52),(.40,.002,.035),'accent',.0008,label='payment-card-color-band')
            m.box((-.12,.229,.56),(.065,.003,.05),'metal',.001,label='payment-card-chip')
            m.interaction='Slide a card in and out while the keys gently wave'
        elif s=='market-basket':move('Folding handle',(0,.65,0),(1,0,0),.07);m.interaction='Gently pivot the basket handle'
        elif s=='price-tag':bind(m.parts,'Tag with attached cord',(0,1.49,0),angle=.025);m.interaction='A small swing of the hanging tag'
        elif s=='coin-stack':move('Tall stack coin 6',(-.26,.59,0),(0,1,0),.12);m.interaction='Turn the top coin slightly in place'
        elif s=='store-awning':
            # Only the door, its inset glass and knob move together at its hinge.
            door=[p for p in m.parts if p['layer']=='Shopfront glazing' and center(p)[0]>.22]
            bind(door,'Hinged shop door',(.25,.58,.32),(0,1,0),-.09);m.interaction='Gently open the shop door'
        elif s=='piggy-bank':
            for p in m.parts:
                if p['layer']=='Savings slot and coin' and p['mat']=='metal':bind([p],'Coin entering savings slot',translate=[0,-.05,0])
            m.interaction='Nudge a coin into the savings slot'
        elif s=='cabin-suitcase':move('Telescoping handle',translate=[0,.045,0]);m.interaction='Slightly extend the suitcase handle'
        elif s=='weekend-backpack':bind(m.parts,'Complete sewn backpack',(0,1.4,0),angle=.018,translate=[0,.018,0]);m.interaction='Slightly lift the complete backpack'
        elif s=='binoculars':
            for p in m.parts:
                if p['layer']=='Bridge and focus' and center(p)[1]>.55:bind([p],'Focus wheel',(0,.60,0),(0,1,0),.16)
            m.interaction='Turn the focus wheel slightly'
        elif s=='pocket-compass':move('Floating compass needle',(0,.25,0),(0,1,0),.16);m.interaction='The compass needle gently settles'
        elif s=='travel-mug':
            for p in m.parts:
                if p['layer']=='Drinking slide' and p['mat']=='accent':bind([p],'Sliding sip cover',translate=[0,0,-.035])
            m.interaction='Slide the sip cover slightly'
        elif s=='folding-sunglasses':
            for name,sign in [('Left',-1),('Right',1)]:move(name+' folding temple',(sign*.67,.44,0),(0,1,0),sign*.075)
            m.interaction='Gently fold the temples at their hinges'
        elif s=='key-fob':move('House key',(.27,.76,.02),angle=.045);m.interaction='A small swing of the key on its ring'
        elif s=='orbit-sculpture':move(['Outer orbital ring','Inner orbital ring','Orbiting satellites'],(0,.90,0),(0,1,0),.08);m.interaction='Gently turn the connected orbit sculpture'
        elif s in ('stacking-rings','cloud-sculpture','ceramic-rainbow'):
            bind(m.parts,'Complete sculpture',(0,.08,0),(0,1,0),.035);m.interaction='Gently turn the complete sculpture'
        elif s=='rubber-duck':bind(m.parts,'Complete rubber duck',(0,.30,0),angle=.018,wave={'axis':[0,1,0],'amplitude':.006,'frequency':.5,'phase':0});m.interaction='A gentle bob of the whole duck'
        elif s=='tiny-robot':move(['Head assembly','Faceplate','Antenna'],(0,.93,0),(0,1,0),.07);m.interaction='A small curious turn of the robot head'
        elif s=='flower-vase':move(['Stem and leaves','Curved ceramic petals','Flower center'],(0,.65,0),angle=.020,oscillate=.45);m.interaction='A gentle sway of the stem and flower'
        elif s=='wind-up-bird':move('Wind-up key',(-.42,.56,0),(1,0,0),.25);m.interaction='A small turn of the winding key'
        elif s=='balance-mobile':move(['Balancing beam','Sphere counterweight','Ring counterweight'],(0,1.36,0),angle=.025,oscillate=.4);m.interaction='The connected balance beam gently rocks'
        else:raise ValueError(f'{s}: author a small real-use hover action')
    m.presentation.update(explodeYaw=0,motionFrame=0,motionLift=0)
    m.hint='HOVER FOR A LITTLE MOVEMENT · DRAG TO EXPLORE'
