"""Individually constructed camera finish study: hollow covers and authored mechanical layers.
The shell is a continuous loft with a true circular aperture, rather than stacked solid boxes.
"""
import math, json, pathlib, shutil
from math import sin,cos,pi,sqrt

def group(m,name,offset,delay=0):m.group={'layer':name,'explode':offset,'delay':delay}
def smooth_profile(points,steps=6):
    result=[];closed=points[0]==points[-1];src=points[:-1] if closed else points
    for i in range(len(src) if closed else len(src)-1):
        p0=src[(i-1)%len(src)] if closed else src[max(0,i-1)]
        p1=src[i];p2=src[(i+1)%len(src)];p3=src[(i+2)%len(src)] if closed else src[min(len(src)-1,i+2)]
        for j in range(steps):
            t=j/steps;t2=t*t;t3=t2*t
            result.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t2+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t3) for k in range(2)))
    result.append(result[0] if closed else src[-1]);return result

def add_mesh(m,points,indices,material,label,rows=0,columns=0):
    normals=[[0.,0.,0.] for _ in points]
    for i in range(0,len(indices),3):
        ia,ib,ic=indices[i:i+3];a,b,c=points[ia],points[ib],points[ic]
        u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        for index in (ia,ib,ic):
            for k in range(3):normals[index][k]+=n[k]
    if rows and columns:
        for row in range(rows):
            a=row*columns;b=a+columns-1;combined=[normals[a][k]+normals[b][k] for k in range(3)]
            normals[a]=combined[:];normals[b]=combined[:]
    for i,n in enumerate(normals):
        length=sqrt(sum(v*v for v in n));normals[i]=[v/length for v in n] if length>1e-12 else [0,0,1]
    m.mesh(points,normals,indices,material,label=label)

def create_camera(Model):
    m=Model('rangefinder-camera','Studio camera','Devices','A hollow pearl camera with a sculpted front cover, periwinkle optical assembly, glass elements and a removable film cartridge.')
    m.palette={
        'body':('#f5f5f1',.23,0),'accent':('#a4b3dd',.24,0),'secondary':('#bcc8e9',.32,0),
        'ink':('#191d24',.34,.06),'metal':('#b8bdc3',.19,.92),'lens':('#102128',.15,.05),
        'paper':('#eff1ed',.5,0),'rubber':('#25282d',.72,0),'glass':('#aec6cf',.055,0),
        'circuit':('#364b42',.58,.05),'optic':('#487a84',.11,.28)}
    m.alpha={'glass':.08}
    m.preferredPalette='Cobalt';m.study='camera-finish-v04';m.qualityStandard='camera-craft-v1'
    m.presentation={'viewDirection':[.36,.20,1.0],'explodeYaw':-.27,'contactShade':.42,'study':'camera-finish-v04'}
    cx,cy=.105,.635;segments=192
    def outline(a,inset):
        hw=.65-inset;hh=.83-inset;r=max(.04,.245-inset*.6);dx,dy=cos(a),sin(a)
        low,high=0,3
        for _ in range(30):
            distance=(low+high)*.5;x=cx+dx*distance;y=cy+dy*distance
            qx=abs(x)-(hw-r);qy=abs(y-.91)-(hh-r)
            sdf=sqrt(max(qx,0)**2+max(qy,0)**2)+min(max(qx,qy),0)-r
            if sdf>0:high=distance
            else:low=distance
        return cx+dx*(low+high)*.5,cy+dy*(low+high)*.5
    def sample(spec,a):
        kind,value,z=spec
        if kind=='circle':return [cx+value*cos(a),cy+value*sin(a),z]
        if kind=='outline':x,y=outline(a,value);return [x,y,z]
        if kind=='blend':
            x,y=outline(a,.065);ix,iy=cx+.335*cos(a),cy+.335*sin(a)
            return [ix+(x-ix)*value,iy+(y-iy)*value,z]
        return [cx,cy,z]
    def loft(profile,material,label):
        points=[sample(spec,2*pi*i/segments) for spec in profile for i in range(segments+1)];idx=[]
        for row in range(len(profile)-1):
            for i in range(segments):
                a=row*(segments+1)+i;b=a+segments+1;idx.extend([a,b,a+1,a+1,b,b+1])
        add_mesh(m,points,idx,material,label,len(profile),segments+1)

    group(m,'Rear ceramic housing',[.105,0,-.14],.03)
    tray=[('point',0,-.195),('outline',.105,-.195),('outline',.08,-.185),('outline',.061,-.155),('outline',.058,.08),('outline',.05,.101),('outline',.035,.108),('outline',.008,.10),('outline',0,.08),('outline',0,-.15)]
    for i in range(1,17):
        t=pi/2*i/16;tray.append(('outline',.105*(1-cos(t)),-.15-.12*sin(t)))
    tray.extend([('outline',.14,-.273),('point',0,-.273)])
    loft(tray,'body','hollow-pearl-rear-housing')
    group(m,'Rear-panel gasket',[.105,0,-.14],.03)
    # A dark seam is visible between the two independently hollow covers.
    loft([('outline',.055,.106),('outline',.037,.111),('outline',.02,.106)],'rubber','precision-cover-gasket')

    group(m,'Inner chassis',[.04,0,-.04],.06)
    m.box((0,.91,-.175),(1.05,1.37,.025),'circuit',.11,label='internal-pcb')
    for x,y,w,h in [(-.28,.98,.19,.27),(.27,1.04,.26,.17),(-.25,.43,.19,.17),(.22,.36,.29,.08)]:
        m.box((x,y,-.149),(w,h,.038),'ink',.022,label='chassis-electronics')
    for i in range(5):m.box((-.37+i*.15,.25,-.142),(.08,.012,.012),'metal',.003,label='pcb-contact')
    # Recessed internal optical throat, visible through the front cover aperture.
    m.lathe(smooth_profile([(.17,-.16),(.238,-.16),(.25,.10),(.226,.16),(.185,.16),(.17,-.16)]),pos=(cx,cy,0),mat='rubber',rot=(pi/2,0,0),seg=128,label='recessed-optical-throat')

    group(m,'Film cartridge',[.04,.82,-.24],.12)
    m.box((.035,1.065,-.106),(.68,.94,.045),'ink',.034,label='removable-film-cartridge')
    m.box((.035,1.14,-.078),(.573,.68,.009),'paper',.014,label='film-emulsion-window')
    m.box((.035,.70,-.076),(.40,.032,.011),'rubber',.009,label='film-grip-strip')
    for i in range(4):m.box((-.18+i*.14,.65,-.075),(.055,.015,.01),'metal',.004,label='film-contact')

    group(m,'Front sculpted cover',[-.12,.025,.48],0)
    cover=[('circle',.307,.115),('circle',.307,.298),('circle',.314,.321),('circle',.335,.334)]
    cover +=[('blend',i/14,.334+.009*sin(pi*i/14)) for i in range(1,15)]
    for i in range(1,17):
        t=pi/2*i/16;cover.append(('outline',.065*(1-sin(t)),.334-.067*(1-cos(t))))
    cover.extend([('outline',0,.14),('outline',.012,.12),('outline',.04,.115),('circle',.307,.115)])
    loft(cover,'body','hollow-front-cover-with-optical-aperture')
    # The front grip is a continuous rounded relief rather than a rectangular sticker.
    m.box((-.442,.72,.329),(.20,.98,.093),'body',.095,label='sculpted-hand-grip')
    m.box((-.44,1.30,.342),(.115,.13,.024),'metal',.022,label='viewfinder-frame')
    m.box((-.44,1.30,.356),(.079,.091,.009),'lens',.014,label='recessed-viewfinder-glass')
    m.box((-.228,1.375,.342),(.111,.287,.024),'metal',.022,label='flash-surround')
    m.box((-.228,1.375,.359),(.085,.258,.012),'paper',.013,label='frosted-flash-diffuser')
    for i in range(9):m.box((-.228,1.274+i*.025,.366),(.067,.004,.004),'body',.001,label='flash-fresnel-rib')
    for y in (1.40,1.485):m.cyl((.115,y,.344),.022,.017,'ink',(pi/2,0,0),label='status-led-socket')
    m.cyl((-.44,1.066,.362),.072,.049,'accent',(pi/2,0,0),label='rounded-front-shutter')
    m.torus((-.44,1.066,.365),.074,.004,'metal',(pi/2,0,0),seg=96)

    group(m,'Optical mount',[-.12,.025,.69],.055)
    mount=[(.237,.290),(.292,.290),(.322,.307),(.344,.342),(.346,.371),(.331,.405),(.303,.423),(.268,.426),(.245,.412),(.235,.385),(.237,.290)]
    m.lathe(smooth_profile(mount,8),pos=(cx,cy,0),mat='accent',rot=(pi/2,0,0),seg=192,label='continuous-satin-periwinkle-lens-mount')
    m.torus((cx,cy,.420),.276,.005,'secondary',(pi/2,0,0),seg=192)
    m.torus((cx,cy,.416),.298,.0028,'ink',(pi/2,0,0),seg=192)
    for i in range(32):
        a=2*pi*i/32
        m.ball((cx+.332*cos(a),cy+.332*sin(a),.387),.0028,'secondary',seg=8,rings=4,label='molded-focus-index')

    group(m,'Focus sleeve',[-.12,.025,.88],.11)
    sleeve=[(.176,.360),(.228,.360),(.238,.379),(.238,.453),(.224,.475),(.185,.475),(.176,.457),(.176,.360)]
    m.lathe(smooth_profile(sleeve,8),pos=(cx,cy,0),mat='rubber',rot=(pi/2,0,0),seg=160,label='optical-focus-sleeve')
    m.torus((cx,cy,.465),.211,.005,'metal',(pi/2,0,0),seg=160)

    group(m,'Optical glass',[-.12,.025,1.06],.165)
    m.lathe(smooth_profile([(.157,.446),(.181,.446),(.187,.463),(.183,.481),(.166,.487),(.157,.476),(.157,.446)],6),pos=(cx,cy,0),mat='metal',rot=(pi/2,0,0),seg=144,label='machined-optical-retaining-ring')
    # Six visible aperture blades sit behind an actual transparent curved window.
    m.cyl((cx,cy,.450),.165,.012,'lens',(pi/2,0,0),label='dark-optical-recess')
    for i in range(6):
        a=i*pi/3;pts=[]
        for r,t in [(.062,a),(.154,a),(.154,a+pi/3),(.062,a+pi/3)]:pts.append([cx+r*cos(t),cy+r*sin(t),.458+i*.0002])
        add_mesh(m,pts,[0,1,2,0,2,3],'ink',f'aperture-blade-{i+1}')
    m.ball((cx,cy,.476),.162,'glass',scale=(1,1,.145),seg=128,rings=48,label='curved-transparent-optical-window')
    # Side fittings and cap attach to the rear housing rather than flying as unrelated pieces.
    group(m,'Top cap',[.105,.23,-.14],.10)
    m.box((0,1.715,-.075),(.69,.035,.20),'body',.017,label='top-film-slot-cap')
    m.box((0,1.738,-.075),(.52,.007,.043),'ink',.013,label='film-ejection-slot')
    group(m,'Rear ceramic housing',[.105,0,-.14],.03)
    m.box((.648,1.48,-.06),(.058,.11,.10),'metal',.025,label='strap-lug')
    m.box((-.648,.37,-.06),(.048,.10,.10),'metal',.023,label='lower-strap-lug')
    return m

if __name__=='__main__':
    from build_pack import Model,export_glb,ROOT
    camera=create_camera(Model);asset=export_glb(camera)
    asset['preferredPalette']='Cobalt';asset['study']='camera-finish-v04'
    path=ROOT/'catalog.json';catalog=json.loads(path.read_text());catalog['assets']=[asset if a['id']==asset['id'] else a for a in catalog['assets']]
    path.write_text(json.dumps(catalog,indent=2))
    print(json.dumps({k:asset[k] for k in ('name','triangles','parts','bytes')},indent=2))
