"""Verify the actual GLB study geometry, normals and edge topology."""
from pathlib import Path
import sys,json
import numpy as np
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE.parents[2]/'site/source'))
from render_previews import read_glb
report=[]
for path in sorted((HERE/'models').glob('*.glb')):
    parts,_=read_glb(path);bad=0;collapsed=0;tiny=0
    for pos,norm,idx,*_ in parts:
        assert np.isfinite(pos).all() and np.isfinite(norm).all()
        assert np.max(np.abs(np.linalg.norm(norm,axis=1)-1))<.001
        assert idx.min()>=0 and idx.max()<len(pos)
        area=np.linalg.norm(np.cross(pos[idx[:,1]]-pos[idx[:,0]],pos[idx[:,2]]-pos[idx[:,0]]),axis=1)
        collapsed+=int(np.sum(area==0));tiny+=int(np.sum(area<1e-10))
        edges=np.sort(np.concatenate([idx[:,[0,1]],idx[:,[1,2]],idx[:,[2,0]]]),axis=1)
        _,counts=np.unique(edges,axis=0,return_counts=True);bad+=int(np.sum(counts!=2))
    assert bad==0 and collapsed==0, 'A study must be closed and have no collapsed triangles'
    report.append({'model':path.name,'parts':len(parts),'finiteGeometry':True,'unitNormals':True,'nonManifoldEdges':bad,'collapsedTriangles':collapsed,'nearZeroAreaTriangles':tiny})
(HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
