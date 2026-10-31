"""Authored, optional exploded-view poses. Never used by ordinary hover motion."""
MAPS={
 'tape-dispenser':{'Weighted enamel base':[0,-.12,0],'Turning tape roll':[-.20,.30,0],'Connected feed span':[0,.25,.08],'Unrolling tape tail':[.12,.32,.08],'Fixed serrated cutter':[.24,.15,.12]},
 'calculator':{'Closed calculator case':[0,-.10,0],'Recessed LCD':[0,.20,0],'Key ':[0,.40,0]},
 'alarm-clock':{'Clock case and legs':[0,0,-.18],'Exposed clock dial':[0,0,.25],'Hour hand':[0,0,.43],'Minute hand':[0,0,.47],'Hand spindle':[0,0,.49],'Fixed bell supports':[0,.20,0],'Left ringing bell':[-.10,.40,0],'Right ringing bell':[.10,.40,0],'Oscillating alarm hammer':[0,.34,.10]},
 'sand-timer':{'Fixed turned frame':[-.33,0,0],'Fitted glass vessel':[0,.08,0],'Draining upper sand':[.30,.16,.06],'Growing lower sand':[.30,.16,.06],'Falling sand stream':[.30,.16,.06],'Falling grain ':[.30,.16,.06]},
 'fountain-pen':{'Open lacquer barrel':[0,-.12,0],'Nib and attached feed':[0,.35,0],'Fitted open pen cap':[.20,.08,0]},
 'over-ear-headphones':{'Connected padded headband':[0,.28,0],'Left connected swiveling cup':[-.25,0,0],'Right connected swiveling cup':[.25,0,0]},
 'game-controller':{'Continuous controller shell':[0,-.08,-.14],'Analog socket ':[0,0,.12],'Tilting stick ':[0,0,.35],'Seated direction pad':[0,.10,.30],'Pressing action button ':[0,.10,.34],'Pressing shoulder trigger ':[0,.30,0],'Status light':[0,.10,.28]},
 'portable-radio':{'Fitted rounded enclosure':[0,0,-.13],'Fitted speaker grille':[-.10,0,.30],'Inset tuner display':[0,.06,.27],'Sliding tuner needle':[0,.06,.34],'Fixed dial collar':[0,0,.32],'Turning tuning dial':[0,0,.52],'Attached carrying handle and antenna socket':[0,.28,0],'Extending antenna':[.08,.35,0],'Attached rubber feet':[0,-.15,0]},
 'web-camera':{'Monitor clip and hinge':[0,-.15,0],'Attached aiming camera head':[0,.12,-.12]},
 'two-slot-toaster':{'Closed enamel toaster':[0,-.10,-.10],'Fitted metal slot deck':[0,.30,0],'Browning dial and lever guide':[.12,.03,.20],'Popping lever':[.18,.12,.10],'Popping toast slice ':[0,.46,0]},
 'shopping-tote':{'Sewn tote and attached handles':[0,-.10,0]},
 'receipt-printer':{'Closed printer enclosure':[0,-.08,-.10],'Feeding printed receipt':[0,.35,.18]},
 'sun-cap':{'Complete sewn cap':[0,.20,0]},
 'little-rocket':{'Engine flame':[0,-.15,0],'Flame core':[0,-.15,0]},
 'payment-terminal':{'Sliding payment card':[0,0,.35]},
 'pocket-notebook':{'Back cover':[0,-.12,0],'Sewn signatures':[0,.08,0],'Open reading page':[0,.16,0],'Cloth spine and binding':[-.15,0,0],'Turning leaf 1':[0,.24,0],'Turning leaf 2':[0,.29,0],'Turning leaf 3':[0,.34,0],'Front cover':[0,.49,0],'Ribbon bookmark':[.12,.08,.10]},
}
MAPS['delivery-parcel']={'Rear hinged top flap':[0,.43,0],'Front hinged top flap':[0,.43,0]}
MAPS['countertop-blender']={'Motor enclosure top':[0,.15,0]}
MAPS['pour-over-kettle']={'Pouring water':[.20,.10,0],'Water drop ':[.20,.10,0]}
MAPS['insulated-bottle']={'Lid and attached carrying loop':[0,.47,0]}
MAPS['little-rocket']['Inset dark porthole']=[0,.08,.48]
MAPS['little-rocket']['Complete lifting rocket']=[0,.08,.48]
MAPS['passport-wallet']=MAPS['pocket-notebook']

def apply(m):
    for p in m.parts:
        if 'blast' in p:continue
        if any(p['explode']):p['blast']=list(p['explode']);p['blastGroup']=p['layer'];continue
        offset=None;role=p['layer'];table=MAPS.get(m.slug,{})
        for prefix,vector in table.items():
            if role==prefix or (prefix.endswith(' ') and role.startswith(prefix)):offset=vector;break
        if m.slug=='portable-radio' and p['name']=='matching-radius-rounded-radio-front':offset=[0,0,.20];role='Fitted front cover'
        if m.slug=='web-camera' and p['layer']=='Attached aiming camera head':
            if p['name']=='fitted-dark-optical-front-window':offset=[0,.12,.20];role='Optical front window'
            elif p['mat'] in ('metal','glass','lens','accent'):offset=[0,.12,.40];role='Optical elements'
        if m.slug=='calculator' and p['name']=='matching-radius-calculator-top-deck':offset=[0,.18,0];role='Fitted top deck'
        if m.slug=='over-ear-headphones' and p['mat'] in ('rubber','fabric'):
            side=-1 if p['layer'].startswith('Left') else 1;offset=[side*.40,-.03,.08];role=p['layer']+' cushion'
        if offset is None:raise ValueError(f'{m.slug}: author optional blast for {p["layer"]} / {p["name"]}')
        p['blast']=list(offset);p['blastGroup']=role
