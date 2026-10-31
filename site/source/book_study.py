"""A sewn book study: connected hinge motion and individually bending leaves.

The book stays bound. Covers and pages rotate at the spine; no page block or
cover is translated away to fake an exploded view. Geometry is editable GLB.
"""
from quality_geometry import *

def hinge(m,name,pivot,angle,delay=0,page=None):
    group(m,name,[0,0,0],delay)
    m.group['motion']={'type':'hinge','pivot':list(pivot),'axis':[0,0,1],'angle':angle}
    if page:m.group['motion']['page']=page

def sheet(m,x0,y,width,depth,mat='paper',label='bound-paper-leaf'):
    pts=[];norm=[];idx=[];nx=56;nz=32;radius=.022
    for face in (1,-1):
        base=len(pts)
        for i in range(nx+1):
            u=i/nx;x=u*width;edge=min(x,width-x);half=depth/2
            if edge<radius:half=depth/2-radius+sqrt(max(0,radius*radius-(radius-edge)**2))
            bow=.0025*sin(pi*u);slope=.0025*pi/width*cos(pi*u)
            for j in range(nz+1):
                pts.append([x0+x,y+bow+face*.0008,half*(-1+2*j/nz)])
                n=[-slope*face,face,0];length=sqrt(sum(v*v for v in n));norm.append([v/length for v in n])
        for i in range(nx):
            for j in range(nz):
                a=base+i*(nz+1)+j;b=a+nz+1
                idx.extend([a,a+1,b,a+1,b+1,b] if face>0 else [a,b,a+1,a+1,b,b+1])
    m.mesh(pts,norm,idx,mat,label=label)

def build(m):
    passport=m.slug=='passport-wallet';w=.94 if passport else 1.12;d=1.38 if passport else 1.52
    x0=-w/2+.055;pw=w-.11;pd=d-.095;top=.205;mat='leather' if passport else 'fabric'
    m.presentation={'viewDirection':[.52,1.0,1.0],'explodeYaw':0,'contactShade':.30,'study':'bound-book-study','motionFrame':.68}
    m.interaction='Open the cover & turn the pages';m.reviewStatus='individual-study'
    m.description=('A stitched travel document with a hinged leather cover and individually bending printed leaves.' if passport else 'A thread-bound notebook with a cloth cover, rounded paper leaves and a sequential page turn at the spine.')
    group(m,'Back cover',[0,0,0]);m.box((0,.035,0),(w,.055,d),mat,.026,label='soft-rounded-bound-back-cover')
    # Thin endpaper and the lower unturned signatures remain attached to the back.
    m.box((.008,.070,0),(w-.07,.012,d-.07),'paper',.012,label='pastedown-endpaper')
    group(m,'Sewn signatures',[0,0,0]);m.box((.010,.125,0),(w-.105,.105,d-.095),'paper',.019,label='bound-lower-page-block')
    for yy in [.084+i*.009 for i in range(10)]:
        m.box((w/2-.043,yy,0),(.003,.0013,d-.16),'body',.0004,label='fine-fore-edge-page-line')
    for z in (-pd/2,pd/2):
        for yy in (.092,.119,.146,.173):m.box((.02,yy,z),(.87*pw,.0014,.002),'body',.0004,label='signature-edge')
    # The unturned reading page is curved slightly into the gutter.
    group(m,'Open reading page',[0,0,0]);sheet(m,x0,.183,pw,pd,label='attached-right-reading-page')
    print_page(m,x0,.1842,pw,pd,passport,0)
    group(m,'Cloth spine and binding',[0,0,0]);m.box((-w/2+.018,.120,0),(.068,.215,d),mat,.031,label='cloth-wrapped-flexible-spine')
    for z in (-d/2+.035,d/2-.035):
        for i in range(12):m.box((x0+.01+i*.011,.179,z),(.006,.009,.008),'accent',.002,label='woven-headband-thread')
    # Three thin leaves open one after another. Their pivot positions are authored
    # in model space, and the exporter normalizes pivots with the actual mesh.
    for i in range(3):
        yy=.191+i*.004
        hinge(m,f'Turning leaf {i+1}',(x0,yy,0),2.75+i*.030,.28-i*.075,{'width':pw,'bend':.14,'phase':1})
        sheet(m,x0,yy,pw,pd,label=f'rounded-two-sided-turning-leaf-{i+1}')
        print_page(m,x0,yy+.0012,pw,pd,passport,i+1)
        print_page(m,x0,yy-.0012,pw,pd,passport,i+1,side=-1)
    hinge(m,'Front cover',(x0,.225,0),2.92,.015)
    m.box((0,.232,0),(w,.047,d),mat,.023,label='hinged-cloth-front-cover' if not passport else 'hinged-leather-front-cover')
    m.box((.008,.204,0),(w-.065,.005,d-.065),'paper',.012,label='inside-front-cover-endpaper')
    if passport:
        ring(m,(.015,.258,-.12),.17,.161,.003,'metal');m.torus((.015,.261,-.12),.115,.003,'metal')
        for z in (-d/2+.075,d/2-.075):m.rod((-w/2+.07,.259,z),(w/2-.07,.259,z),.0025,'body')
        for x in (-w/2+.07,w/2-.07):m.rod((x,.259,-d/2+.075),(x,.259,d/2-.075),.0025,'body')
        m.box((.015,.260,.28),(.29,.003,.019),'metal',.005,label='foil-title-rule')
    else:
        # Quiet blind debossing, a cloth-covered joint and no loose elastic to
        # pass through the turning cover.
        m.box((.12,.257,-.34),(.39,.002,.015),'secondary',.005,label='blind-debossed-cover-rule')
        m.box((.12,.257,-.29),(.25,.002,.010),'secondary',.004,label='blind-debossed-subtitle-rule')
    group(m,'Ribbon bookmark',[0,0,0]);m.box((.06,.115,d/2+.055),(.037,.006,.23),'accent',.003,label='bound-satin-bookmark')

def print_page(m,x0,y,w,d,passport,index,side=1):
    # These marks share the leaf's hinge and curvature; nothing floats above it
    # when it turns. Keep the layout restrained enough to read as paper at 64px.
    ink='secondary' if not passport else 'ink'
    def mark(cx,cz,ww,dd,mat,label):
        pts=[];norm=[];idx=[];n=20
        for i in range(n+1):
            x=cx-ww/2+ww*i/n;u=(x-x0)/w;bow=.0025*sin(pi*u);slope=.0025*pi/w*cos(pi*u)
            for z in (cz-dd/2,cz+dd/2):
                pts.append([x,y+bow,z]);length=sqrt(1+slope*slope);norm.append([-slope*side/length,side/length,0])
        for i in range(n):
            a=i*2;idx.extend([a,a+1,a+2,a+1,a+3,a+2] if side>0 else [a,a+2,a+1,a+1,a+2,a+3])
        m.mesh(pts,norm,idx,mat,label=label)
    if not passport:
        for j in range(11):mark(x0+w*.54,-d*.35+j*d*.068,w*.73,d*.0013,ink,'printed-notebook-rule')
        mark(x0+w*.15,0,.001,d*.79,'accent','printed-margin-rule')
    else:
        mark(x0+w*.26,-d*.20,w*.22,d*.22,'secondary','passport-portrait-field')
        for j in range(5):mark(x0+w*.65,-d*.30+j*.055,w*.36,.007,ink,'passport-data-rule')
        for j in range(4):mark(x0+w*.52,d*.13+j*.055,w*.75,.006,ink,'passport-record-rule')
        for j in range(15):mark(x0+w*.16+j*w*.048,d*.37,.008,.020,ink,'document-machine-line')
