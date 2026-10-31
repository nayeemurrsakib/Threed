"""Vector outlines of the approved rounded ThreeDee concept, at a lighter weight.

Reads the image-generated concept as a reference; writes true SVG paths, never
embeds bitmap data. Requires Pillow and NumPy to read the reference pixels.
"""
from pathlib import Path
from collections import defaultdict
from xml.sax.saxutils import escape
import json
import shutil
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INK, PAPER, ACCENT = '#252823', '#F5F2EA', '#E2694B'
REFERENCE = ROOT / 'references' / 'lighter-concept.png'

def simplify(points, tolerance=.65):
    if len(points) < 3:
        return points
    a, b = np.array(points[0]), np.array(points[-1])
    p = np.array(points)
    delta = b-a
    if np.dot(delta, delta) == 0:
        distances = np.linalg.norm(p-a, axis=1)
    else:
        t = np.clip(((p-a) @ delta) / np.dot(delta, delta), 0, 1)
        distances = np.linalg.norm(p-a-t[:, None]*delta, axis=1)
    i = int(np.argmax(distances))
    if distances[i] <= tolerance:
        return [points[0], points[-1]]
    return simplify(points[:i+1], tolerance)[:-1] + simplify(points[i:], tolerance)

def contours(mask):
    edges = defaultdict(list)
    padded = np.pad(mask, 1)
    ys, xs = np.where(mask)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if not padded[y, x+1]: edges[(x,y)].append((x+1,y))
        if not padded[y+1, x+2]: edges[(x+1,y)].append((x+1,y+1))
        if not padded[y+2, x+1]: edges[(x+1,y+1)].append((x,y+1))
        if not padded[y+1, x]: edges[(x,y+1)].append((x,y))
    paths=[]
    direction = {(1,0):0, (0,1):1, (-1,0):2, (0,-1):3}
    while edges:
        start=next(iter(edges))
        point=start
        loop=[point]
        previous=None
        while True:
            options=edges[point]
            if previous is None or len(options)==1:
                following=options[0]
            else:
                incoming=direction[(point[0]-previous[0],point[1]-previous[1])]
                priority={1:0,0:1,3:2,2:3}
                following=min(options,key=lambda q: priority[(direction[(q[0]-point[0],q[1]-point[1])]-incoming)%4])
            options.remove(following)
            if not options: del edges[point]
            previous,point=point,following
            loop.append(point)
            if point==start: break
        if len(loop)>20:
            paths.append(simplify(loop)[:-1])
    return paths

def outline(loops, xoff, yoff):
    result=[]
    for points in loops:
        # Small quadratic fillets remove pixel stair steps while retaining the outline.
        vertices=[np.array((x-xoff,y-yoff), dtype=float) for x,y in points]
        steps=[]
        for i,v in enumerate(vertices):
            before,after=vertices[i-1],vertices[(i+1)%len(vertices)]
            d1,d2=np.linalg.norm(before-v),np.linalg.norm(after-v)
            radius=min(1.3,d1*.25,d2*.25)
            entry=v+(before-v)*(radius/d1)
            exit=v+(after-v)*(radius/d2)
            steps.append((entry,v,exit))
        def xy(p): return f'{p[0]:.2f} {p[1]:.2f}'
        result.append('M'+xy(steps[0][0]))
        for entry,v,exit in steps:
            result.append('L'+xy(entry)+'Q'+xy(v)+' '+xy(exit))
        result.append('Z')
    return ''.join(result)

def svg(path, width, height, title, color=INK):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Rounded ThreeDee lettering in a slightly lighter weight, retaining the large eye counters in the final ee. Transparent outlined vector artwork; no fonts or embedded images.</desc>
<path fill="{color}" fill-rule="evenodd" d="{path}"/>
</svg>\n'''

def save(name, content):
    p=ROOT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content)

image=np.asarray(Image.open(REFERENCE).convert('RGB'))
# Exact logo region, excluding the header, tagline, and lower brand applications.
pixels=image[250:492,200:1345,:]
mask=np.max(pixels,axis=2)<105
loops=contours(mask)
ys,xs=np.where(mask)
xmin,xmax,ymin,ymax=int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())
word=outline(loops,xmin-16,ymin-16)
ww,wh=xmax-xmin+33,ymax-ymin+33
eye_loops=[loop for loop in loops if min(p[0] for p in loop)>820]
exmin=min(x for loop in eye_loops for x,y in loop)
exmax=max(x for loop in eye_loops for x,y in loop)
eymin=min(y for loop in eye_loops for x,y in loop)
eymax=max(y for loop in eye_loops for x,y in loop)
eyes=outline(eye_loops,exmin-12,eymin-12)
ew,eh=exmax-exmin+24,eymax-eymin+24
for color,suffix in ((INK,''),(PAPER,'-white')):
    save(f'logo/wordmark/threedee{suffix}.svg',svg(word,ww,wh,'ThreeDee wordmark',color))
    save(f'logo/mark/threedee-eyes{suffix}.svg',svg(eyes,ew,eh,'ThreeDee eye mark',color))

# Pure-vector presentation of the revised identity, retaining the original palette.
wordscale=1120/ww
markscale=250/ew
board=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" role="img" aria-label="ThreeDee revised brand identity">
<rect width="1536" height="1024" fill="{PAPER}"/>
<g fill="{INK}" font-family="Arial, sans-serif">
<text x="38" y="52" font-size="17">ThreeDee / Visual identity</text>
<path fill-rule="evenodd" d="{word}" transform="translate(208 250) scale({wordscale})"/>
<text x="768" y="550" font-size="28" text-anchor="middle" letter-spacing="3">A little world of 3D.</text>
<path d="M33 713H1503" stroke="{INK}" stroke-opacity=".4"/>
<path fill-rule="evenodd" d="{eyes}" transform="translate(172 787) scale({markscale})"/>
<rect x="654" y="748" width="228" height="220" rx="24" fill="{ACCENT}"/>
<path fill="{PAPER}" fill-rule="evenodd" d="{eyes}" transform="translate(678 811) scale({180/ew})"/>
<g font-size="17" text-anchor="middle">
<circle cx="1150" cy="831" r="42" fill="{PAPER}" stroke="{INK}" stroke-width=".5"/>
<circle cx="1278" cy="831" r="42"/>
<circle cx="1406" cy="831" r="42" fill="{ACCENT}"/>
<text x="1150" y="905">Ivory<tspan x="1150" dy="25">#F5F2EA</tspan></text>
<text x="1278" y="905">Ink<tspan x="1278" dy="25">#252823</tspan></text>
<text x="1406" y="905">Vermilion<tspan x="1406" dy="25">#E2694B</tspan></text>
</g></g></svg>'''
save('previews/threedee-preview.svg',board)
save('colors/palette.json',json.dumps({'ink':INK,'ivory':PAPER,'vermilion':ACCENT},indent=2)+'\n')
save('colors/palette.css',f':root {{\n  --threedee-ink: {INK};\n  --threedee-ivory: {PAPER};\n  --threedee-vermilion: {ACCENT};\n}}\n')
save('typography/README.md','''# Typography

Use the supplied outlined wordmark. Its rounded lettering follows the original
concept, with a slightly lighter weight and large eye counters in the final ee.
The logo SVGs require no font installation. Use a quiet sans serif such as
Satoshi Regular for supporting copy.
''')
save('guidelines/README.md','''# ThreeDee

Retain the original rounded lettering, large curious ee eyes, warm ivory,
charcoal ink, and restrained vermilion accent. The revised weight is slightly lighter.

- Use the full wordmark as the main signature and the ee mark in compact spaces.
- Use ink on ivory or the light SVG on a solid dark background.
- Logo files are transparent outlines with no fonts or bitmap data.
- Keep clear space equal to half the lowercase letter height.
- Suggested minimum widths: wordmark 180 px; eye mark 48 px.
- Preserve the pupils and expressive eye openings. Do not add effects.

The preview includes supporting typography and is separate from the logo assets.
''')
save('README.md','''# ThreeDee branding

The original rounded identity, revised with a slightly lighter logo weight.

- `logo/wordmark/`: outlined transparent wordmark SVGs in ink and ivory.
- `logo/mark/`: matching ee eye mark SVGs in ink and ivory.
- `colors/`: original ivory, charcoal, and vermilion palette.
- `typography/`: supporting type guidance.
- `guidelines/`: basic usage rules.
- `previews/`: SVG and PNG presentation of the current identity.
- `references/`: original and revised image-generated concept boards.
- `source/`: vector outline builder and edit prompt.
- `archive/minimal-v1/`: preserved earlier black-and-white version.

Rebuild with `python3 source/vectorize_lighter.py` (Pillow and NumPy required).
''')
print(f'Generated {len(loops)} wordmark contours and {len(eye_loops)} eye-mark contours.')
print(f'Wordmark viewBox {ww} x {wh}; mark {ew} x {eh}.')
