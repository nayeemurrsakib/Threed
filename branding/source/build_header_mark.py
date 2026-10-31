"""Build a lighter Soft keys EE mesh for the site's animated header."""
from pathlib import Path
import importlib.util,json,tempfile,sys
ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'site'
sys.path.insert(0,str(SITE/'source'))
spec=importlib.util.spec_from_file_location('ee_studies',ROOT/'branding/3d-studies/smiling-ee/source/build_studies.py')
study=importlib.util.module_from_spec(spec);spec.loader.exec_module(study)
pack=study.pack;config=study.SPECS[0]
m=pack.Model('ee-soft-keys','threed® Soft keys EE','Brand identity','Approved Soft keys direction: paired smiling EE glyphs with warm orange caps, a darker orange edge and ivory bases.')
m.palette={**config['palette'],'secondary':('#d96b32',.72,0),'accent':('#aa4b27',.40,0)};m.presentation={'viewDirection':[.85,.55,6.5],'study':True,'motionFrame':0,'motionLift':0};m.reviewStatus='approved-for-site-integration';m.interaction='A gentle idle smile; hover to lift the lip corners and squint the crescent eyes.'
for i,region in enumerate(study.regions):
    field=study.glyph_field(region,step=9.2)
    m.group={'layer':'Left ee' if i==0 else 'Right ee','explode':[0,0,0],'delay':0,'blast':[0,0,0], 'motion':{'type':'functional','pivot':[-.55 if i==0 else .55,.52,0],'axis':[0,1,0],'angle':0,'wave':{'axis':[0,1,0],'amplitude':0,'frequency':.42,'phase':0}}}
    for depth,bevel,z,slot in config['layers']:
        p,n,idx=study.geometry(field,depth,bevel,z,depth_steps=15);m.mesh(p,n,idx,slot,label=f'{i+1}-{slot}-beveled-glyph')
folder=SITE/'assets/brand'
with tempfile.TemporaryDirectory(dir=folder) as temp:
    pack.ROOT=Path(temp);(pack.ROOT/'models').mkdir();asset=pack.export_glb(m)
    (folder/'ee-soft-keys.glb').write_bytes((pack.ROOT/asset['model']).read_bytes())
asset.update(model='assets/brand/ee-soft-keys.glb',source='branding/source/build_header_mark.py',approvedDirection='Soft keys')
(folder/'ee-soft-keys.json').write_text(json.dumps(asset,indent=2)+'\n')
print(json.dumps({'triangles':asset['triangles'],'bytes':asset['bytes'],'path':asset['model']}))
