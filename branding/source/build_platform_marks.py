"""Beveled editable 3D guide-button marks from the official platform SVG paths."""
from pathlib import Path
import sys,re,importlib.util,json,tempfile
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'site';OUT=SITE/'assets/platforms/3d'
sys.path.insert(0,str(SITE/'source'));sys.path.insert(0,str(ROOT/'branding/source'))
spec=importlib.util.spec_from_file_location('ee_geometry',ROOT/'branding/3d-studies/smiling-ee/source/build_studies.py')
study=importlib.util.module_from_spec(spec);spec.loader.exec_module(study)
from vector_geometry import contours
import render_previews

def flatten(path):
    tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path)
    i=0;command=None;point=np.zeros(2);start=None;line=[];paths=[]
    def number():
        nonlocal i
        n=float(tokens[i]);i+=1;return n
    while i<len(tokens):
        if tokens[i].isalpha():command=tokens[i];i+=1
        c=command.upper();relative=command.islower();origin=point.copy()
        if c=='Z':
            if line:paths.append(line);line=[]
            point=start.copy();command=None;continue
        if c in ('M','L'):
            point=np.array([number(),number()])+(origin if relative else 0)
            if c=='M':
                if line:paths.append(line)
                line=[];start=point.copy();command='l' if relative else 'L'
            line.append(point.copy())
        elif c in ('H','V'):
            axis=0 if c=='H' else 1;point[axis]=number()+(origin[axis] if relative else 0);line.append(point.copy())
        elif c=='C':
            control=np.array([[number(),number()] for _ in range(3)])+(origin if relative else 0)
            for t in np.linspace(0,1,25)[1:]:line.append((1-t)**3*origin+3*(1-t)**2*t*control[0]+3*(1-t)*t*t*control[1]+t**3*control[2])
            point=control[-1].copy()
        else:raise ValueError(command)
    if line:paths.append(line)
    return paths

def field(name):
    source=SITE/f'assets/platforms/{name}.svg'
    path=re.search(r'<path[^>]*\sd="([^"]+)"',source.read_text()).group(1)
    polygons=flatten(path);allp=np.concatenate(polygons);lo=allp.min(axis=0);span=allp.max(axis=0)-lo
    factor=480/max(span);mask=Image.new('1',(512,512));draw=ImageDraw.Draw(mask)
    offset=(512-span*factor)/2
    for polygon in polygons:draw.polygon([tuple((p-lo)*factor+offset) for p in polygon],fill=1)
    mask=np.asarray(mask);points=np.concatenate([np.asarray(p) for p in contours(mask)])
    px=np.arange(0,512,6.0);py=px.copy();xx,yy=np.meshgrid(px,py);grid=np.stack([xx.ravel(),yy.ravel()],axis=1);distance=np.full(len(grid),np.inf)
    for j in range(0,len(points),256):distance=np.minimum(distance,np.min(np.sum((grid[:,None]-points[None,j:j+256])**2,axis=2),axis=1))
    inside=mask[np.clip(np.rint(yy).astype(int),0,511),np.clip(np.rint(xx).astype(int),0,511)]
    distance=np.sqrt(distance).reshape(xx.shape)*np.where(inside,-1,1)
    return (px-256)*2.2/512,(512-py)*2.2/512,distance*2.2/512

OUT.mkdir(parents=True,exist_ok=True)
for name,source,color in [('framer-light','framer','#252823'),('framer-dark','framer','#f5f2ea'),('webflow','webflow-light','#146ef5')]:
    m=study.pack.Model(name,name,'Platform mark','Official silhouette with native rounded 3D extrusion for the guide button.')
    m.palette={'body':(color,.36,.08)};m.presentation={'viewDirection':[1.5,.9,6.5],'study':True}
    m.group={'layer':'Platform logo','explode':[0,0,0],'delay':0,'blast':[0,0,0]}
    p,n,indices=study.geometry(field(source),.30,.025,depth_steps=17);m.mesh(p,n,indices,'body',label='beveled-platform-mark')
    with tempfile.TemporaryDirectory(dir=OUT) as temp:
        folder=Path(temp);(folder/'models').mkdir();study.pack.ROOT=folder;render_previews.ROOT=folder
        asset=study.pack.export_glb(m);(OUT/f'{name}.glb').write_bytes((folder/asset['model']).read_bytes())
        rendered=render_previews.render(asset,384);alpha=np.asarray(rendered.getchannel('A'));ys,xs=np.where(alpha>80)
        bbox=(max(0,int(xs.min())-12),max(0,int(ys.min())-12),min(384,int(xs.max())+13),min(384,int(ys.max())+13));rendered.crop(bbox).save(OUT/f'{name}.png')
    print(name,asset['triangles'],flush=True)
(OUT/'README.md').write_text('Native beveled GLB meshes and transparent PNGs for the guide button. Source: branding/source/build_platform_marks.py. Official SVG path provenance: ../SOURCES.md. These are interface marks, not additional library objects.\n')
