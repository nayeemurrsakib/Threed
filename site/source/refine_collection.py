"""Run the authored collection pass; unknown silhouettes deliberately fail closed."""
from quality_geometry import prepare,finish,STANDARD
import craft_desk,craft_devices,craft_kitchen,craft_commerce,craft_travel,craft_play
import hover_policy,blast_policy
import book_study
import desk_interactions,device_interactions,kitchen_interactions,object_interactions
FUNCTIONAL={**desk_interactions.BUILDERS,**device_interactions.BUILDERS,**kitchen_interactions.BUILDERS,**object_interactions.BUILDERS}

BUILDERS={'Desk':craft_desk.build,'Devices':craft_devices.build,'Kitchen':craft_kitchen.build,
          'Commerce':craft_commerce.build,'Travel':craft_travel.build,'Play':craft_play.build}

def refine_collection(models):
    for i,m in enumerate(models):
        if m.slug=='rangefinder-camera':
            m.qualityStandard=STANDARD;blast_policy.apply(m);hover_policy.apply(m);blast_policy.apply(m);finish(m)
        else:
            prepare(m)
            if m.slug in FUNCTIONAL:FUNCTIONAL[m.slug](m)
            elif m.slug in ('pocket-notebook','passport-wallet'):book_study.build(m)
            else:BUILDERS[m.category](m)
            blast_policy.apply(m)
            hover_policy.apply(m)
            blast_policy.apply(m)
            finish(m)
        print(f'Crafted {i+1:02d}/{len(models)} {m.slug}: {len(m.parts)} parts / {len(set(p["layer"] for p in m.parts))} assemblies',flush=True)
