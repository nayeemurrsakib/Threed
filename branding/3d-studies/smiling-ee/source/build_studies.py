"""Actual beveled 3D EE glyphs from the supplied smiling logo. No raster billboards.
SDF contour distance + rounded extrusion + marching tetrahedra; NumPy/Pillow only.
"""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'site/source'))
sys.path.insert(0,str(ROOT/'branding/source'))
import build_pack as pack
from vector_geometry import contours
from render_previews import render,font
import render_previews
pack.ROOT=HERE;render_previews.ROOT=HERE
(HERE/'models').mkdir(exist_ok=True);(HERE/'renders').mkdir(exist_ok=True)
original=np.asarray(Image.open(ROOT/'branding/explorations/selected-b-happy/threed-smiling-v2.png').convert('RGB')).mean(axis=2)<100
# The paired glyphs occupy this source region, with the original center gap intact.
regions=[(835,275,1105,565),(1107,275,1382,565)]


def glyph_field(region,step=4.6):
    x0,y0,x1,y1=region;mask=original[y0:y1,x0:x1]
    # Grid coordinates are in source pixels so all counters follow the supplied logo.
    px=np.arange(-8,x1-x0+9,step);py=np.arange(-8,y1-y0+9,step)
    xx,yy=np.meshgrid(px,py,indexing='xy');grid=np.stack([xx.ravel(),yy.ravel()],axis=1)
    points=np.concatenate([np.asarray(p) for p in contours(mask)])
    distance=np.full(len(grid),np.inf)
    for start in range(0,len(points),256):
        delta=grid[:,None,:]-points[None,start:start+256,:]
        distance=np.minimum(distance,np.min(np.sum(delta*delta,axis=2),axis=1))
    ix=np.clip(np.rint(xx).astype(int),0,mask.shape[1]-1);iy=np.clip(np.rint(yy).astype(int),0,mask.shape[0]-1)
    inside=mask[iy,ix]&(xx>=0)&(yy>=0)&(xx<mask.shape[1])&(yy<mask.shape[0])
    distance=np.sqrt(distance).reshape(xx.shape)*np.where(inside,-1,1)
    # Keep the entire EE identity 2.2 units wide before the common normalization.
    scale=2.2/(1382-835)
    x=(px+x0-(835+1382)/2)*scale
    y=(565-(py+y0))*scale
    return x,y,distance*scale

FIELDS=[glyph_field(r) for r in regions]
CORNERS=np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0],[0,0,1],[0,1,1],[1,1,1],[1,0,1]])
TETS=[[0,1,2,6],[0,2,3,6],[0,3,7,6],[0,7,4,6],[0,4,5,6],[0,5,1,6]]


def geometry(field,depth,bevel,zshift=0,depth_steps=23):
    x,y,d=field;z=np.linspace(-depth/2-.025,depth/2+.025,depth_steps)
    a=d[:,:,None]+bevel;b=np.abs(z)[None,None,:]-depth/2+bevel
    f=np.sqrt(np.maximum(a,0)**2+np.maximum(b,0)**2)+np.minimum(np.maximum(a,b),0)-bevel
    gy,gx,gz=np.gradient(f,y,x,z)
    values=[f[o[0]:f.shape[0]-1+o[0],o[1]:f.shape[1]-1+o[1],o[2]:f.shape[2]-1+o[2]] for o in CORNERS]
    base=np.stack(np.where((np.minimum.reduce(values)<0)&(np.maximum.reduce(values)>=0)),axis=1)
    idx=base[:,None,:]+CORNERS[None,:,:]
    scalar=f[idx[:,:,0],idx[:,:,1],idx[:,:,2]]
    pts=np.stack([x[idx[:,:,1]],y[idx[:,:,0]],z[idx[:,:,2]]+zshift],axis=-1)
    normals=np.stack([gx[idx[:,:,0],idx[:,:,1],idx[:,:,2]],gy[idx[:,:,0],idx[:,:,1],idx[:,:,2]],gz[idx[:,:,0],idx[:,:,1],idx[:,:,2]]],axis=-1)
    triangles=[];ns=[]
    for tet in TETS:
        v=scalar[:,tet];p=pts[:,tet];n=normals[:,tet];case=np.sum((v<0)*(1<<np.arange(4)),axis=1)
        for code in range(1,15):
            chosen=case==code
            if not chosen.any():continue
            vv=v[chosen];pp=p[chosen];nn=n[chosen]
            ins=[i for i in range(4) if code&(1<<i)];outs=[i for i in range(4) if not code&(1<<i)]
            def edge(i,j):
                t=vv[:,i]/(vv[:,i]-vv[:,j]);return pp[:,i]+t[:,None]*(pp[:,j]-pp[:,i]),nn[:,i]+t[:,None]*(nn[:,j]-nn[:,i])
            if len(ins) in (1,3):
                one,many=(ins,outs) if len(ins)==1 else (outs,ins)
                edges=[edge(one[0],j) for j in many];triplets=[(0,1,2)]
            else:
                edges=[edge(ins[0],outs[0]),edge(ins[0],outs[1]),edge(ins[1],outs[0]),edge(ins[1],outs[1])];triplets=[(0,1,2),(1,3,2)]
            for triplet in triplets:
                t=np.stack([edges[i][0] for i in triplet],axis=1);norm=np.stack([edges[i][1] for i in triplet],axis=1)
                flip=np.sum(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])*norm.mean(axis=1),axis=1)<0
                t[flip]=t[flip][:,[0,2,1]];norm[flip]=norm[flip][:,[0,2,1]]
                triangles.append(t.reshape(-1,3));ns.append(norm.reshape(-1,3))
    vertices=np.concatenate(triangles);normals=np.concatenate(ns)
    vertices,first,inverse=np.unique(np.round(vertices,8),axis=0,return_index=True,return_inverse=True)
    normals=normals[first];normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-9)
    faces=inverse.reshape(-1,3)
    noncollapsed=(faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,2]!=faces[:,0])
    faces=faces[noncollapsed]
    area=np.linalg.norm(np.cross(vertices[faces[:,1]]-vertices[faces[:,0]],vertices[faces[:,2]]-vertices[faces[:,0]]),axis=1)
    faces=faces[area>1e-14]
    _,unique=np.unique(np.sort(faces,axis=1),axis=0,return_index=True)
    faces=faces[np.sort(unique)]
    return vertices.tolist(),normals.tolist(),faces.ravel().tolist()

SPECS=[
 {'id':'01-soft-keys','name':'Soft keys','description':'Sage caps, a fine coral gasket and ivory bases. A friendly tactile pair.', 'layers':[(.11,.018,-.18,'paper'),(.045,.008,-.1025,'accent'),(.27,.048,.055,'secondary')], 'palette':{'secondary':('#9ebaaa',.34,0),'accent':('#e66e45',.32,0),'paper':('#f5f0e4',.42,0)},'wave':.018,'tilt':.045},
 {'id':'02-porcelain','name':'Porcelain twins','description':'Deep ivory ceramic letters with a warm coral reverse. A small shared bow.', 'layers':[(.08,.018,-.23,'accent'),(.38,.058,0,'body')], 'palette':{'body':('#f5f0e4',.20,0),'accent':('#db653f',.29,0)},'wave':.012,'tilt':.07},
 {'id':'03-ink-cushions','name':'Ink cushions','description':'Plump ink letters with softly rounded shoulders. A slow buoyant breathing motion. Ivory in dark mode.', 'layers':[(.48,.075,0,'ink')], 'palette':{'ink':('#29332d',.28,.04)},'wave':.028,'tilt':.035},
]
def main():
    assets=[]
    for spec in SPECS:
        m=pack.Model(spec['id'],spec['name'],'Brand study',spec['description']);m.palette=spec['palette'];m.presentation={'viewDirection':[1.35,.8,6.5],'study':True,'motionFrame':.06,'motionLift':0};m.reviewStatus='pending-user-approval';m.interaction='Subtle idle breathing; hover to greet. No integration until approved.'
        for i,field in enumerate(FIELDS):
            pivot=[-.55 if i==0 else .55,.52,0]
            m.group={'layer':'Left ee' if i==0 else 'Right ee','explode':[0,0,0],'delay':0,'blast':[0,0,0], 'motion':{'pivot':pivot,'axis':[0,1,0],'angle':spec['tilt']*(1 if i==0 else -1),'wave':{'axis':[0,1,0],'amplitude':spec['wave'],'frequency':.5,'phase':0}}}
            for depth,bevel,z,slot in spec['layers']:
                p,n,idx=geometry(field,depth,bevel,z);m.mesh(p,n,idx,slot,label=f'{i+1}-{slot}-beveled-glyph')
        asset=pack.export_glb(m);assets.append(asset)
        render(asset,1024).save(HERE/'renders'/f'{m.slug}.png')
        print(m.slug,asset['triangles'],flush=True)
    (HERE/'catalog.json').write_text(json.dumps({'name':'threed® EE studies','status':'Pending approval — separate from the main site','assets':assets},indent=2)+'\n')
    print('Three editable 3D studies built.')

if __name__=='__main__':main()
