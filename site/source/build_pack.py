"""Little Things Vol. 01 — original procedural models. Python 3, no geometry dependencies.
Run from any directory. NumPy + Pillow are required only for the preview renderer.
All assets use Y up, metres, floor origin and named editable PBR materials.
"""
import array, json, math, pathlib, struct
from math import sin, cos, pi, sqrt

ROOT = pathlib.Path(__file__).resolve().parents[1]
PALETTE = {
    'body': ('#e8e4d8', .30, 0), 'accent': ('#e66e45', .26, 0),
    'secondary': ('#9ebaaa', .40, 0), 'ink': ('#293330', .37, .08),
    'metal': ('#b4a078', .23, .72), 'lens': ('#17272a', .10, .28),
    'paper': ('#f5eddb', .65, 0), 'rubber': ('#444844', .80, 0),
}
def rgb(h):
    c = [int(h[i:i+2],16)/255 for i in (1,3,5)]
    return [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
def unit(v):
    s = sqrt(sum(x*x for x in v)) or 1
    return [x/s for x in v]
def matrix(rot):
    x,y,z = rot; sx,cx,sy,cy,sz,cz = sin(x),cos(x),sin(y),cos(y),sin(z),cos(z)
    return [[cz*cy,cz*sy*sx-sz*cx,cz*sy*cx+sz*sx],
            [sz*cy,sz*sy*sx+cz*cx,sz*sy*cx-cz*sx],[-sy,cy*sx,cy*cx]]
def trans(v,r): return [sum(r[i][j]*v[j] for j in range(3)) for i in range(3)]

class Model:
    def __init__(self,slug,name,category,description):
        self.slug,self.name,self.category,self.description=slug,name,category,description
        self.parts=[]
        self.group={}
    def mesh(self,p,n,idx,mat='body',pos=(0,0,0),rot=(0,0,0),label=None):
        r=matrix(rot)
        p=[[a+b for a,b in zip(trans(v,r),pos)] for v in p]
        n=[unit(trans(v,r)) for v in n]
        self.parts.append({'p':p,'n':n,'i':idx,'mat':mat,'name':label or f'{mat}-{len(self.parts):02d}',**json.loads(json.dumps(self.group))})
    def ball(self,pos,r,mat='body',scale=(1,1,1),rot=(0,0,0),seg=64,rings=32,label=None):
        p=[]; n=[]; idx=[]
        for j in range(rings+1):
            t=pi*j/rings
            for i in range(seg+1):
                a=2*pi*i/seg; v=[sin(t)*cos(a),cos(t),sin(t)*sin(a)]
                p.append([v[k]*r*scale[k] for k in range(3)])
                n.append(unit([v[k]/scale[k] for k in range(3)]))
        for j in range(rings):
            for i in range(seg):
                a=j*(seg+1)+i; b=a+seg+1
                idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def box(self,pos,size,mat='body',bevel=.08,rot=(0,0,0),label=None):
        # A rounded box: subdivided cube projected to the Minkowski sum of a box and sphere.
        half=[v/2 for v in size]; b=min(bevel,min(half)*.96); inner=[x-b for x in half]
        p=[]; n=[]; idx=[]; steps=8
        for axis in range(3):
            u=(axis+1)%3; v=(axis+2)%3
            for sign in (-1,1):
                start=len(p)
                def coordinates(k):
                    return [-inner[k]-b*i/steps for i in range(steps,-1,-1)]+[0.]+[inner[k]+b*i/steps for i in range(steps+1)]
                us,vs=coordinates(u),coordinates(v); nu,nv=len(us),len(vs)
                for j in range(nv):
                    for i in range(nu):
                        q=[0.,0.,0.]; q[axis]=sign*half[axis]
                        q[u]=us[i]; q[v]=vs[j]
                        near=[max(-inner[k],min(inner[k],q[k])) for k in range(3)]
                        normal=unit([q[k]-near[k] for k in range(3)])
                        p.append([near[k]+b*normal[k] for k in range(3)]); n.append(normal)
                for j in range(nv-1):
                    for i in range(nu-1):
                        a=start+j*nu+i; c=a+nu
                        idx += [a,a+1,c,a+1,c+1,c] if sign>0 else [a,c,a+1,a+1,c,c+1]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def lathe(self,profile,pos=(0,0,0),mat='body',rot=(0,0,0),seg=80,label=None):
        p=[]; n=[]; idx=[]
        for j,(radius,y) in enumerate(profile):
            before=profile[max(0,j-1)]; after=profile[min(len(profile)-1,j+1)]
            dr=after[0]-before[0]; dy=after[1]-before[1]
            for i in range(seg+1):
                a=2*pi*i/seg
                p.append([radius*cos(a),y,radius*sin(a)])
                n.append(unit([dy*cos(a),-dr,dy*sin(a)]))
        for j in range(len(profile)-1):
            for i in range(seg):
                a=j*(seg+1)+i; b=a+seg+1
                idx += [a,b,a+1,a+1,b,b+1]
        self.mesh(p,n,idx,mat,pos,rot,label)
    def cyl(self,pos,r,h,mat='body',rot=(0,0,0),top=None,label=None):
        t=r if top is None else top; b=min(.035,h*.18,r*.18)
        profile=[(0,-h/2),(r-b,-h/2)]
        for i in range(1,9):
            a=pi/2*i/8;profile.append((r-b+b*sin(a),-h/2+b-b*cos(a)))
        if t>0:
            bt=min(b,t*.18);profile.append((t,h/2-bt))
            for i in range(1,9):
                a=pi/2*i/8;profile.append((t-bt+bt*cos(a),h/2-bt+bt*sin(a)))
            profile.append((0,h/2))
        else:profile.append((0,h/2))
        self.lathe(profile,pos,mat,rot,label=label)
    def torus(self,pos,r,t,mat='body',rot=(0,0,0),arc=2*pi,seg=80):
        p=[]; n=[]; idx=[]; radial=20
        for j in range(seg+1):
            a=arc*j/seg
            for i in range(radial+1):
                b=2*pi*i/radial
                p.append([(r+t*cos(b))*cos(a),t*sin(b),(r+t*cos(b))*sin(a)])
                n.append([cos(b)*cos(a),sin(b),cos(b)*sin(a)])
        for j in range(seg):
            for i in range(radial):
                a=j*(radial+1)+i; b=a+radial+1
                idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat,pos,rot)
    def rod(self,a,b,r,mat='metal'):
        d=[b[i]-a[i] for i in range(3)]; length=sqrt(sum(v*v for v in d))
        # Rotating a Y-axis cylinder with Rz * Rx.
        rot=(math.atan2(d[2],sqrt(d[0]**2+d[1]**2)),0,-math.atan2(d[0],d[1]))
        self.cyl(tuple((a[i]+b[i])/2 for i in range(3)),r,length,mat,rot)
    def tube(self,points,r,mat='body'):
        # Parallel local frame, open ends; enough for stylized handles and cables.
        p=[]; n=[]; idx=[]; sides=24
        for j,point in enumerate(points):
            a=points[max(0,j-1)]; b=points[min(len(points)-1,j+1)]
            tangent=unit([b[k]-a[k] for k in range(3)])
            ref=[0,0,1] if abs(tangent[2])<.9 else [0,1,0]
            u=unit([tangent[1]*ref[2]-tangent[2]*ref[1],tangent[2]*ref[0]-tangent[0]*ref[2],tangent[0]*ref[1]-tangent[1]*ref[0]])
            v=[tangent[1]*u[2]-tangent[2]*u[1],tangent[2]*u[0]-tangent[0]*u[2],tangent[0]*u[1]-tangent[1]*u[0]]
            for i in range(sides+1):
                a=2*pi*i/sides; normal=[u[k]*cos(a)+v[k]*sin(a) for k in range(3)]
                p.append([point[k]+r*normal[k] for k in range(3)]); n.append(normal)
        for j in range(len(points)-1):
            for i in range(sides):
                a=j*(sides+1)+i; b=a+sides+1; idx += [a,a+1,b,a+1,b+1,b]
        self.mesh(p,n,idx,mat)
    def grille(self,origin,columns,rows,pitch,hole,mat='body'):
        """A real perforated sheet: square cells with circular openings and recessed hole walls."""
        p=[];n=[];idx=[];segments=24;thickness=.018
        for row in range(rows):
            for col in range(columns):
                cx=origin[0]+col*pitch;cy=origin[1]+row*pitch;z=origin[2];start=len(p)
                for i in range(segments+1):
                    a=2*pi*i/segments;c,s=cos(a),sin(a);outer=pitch*.5/max(abs(c),abs(s))
                    p.extend([[cx+outer*c,cy+outer*s,z],[cx+hole*c,cy+hole*s,z],[cx+hole*c,cy+hole*s,z-thickness]])
                    n.extend([[0,0,1],[0,0,1],[-c,-s,0]])
                for i in range(segments):
                    a=start+i*3;b=a+3
                    idx.extend([a,b,a+1,a+1,b,b+1,a+1,b+1,a+2,a+2,b+1,b+2])
        self.mesh(p,n,idx,mat,label='perforated-speaker-sheet')
    def knurl(self,pos,r,h,mat='metal',ridges=48):
        p=[];n=[];idx=[];seg=ridges*2
        for j,y in enumerate((-h/2,h/2)):
            for i in range(seg+1):
                a=2*pi*i/seg;radius=r-(.003 if i%2 else 0)
                p.append([radius*cos(a),y,radius*sin(a)]);n.append([cos(a),0,sin(a)])
        for i in range(seg):a=i;b=i+seg+1;idx.extend([a,b,a+1,a+1,b,b+1])
        self.mesh(p,n,idx,mat,pos,label='fine-knurled-edge')
        self.cyl(pos,r-.003,h*.94,mat)
    def normalize(self):
        verts=[p for part in self.parts for p in part['p']]
        lo=[min(v[k] for v in verts) for k in range(3)]; hi=[max(v[k] for v in verts) for k in range(3)]
        factor=2/max(hi[k]-lo[k] for k in range(3)); center=[(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2]
        for part in self.parts:
            part['p']=[[(v[k]-center[k])*factor for k in range(3)] for v in part['p']]
            if part.get('motion'):
                motion=json.loads(json.dumps(part['motion']))
                motion['pivot']=[(motion['pivot'][k]-center[k])*factor for k in range(3)]
                if motion.get('translate'):motion['translate']=[v*factor for v in motion['translate']]
                if motion.get('wave'):
                    for key in ('amplitude','lift'):motion['wave'][key]=motion['wave'].get(key,0)*factor
                if motion.get('clipY') is not None:motion['clipY']=(motion['clipY']-center[1])*factor
                if motion.get('follow'):
                    for key in ('pivot','point'):motion['follow'][key]=[(motion['follow'][key][k]-center[k])*factor for k in range(3)]
                if motion.get('page'):
                    motion['page']['width']*=factor;motion['page']['bend']*=factor
                part['motion']=motion
        return [round((hi[k]-lo[k])*factor,4) for k in range(3)]

def export_glb(m):
    bounds=m.normalize(); blob=bytearray(); views=[]; access=[]; meshes=[]; nodes=[]
    def accessor(values,kind,component,target,count,minmax=False):
        while len(blob)%4: blob.append(0)
        offset=len(blob); data=array.array('f' if component==5126 else 'I',values)
        import sys
        if sys.byteorder!='little': data.byteswap()
        blob.extend(data.tobytes()); vi=len(views)
        views.append({'buffer':0,'byteOffset':offset,'byteLength':len(data)*data.itemsize,'target':target})
        a={'bufferView':vi,'componentType':component,'count':count,'type':kind}
        if minmax:
            a['min']=[min(values[k::3]) for k in range(3)]; a['max']=[max(values[k::3]) for k in range(3)]
        access.append(a); return len(access)-1
    palette={**PALETTE,**getattr(m,'palette',{})};slots=[slot for slot in palette if any(p['mat']==slot for p in m.parts)]
    def explosion(part,index):
        if not all(k in part for k in ('explode','layer','delay')):
            raise ValueError(f'{m.slug}: part {index} is missing authored assembly metadata')
        return part['explode'],part['layer']
    for part_index,part in enumerate(m.parts):
        pa=accessor([v for p in part['p'] for v in p],'VEC3',5126,34962,len(part['p']),True)
        na=accessor([v for p in part['n'] for v in p],'VEC3',5126,34962,len(part['n']))
        ia=accessor(part['i'],'SCALAR',5125,34963,len(part['i']))
        offset,layer=explosion(part,part_index)
        metadata={'explosionOffset':offset,'layer':layer,'delay':part.get('delay',0)}
        if part.get('motion'):metadata['motion']=part['motion']
        metadata['blastOffset']=part['blast'];metadata['blastGroup']=part.get('blastGroup',part['layer'])
        meshes.append({'name':part['name'],'extras':metadata,'primitives':[{'attributes':{'POSITION':pa,'NORMAL':na},'indices':ia,'material':slots.index(part['mat'])}]})
        nodes.append({'name':part['name'],'mesh':len(meshes)-1})
    materials=[]
    for slot in slots:
        h,rough,metal=palette[slot]
        alpha=getattr(m,'alpha',{}).get(slot,1)
        material={'name':slot,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':rgb(h)+[alpha],'roughnessFactor':rough,'metallicFactor':metal}}
        if alpha<1:material['alphaMode']='BLEND'
        materials.append(material)
    doc={'asset':{'version':'2.0','generator':'threed original geometry studio / 0.7.0','copyright':'Original asset recipes supplied in source/build_pack.py'},
         'scene':0,'scenes':[{'name':m.name,'nodes':list(range(len(nodes)))}],'nodes':nodes,'meshes':meshes,'materials':materials,
         'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':access,
         'extras':{'category':m.category,'description':m.description,'materialSlots':slots,'units':'metres','upAxis':'Y','floorOrigin':True,'presentation':getattr(m,'presentation',{}),'qualityStandard':getattr(m,'qualityStandard',None),'interaction':getattr(m,'interaction','Explore the assembly')}}
    js=json.dumps(doc,separators=(',',':')).encode(); js+=b' '*((-len(js))%4); blob+=b'\0'*((-len(blob))%4)
    out=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(blob))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(blob),0x004E4942)+blob
    path=ROOT/'models'/f'{m.slug}.glb'; path.write_bytes(out)
    return {'id':m.slug,'name':m.name,'category':m.category,'description':m.description,'model':f'models/{m.slug}.glb',
            'thumbnail':f'previews/{m.slug}.png','dimensions':bounds,'triangles':sum(len(p['i'])//3 for p in m.parts),
            'vertices':sum(len(p['p']) for p in m.parts),'parts':len(m.parts),'bytes':len(out),'materialSlots':sorted(set(p['mat'] for p in m.parts)),
            'preferredPalette':getattr(m,'preferredPalette',None),'study':getattr(m,'study',None),
            'qualityStandard':getattr(m,'qualityStandard',None),'assemblies':list(dict.fromkeys(p['layer'] for p in m.parts)),
            'interaction':getattr(m,'interaction','Explore the assembly'),'hint':getattr(m,'hint',None),'reviewStatus':getattr(m,'reviewStatus','approved-benchmark' if m.slug=='rangefinder-camera' else 'collection-study')}

def main():
    for folder in ('models','previews','presets'): (ROOT/folder).mkdir(exist_ok=True)
    from camera_benchmark import create_camera
    from refine_collection import refine_collection
    registry=json.loads((ROOT/'source/object_registry.json').read_text())
    models=[create_camera(Model) if a['id']=='rangefinder-camera' else Model(a['id'],a['name'],a['category'],a['description']) for a in registry]
    refine_collection(models)
    assets=[export_glb(m) for m in models]
    manifest={'name':'threed®','volume':'01','version':'0.7.0','stage':'Individual craft studies','assetCount':len(assets),
              'categories':list(dict.fromkeys(a['category'] for a in assets)),'defaultPalette':{k:v[0] for k,v in PALETTE.items()},'assets':assets}
    (ROOT/'catalog.json').write_text(json.dumps(manifest,indent=2))
    palettes={
      'Workshop':{k:v[0] for k,v in PALETTE.items()},
      'Cobalt':{'body':'#f5f5f1','accent':'#a4b3dd','secondary':'#bcc8e9','ink':'#191d24','metal':'#b8bdc3','lens':'#102128','paper':'#eff1ed','rubber':'#25282d'},
      'Cherry':{'body':'#efddd2','accent':'#a82e40','secondary':'#d17b81','ink':'#392c31','metal':'#b79b75','lens':'#2c1926','paper':'#faebdf','rubber':'#4f373b'},
      'Butter':{'body':'#f3e5ba','accent':'#e3a53c','secondary':'#a6b695','ink':'#3a4135','metal':'#b99a62','lens':'#23352c','paper':'#fbf4de','rubber':'#4d5344'},
      'Lilac':{'body':'#e9e4f1','accent':'#8664b0','secondary':'#b3a7c4','ink':'#343044','metal':'#b8a8a0','lens':'#251f38','paper':'#f3ecf5','rubber':'#4b4359'},
      'Graphite':{'body':'#a7aaa7','accent':'#4b5854','secondary':'#d5d6cf','ink':'#252c29','metal':'#9b9f98','lens':'#1b2421','paper':'#ecece5','rubber':'#3c443f'}}
    textile_colors={'Workshop':('#9ebaaa','#6d887b'),'Cobalt':('#a4b3dd','#8f9fba'),'Cherry':('#d17b81','#a82e40'),'Butter':('#a6b695','#b99a62'),'Lilac':('#b3a7c4','#8664b0'),'Graphite':('#4b5854','#4b5854')}
    for name,(fabric,leather) in textile_colors.items():palettes[name].update(fabric=fabric,leather=leather)
    (ROOT/'presets/palettes.json').write_text(json.dumps(palettes,indent=2))
    lighting={'Softbox':{'azimuth':-40,'elevation':48,'intensity':3.0,'fill':.65,'warmth':.15,'shadow':.55,'softness':2.5},
              'Daylight':{'azimuth':-65,'elevation':60,'intensity':3.5,'fill':.85,'warmth':-.18,'shadow':.35,'softness':3.0},
              'Golden hour':{'azimuth':-75,'elevation':23,'intensity':3.7,'fill':.35,'warmth':.8,'shadow':.7,'softness':1.2},
              'Gallery':{'azimuth':30,'elevation':65,'intensity':3.8,'fill':.3,'warmth':0,'shadow':.65,'softness':1.8},
              'Product studio':{'azimuth':-45,'elevation':50,'intensity':5.2,'fill':.32,'warmth':-.05,'shadow':.72,'softness':3.6}}
    (ROOT/'presets/lighting.json').write_text(json.dumps(lighting,indent=2))
    print(f'Built {len(assets)} original assets / {sum(a["triangles"] for a in assets):,} triangles / {sum(a["bytes"] for a in assets)/1e6:.1f} MB')
    return models

if __name__=='__main__': main()
