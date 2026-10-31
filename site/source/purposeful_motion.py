"""Explicit functional motion. Attached parts share a transform; no generic explode."""
from quality_geometry import *

def still(m,name):group(m,name,[0,0,0],0)

def action(m,name,pivot=(0,0,0),axis=(0,0,1),angle=0,delay=0,**properties):
    still(m,name);m.group['delay']=delay
    m.group['motion']={'type':'functional','pivot':list(pivot),'axis':list(axis),'angle':angle,**properties}

def presentation(m,interaction,hint=None,view=None,frame=0):
    m.interaction=interaction;m.reviewStatus='individual-study'
    m.presentation.update(explodeYaw=0,motionFrame=frame,motionLift=0)
    if view:m.presentation['viewDirection']=view
    if hint:m.hint=hint

def freeze(m):
    for p in m.parts:
        if any(p['explode']) and 'blast' not in p:p['blast']=list(p['explode']);p['blastGroup']=p['layer']
        p.update(explode=[0,0,0],delay=0);p.pop('motion',None)

def bind(parts,name,pivot=(0,0,0),axis=(0,0,1),angle=0,**properties):
    for p in parts:
        p.update(layer=name,explode=[0,0,0],delay=0,motion={'type':'functional','pivot':list(pivot),'axis':list(axis),'angle':angle,**properties})

def panel(m,pos,size,mat='body',corner=.10,axis='z',label='fitted-rounded-panel'):
    """A thin molded face with a real planar corner radius, independent of depth.

    A uniform 3D box bevel is limited by thickness and cannot make a thin face
    follow a large rounded housing. This construction keeps those radii separate.
    """
    thickness=size[2] if axis=='z' else size[1]
    tray(m,pos,size,mat,corner,min(.012,thickness*.26),axis,True,label)

def ribbon(m,points,width,mat='paper',label='continuous-feed-ribbon'):
    pts=[];idx=[]
    for x,y,z in points:pts.extend([[x,y,z-width/2],[x,y,z+width/2]])
    for i in range(len(points)-1):a=i*2;idx.extend([a,a+1,a+2,a+1,a+3,a+2])
    add_mesh(m,pts,idx,mat,label)
