"""Deterministic CPU contact-sheet renderer. Requires NumPy and Pillow, no network or GPU."""
import json, math, pathlib, struct, time, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=pathlib.Path(__file__).resolve().parents[1]
def read_glb(path):
    data=path.read_bytes(); length=struct.unpack_from('<I',data,12)[0]
    doc=json.loads(data[20:20+length]); off=20+length; binary=data[off+8:]
    def acc(i):
        a=doc['accessors'][i]; v=doc['bufferViews'][a['bufferView']]
        dtype={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']]
        width={'VEC3':3,'SCALAR':1}[a['type']]
        return np.frombuffer(binary,dtype=dtype,count=a['count']*width,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,width)
    parts=[]
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            material=dict(doc['materials'][p['material']]['pbrMetallicRoughness']);material['_slot']=doc['materials'][p['material']]['name']
            parts.append((acc(p['attributes']['POSITION']),acc(p['attributes']['NORMAL']),acc(p['indices']).reshape(-1,3),material,mesh.get('extras',{}).get('explosionOffset',[0,0,0]),mesh.get('extras',{})))
    return parts,doc.get('extras',{}).get('presentation',{})

def rotation_matrix(axis,angle):
    axis=np.array(axis,dtype=float);axis/=np.linalg.norm(axis);x,y,z=axis;c=math.cos(angle);s=math.sin(angle);t=1-c
    return np.array([[c+x*x*t,x*y*t-z*s,x*z*t+y*s],[y*x*t+z*s,c+y*y*t,y*z*t-x*s],[z*x*t-y*s,z*y*t+x*s,c+z*z*t]])

def pose_part(part,movement,time):
    pos,norm,indices,mat,offset,meta=part;pos=pos.copy();norm=norm.copy();motion=meta.get('motion');glow=np.zeros(3)
    if motion:
        progress=max(0,min(1,time/motion['timeline'] if motion.get('timeline') else movement/.85));activation=progress
        if motion.get('activation'):a,b=motion['activation'];activation=max(0,min(1,(progress-a)/(b-a)))
        angle=motion.get('angle',0)*progress;pivot=np.array(motion['pivot'])
        if motion.get('oscillate'):angle*=math.sin(time*2*math.pi*motion['oscillate']+motion.get('phase',0))
        if motion.get('spin'):angle+=time*motion['spin']*(movement/.85)
        if motion.get('page'):
            page=motion['page'];u=np.clip((pos[:,0]-pivot[0])/page['width'],0,1)
            pos[:,1]+=page['bend']*np.sin(np.pi*u)*math.sin(angle)
            slope=page['bend']*math.pi/page['width']*np.cos(np.pi*u)*math.sin(angle);norm[:,0]-=slope*norm[:,1]
        scale=np.array(motion.get('scaleFrom',[1,1,1]))+(np.array(motion.get('scaleTo',[1,1,1]))-np.array(motion.get('scaleFrom',[1,1,1])))*activation
        rotation=rotation_matrix(motion['axis'],angle);pos=((pos-pivot)*scale)@rotation.T+pivot;norm=(norm/scale)@rotation.T
        shift=np.array(motion.get('translate',[0,0,0]),dtype=float)*progress
        if motion.get('follow'):
            f=motion['follow'];fp=np.array(f['pivot']);point=np.array(f['point']);shift+=(point-fp)@rotation_matrix(f['axis'],f['angle']*progress).T+fp-point
        if motion.get('wave'):
            w=motion['wave'];shift+=np.array(w.get('axis',[0,1,0]))*progress*(w.get('lift',0)+w.get('amplitude',0)*math.exp(-w.get('decay',0)*time)*math.sin(time*2*math.pi*w['frequency']+w.get('phase',0)))
        pos+=shift;glow=np.array(motion.get('glow',[0,0,0]))*activation
    pos+=np.array(offset)*movement;norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-9)
    return pos,norm,indices,mat,meta,glow

def render(asset,size=1024,explode=0,opening_time=None,motion_time=None,palette=None):
    parts,presentation=read_glb(ROOT/asset['model']); h=asset['dimensions'][1];study=bool(presentation.get('study'))
    parts.sort(key=lambda p:p[3]['baseColorFactor'][3]<1)
    target=np.array([0,h*(.48 if study else .46),0]); eye=np.array(presentation.get('viewDirection',[3.8,2.8,5.5])); f=eye/np.linalg.norm(eye)
    right=np.cross([0,1,0],f); right=right/np.linalg.norm(right); up=np.cross(f,right)
    scale=size/(2.75+explode*.8); pixels=np.zeros((size,size,3),dtype=np.float32)
    def amount(part):
        if opening_time is None:return explode
        t=max(0,opening_time-part[5].get('delay',0));return explode*(1-(1+15*t)*math.exp(-15*t))
    maximum=max(amount(p) for p in parts)
    clock=motion_time if motion_time is not None else (opening_time if opening_time is not None else (4 if explode else 0))
    posed=[pose_part(p,amount(p),clock) for p in parts]
    scale=size/(2.75+maximum*(presentation.get('motionFrame',.45)/.45)*.8)
    lift=max(0,-min(float(np.min(p[0][:,1])) for p in posed))+maximum*presentation.get('motionLift',.025)
    shadow=Image.new('L',(size,size),0); draw=ImageDraw.Draw(shadow)
    floor_y=size/2+np.dot(target,up)*scale
    width=max(.5,asset['dimensions'][0])*.34*scale
    draw.ellipse((size/2-width,floor_y-size*.035,size/2+width,floor_y+size*.047),fill=42)
    alpha=np.asarray(shadow.filter(ImageFilter.GaussianBlur(size*.035)),dtype=np.float32)/255
    coverage=alpha.copy(); depth=np.full((size,size),-np.inf)
    light=np.array([-.454,.766,.454] if study else [-3,5,5]); light=light/np.linalg.norm(light)
    half=(light+f); half/=np.linalg.norm(half)
    for pos,norm,indices,mat,meta,glow in posed:
        pos=pos+np.array([0,lift,0])
        if study and maximum:
            angle=presentation.get('explodeYaw',0)*maximum;c,s=math.cos(angle),math.sin(angle)
            pivot=np.array([0,h*.48,0]);rotation=np.array([[c,0,s],[0,1,0],[-s,0,c]])
            pos=(pos-pivot)@rotation.T+pivot;norm=norm@rotation.T
        p=pos-target
        projected=np.stack([p@right*scale+size/2,size/2-p@up*scale,p@f],axis=1)
        color=np.array(mat['baseColorFactor'][:3]);
        if palette and mat['_slot'] in palette:
            rgb=[int(palette[mat['_slot']][i:i+2],16)/255 for i in (1,3,5)];color=np.array([v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb])
        rough=mat.get('roughnessFactor',.4); metal=mat.get('metallicFactor',0)
        # Smooth vertex shading, diffuse studio fill and broad rectangular reflections.
        diffuse=np.clip(norm@light,0,1)
        hemi=(.23+.055*norm[:,1]) if study else (.44+.12*norm[:,1])
        ndv=np.clip(norm@f,0,1);reflection=2*(norm@f)[:,None]*norm-f[None,:]
        def box_reflection(axis,width,height):
            axis=np.array(axis,dtype=float);axis/=np.linalg.norm(axis)
            tangent=np.cross([0,1,0],axis);tangent/=np.linalg.norm(tangent);bitangent=np.cross(axis,tangent)
            facing=reflection@axis;denominator=np.maximum(facing,.001)
            uv=np.abs(np.stack([reflection@tangent,reflection@bitangent],axis=1)/denominator[:,None])
            blur=.028+rough*rough*1.15;dims=np.array([width,height])
            t=np.clip((uv-(dims-blur))/(blur*2),0,1);edge=1-t*t*(3-2*t)
            return edge[:,0]*edge[:,1]*(facing>0)
        environment=np.full_like(norm,.17)
        environment+=box_reflection(light,.34,.62)[:,None]*(8.32 if study else 4.8)
        environment+=box_reflection([1.8,1.4,-2.4],.12,.68)[:,None]*1.5*np.array([.82,.89,1.])
        f0=.04*(1-metal)+color*metal
        fresnel=f0[None,:]+(np.maximum(1-rough,f0)-f0)[None,:]*(1-ndv[:,None])**5
        lin=color[None,:]*(hemi[:,None]+diffuse[:,None]*(5.2/math.pi if study else .8))*(1-metal*.8)+environment*fresnel*(1-rough*.57)+glow
        opacity=mat['baseColorFactor'][3]
        if opacity<1:lin=environment*(.12+fresnel*.4)+color[None,:]*.04
        lin=np.clip((lin*(2.51*lin+.03))/(lin*(2.43*lin+.59)+.14),0,1)
        srgb=np.where(lin<=.0031308,lin*12.92,1.055*np.maximum(lin,0)**(1/2.4)-.055)
        colors=np.clip(srgb,0,1)*255
        for tri in indices:
            a,b,c=projected[tri]; den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-8: continue
            x0=max(0,int(np.floor(min(a[0],b[0],c[0])))); x1=min(size-1,int(np.ceil(max(a[0],b[0],c[0]))))
            y0=max(0,int(np.floor(min(a[1],b[1],c[1])))); y1=min(size-1,int(np.ceil(max(a[1],b[1],c[1]))))
            if x0>x1 or y0>y1: continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1]; xx=xx+.5; yy=yy+.5
            u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den; w=1-u-v
            z=u*a[2]+v*b[2]+w*c[2]; chunk=depth[y0:y1+1,x0:x1+1]
            mask=(u>=-.0001)&(v>=-.0001)&(w>=-.0001)&(z>chunk)
            if not mask.any(): continue
            col=u[:,:,None]*colors[tri[0]]+v[:,:,None]*colors[tri[1]]+w[:,:,None]*colors[tri[2]]
            target_pixels=pixels[y0:y1+1,x0:x1+1]
            if opacity<1:
                a=np.clip(opacity+(1-(u*ndv[tri[0]]+v*ndv[tri[1]]+w*ndv[tri[2]]))**5*.55,.08,.82)
                cov=coverage[y0:y1+1,x0:x1+1];old=cov[mask];new=a[mask]+old*(1-a[mask])
                target_pixels[mask]=(col[mask]*a[mask,None]+target_pixels[mask]*old[:,None]*(1-a[mask,None]))/np.maximum(new[:,None],1e-6)
                cov[mask]=new
            else:
                chunk[mask]=z[mask];target_pixels[mask]=col[mask];coverage[y0:y1+1,x0:x1+1][mask]=1
    opacity=coverage*255
    transparent_rgb=np.where((coverage>0)[:,:,None],pixels,0)
    return Image.fromarray(np.uint8(np.clip(np.dstack([transparent_rgb,opacity]),0,255)))

def font(size):
    for path in ['/System/Library/Fonts/Helvetica.ttc','/System/Library/Fonts/Supplemental/Arial.ttf']:
        try: return ImageFont.truetype(path,size)
        except OSError: pass
    return ImageFont.load_default()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--size',type=int,default=1024);parser.add_argument('--only',nargs='+');args=parser.parse_args()
    catalog=json.loads((ROOT/'catalog.json').read_text()); assets=catalog['assets']; t=time.time()
    (ROOT/'renders').mkdir(exist_ok=True)
    tile=220; cols=10; sheet=Image.new('RGB',(cols*tile+80,6*(tile+64)+200),(235,233,226)); d=ImageDraw.Draw(sheet)
    d.text((40,30),'threed® / vol. 01',font=font(38),fill=(37,46,40))
    d.text((40,82),'60 original 3D objects  /  editable materials  /  six collections',font=font(19),fill=(86,94,87))
    for i,a in enumerate(assets):
        if not args.only or a['id'] in args.only:
            rgba=render(a,args.size); rgba.save(ROOT/'renders'/f'{a["id"]}.png')
            image=Image.new('RGB',rgba.size,(235,233,226));image.paste(rgba,mask=rgba.getchannel('A'))
            rgba.resize((256,256),Image.Resampling.LANCZOS).save(ROOT/a['thumbnail'])
        else:
            rgba=Image.open(ROOT/a['thumbnail']).convert('RGBA')
            image=Image.new('RGB',rgba.size,(235,233,226));image.paste(rgba,mask=rgba.getchannel('A'))
        x=40+(i%cols)*tile; y=144+(i//cols)*(tile+64)
        sheet.paste(image.resize((tile,tile),Image.Resampling.LANCZOS),(x,y))
        d.text((x+8,y+tile+2),a['name'],font=font(15),fill=(37,46,40))
        d.text((x+8,y+tile+25),f'{i+1:02d} / {a["category"]}',font=font(12),fill=(105,111,103))
        print(f'{i+1:02d}/60 {a["id"]}',flush=True)
    sheet.save(ROOT/'CONTACT-SHEET.png'); print(f'Rendered in {time.time()-t:.1f}s')
if __name__=='__main__': main()
