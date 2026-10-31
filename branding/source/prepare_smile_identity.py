"""Trace the user supplied smiling identity into native, transparent SVG masters."""
from pathlib import Path
import numpy as np
from PIL import Image
from vector_geometry import contours,outline
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'branding/explorations/selected-b-happy/threed-smiling-v2.png'
mask=np.asarray(Image.open(SOURCE).convert('RGB')).mean(axis=2)<100

def vector(mask,dest,fill):
    ys,xs=np.where(mask);x0,y0=int(xs.min()),int(ys.min());x1,y1=int(xs.max()+1),int(ys.max()+1)
    d=outline(contours(mask[y0:y1,x0:x1]),0,0)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x1-x0} {y1-y0}" role="img" aria-label="threed registered"><path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>\n')
for name,fill in [('ink','#252823'),('ivory','#f5f2ea')]:
    vector(mask,ROOT/f'branding/logo/wordmark/threed-smile-{name}.svg',fill)
# Preserve the exact paired EE silhouette, crescent eyes, shared smile and gap.
ee=mask[275:565,835:1382]
vector(ee,ROOT/'branding/logo/mark/threed-smile-ee.svg','#252823')
assets=ROOT/'site/assets/brand';assets.mkdir(parents=True,exist_ok=True)
for name in ('ink','ivory'):
    p=ROOT/f'branding/logo/wordmark/threed-smile-{name}.svg';(assets/p.name).write_bytes(p.read_bytes())
p=ROOT/'branding/logo/mark/threed-smile-ee.svg';(assets/p.name).write_bytes(p.read_bytes())
print('Current smiling identity traced from supplied reference.')

# Preserve the exact full wordmark frame while replacing only its paired EE.
ys,xs=np.where(mask);left,top=int(xs.min()),int(ys.min());width,height=int(xs.max()+1-left),int(ys.max()+1-top)
for name in ('ink','ivory'):
    source=ROOT/f'branding/logo/wordmark/threed-smile-{name}.svg'
    clip=f'<defs><clipPath id="letters"><rect width="{835-left}" height="{height}"/><rect x="{1382-left}" width="{width-(1382-left)}" height="{height}"/></clipPath></defs>'
    frame=source.read_text().replace('<path ',clip+'<path clip-path="url(#letters)" ',1)
    dest=ROOT/f'branding/logo/wordmark/threed-smile-frame-{name}.svg';dest.write_text(frame)
    (assets/dest.name).write_text(frame)

# A solid tile keeps the wide smiling mark legible against browser chrome.
ys,xs=np.where(ee)
glyph=outline(contours(ee[ys.min():ys.max()+1,xs.min():xs.max()+1]),0,0)
gw,gh=int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)
for theme,backdrop,face in [('light','#f08a50','#252823'),('dark','#28302d','#ffad79')]:
    icon=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="1" y="1" width="62" height="62" rx="15" fill="{backdrop}"/><svg x="7" y="18" width="50" height="28" viewBox="0 0 {gw} {gh}"><path fill="{face}" fill-rule="evenodd" d="{glyph}"/></svg></svg>\n'
    dest=ROOT/f'branding/logo/mark/favicon-{theme}.svg'
    dest.write_text(icon)
    (assets/dest.name).write_text(icon)
