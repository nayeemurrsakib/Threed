"""Check GLB structure, mesh data, uniqueness, PNG transparency and catalog completeness."""
import array, hashlib, json, math, pathlib, struct
ROOT=pathlib.Path(__file__).resolve().parents[1]

def validate_model(path):
    data=path.read_bytes(); magic,version,total=struct.unpack_from('<III',data)
    assert magic==0x46546c67 and version==2 and total==len(data),path
    jl,jt=struct.unpack_from('<II',data,12);assert jt==0x4e4f534a and jl%4==0
    doc=json.loads(data[20:20+jl]); bl,bt=struct.unpack_from('<II',data,20+jl)
    assert bt==0x004e4942 and 28+jl+bl==len(data)
    binary=data[28+jl:];assert doc['buffers'][0]['byteLength']<=len(binary)
    def acc(index):
        a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
        width={'VEC3':3,'SCALAR':1}[a['type']];t={5126:'f',5125:'I',5123:'H'}[a['componentType']]
        offset=v.get('byteOffset',0)+a.get('byteOffset',0);size=struct.calcsize(t)*a['count']*width
        assert offset%struct.calcsize(t)==0 and size<=v['byteLength'] and offset+size<=len(binary)
        out=array.array(t);out.frombytes(binary[offset:offset+size]);return a,out
    triangles=0;bounds=[[],[],[]]
    for mesh in doc['meshes']:
        metadata=mesh.get('extras',{});offset=metadata.get('explosionOffset')
        assert offset is not None and len(offset)==3 and all(v==0 for v in offset) and metadata.get('layer'),'Only assembled functional hover motion is allowed'
        assert metadata['layer'] not in ('Upper parts','Lower parts','Detail parts','Main body','Object assembly'),'Generic assembly fallback is forbidden'
        assert math.isfinite(metadata.get('delay',-1)) and 0<=metadata['delay']<=.30
        if metadata.get('motion'):
            motion=metadata['motion'];assert motion['type'] in ('hinge','functional')
            assert len(motion['pivot'])==len(motion['axis'])==3
            assert all(math.isfinite(v) for v in motion['pivot']+motion['axis'])
            assert abs(sum(v*v for v in motion['axis'])-1)<1e-6 and abs(motion['angle'])<=math.pi
            if motion.get('page'):assert 0<motion['page']['bend']<motion['page']['width']*.5
            for key in ('scaleFrom','scaleTo'):
                if key in motion:assert len(motion[key])==3 and all(math.isfinite(v) and v>0 for v in motion[key])
            if motion.get('translate'):assert len(motion['translate'])==3 and all(math.isfinite(v) for v in motion['translate'])
            if motion.get('timeline'):assert motion['timeline']>0
        for p in mesh['primitives']:
            a,pos=acc(p['attributes']['POSITION']);n,norm=acc(p['attributes']['NORMAL']);_,idx=acc(p['indices'])
            assert a['count']==n['count'] and len(idx)%3==0 and max(idx)<a['count']
            assert all(math.isfinite(x) for x in pos) and all(math.isfinite(x) for x in norm)
            for k in range(0,len(norm),3): assert abs(sum(x*x for x in norm[k:k+3])-1)<.001
            for k in range(3):
                values=pos[k::3];assert abs(min(values)-a['min'][k])<1e-5 and abs(max(values)-a['max'][k])<1e-5
                bounds[k].extend(values)
            material=doc['materials'][p['material']];assert material['name']
            m=material['pbrMetallicRoughness'];assert all(0<=v<=1 for v in m['baseColorFactor'])
            assert 0<=m['roughnessFactor']<=1 and 0<=m['metallicFactor']<=1
            if m['baseColorFactor'][3]<1:assert material.get('alphaMode')=='BLEND'
            triangles+=len(idx)//3
    assert abs(min(bounds[1]))<1e-5,'Object should sit on the floor'
    assert abs(max(max(v)-min(v) for v in bounds)-2)<1e-4,'Presentation scale should be normalized'
    assert doc['extras'].get('qualityStandard')=='camera-craft-v1'
    groups={}
    for mesh in doc['meshes']:
        e=mesh['extras'];motion=(e['explosionOffset'],e['delay'],e.get('motion'))
        if e['layer'] in groups:assert groups[e['layer']]==motion,'Attached assembly parts must move together'
        groups[e['layer']]=motion
    assert groups,'An object needs an authored motion grouping, not an arbitrary minimum part count'
    return triangles,hashlib.sha256(data).hexdigest()

def main():
    catalog=json.loads((ROOT/'catalog.json').read_text());assets=catalog['assets'];hashes=set();total=0
    registry=json.loads((ROOT/'source/object_registry.json').read_text());count=len(registry)
    assert len(assets)==catalog['assetCount']==count and len(set(a['id'] for a in assets))==count
    assert {a['id'] for a in assets}=={a['id'] for a in registry}
    evidence=json.loads((ROOT/'refinement/review-v05/evidence.json').read_text())
    for asset in assets:
        path=ROOT/asset['model'];tri,hash=validate_model(path);assert tri==asset['triangles'];assert hash not in hashes;hashes.add(hash);total+=tri
        assert asset['qualityStandard']=='camera-craft-v1' and asset['assemblies']
        assert evidence[asset['id']]['sha256']==hash,'Review evidence is stale; regenerate and inspect the review board'
        assert (ROOT/evidence[asset['id']]['board']).exists()
        for path,size,alpha in [(ROOT/asset['thumbnail'],256,False),(ROOT/'renders'/f'{asset["id"]}.png',1024,True)]:
            data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';w,h,depth,color=struct.unpack_from('>IIBB',data,16)
            assert w==h==size and depth==8 and (not alpha or color==6)
    assert len(list((ROOT/'models').glob('*.glb')))==count
    assert len(list((ROOT/'renders').glob('*.png')))==count
    report={'models':count,'uniqueModels':len(hashes),'triangles':total,'transparentPngs':count,'pngResolution':'1024x1024','qualityStandard':'camera-craft-v1','authoredAssemblies':sum(len(a['assemblies']) for a in assets),'currentReviewBoards':len(catalog['categories']),'categories':{c:sum(a['category']==c for a in assets) for c in catalog['categories']},'checks':'GLB headers, chunks, accessor bounds/alignment, finite positions, unit normals, valid indices/materials, floor origins, presentation scale, unique hashes, PNG dimensions and alpha channel, authored assembly timing and consistent offsets, standard metadata, current review-board hashes'}
    (ROOT/'reports/validation/VALIDATION.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
