"""Rebuild a specific study without silently re-authoring the entire collection."""
import argparse,json
from build_pack import Model,ROOT,export_glb
from camera_benchmark import create_camera
from refine_collection import refine_collection

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='+');args=parser.parse_args()
    registry=json.loads((ROOT/'source/object_registry.json').read_text());catalog=json.loads((ROOT/'catalog.json').read_text())
    known={a['id'] for a in registry}
    if not set(args.ids)<=known:parser.error('Unknown object ID')
    changed={}
    for a in registry:
        if a['id'] not in args.ids:continue
        m=create_camera(Model) if a['id']=='rangefinder-camera' else Model(a['id'],a['name'],a['category'],a['description'])
        refine_collection([m]);changed[m.slug]=export_glb(m)
    catalog['assets']=[changed.get(a['id'],a) for a in catalog['assets']]
    catalog['stage']='Purposeful interaction studies';catalog['version']='0.7.0'
    (ROOT/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
