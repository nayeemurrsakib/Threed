"""Build the threed® identity: mirrored ee heart and outlined wordmark."""
from pathlib import Path
import json
import re
import numpy as np
from PIL import Image
from vector_geometry import contours, outline

ROOT=Path(__file__).resolve().parents[1]
INK,IVORY,ACCENT='#252823','#F5F2EA','#E2694B'
image=np.asarray(Image.open(ROOT/'references/threed-heart-concept.png').convert('RGB'))

def artwork(region,padding=16):
    x1,y1,x2,y2=region
    mask=np.max(image[y1:y2,x1:x2,:],axis=2)<105
    loops=contours(mask)
    ys,xs=np.where(mask)
    xmin,xmax,ymin,ymax=xs.min(),xs.max(),ys.min(),ys.max()
    return outline(loops,xmin-padding,ymin-padding),int(xmax-xmin+2*padding+1),int(ymax-ymin+2*padding+1)

word,ww,wh=artwork((300,220,1260,480))

# Original cubic geometry, rather than a pixel trace: a single e and its exact
# mirror. Balanced lobes, diagonal crossbars, and two rounded lower terminals.
left_e=('M345 242 '
        'C360 196 342 117 300 63 C262 16 213 0 165 0 '
        'C69 0 0 82 0 177 C0 272 62 338 145 385 '
        'C210 422 280 453 330 496 Q342 507 347 487 '
        'C360 438 332 394 296 371 C265 350 230 337 200 320 '
        'C126 281 93 257 86 217 L300 279 C322 285 336 268 345 242 Z '
        'M83 167 C86 123 113 84 154 80 C200 75 240 119 249 166 '
        'C252 179 253 195 251 211 Q251 216 246 214 '
        'L88 171 Q83 170 83 167 Z')

def transform_path(path,mirror=False):
    # All source commands use absolute x/y pairs, including their controls.
    parts=re.findall(r'[A-Z]|-?\d+(?:\.\d+)?',path)
    result=[]
    coordinate=0
    for part in parts:
        if part.isalpha():
            result.append(part)
            coordinate=0
        else:
            value=float(part)
            if coordinate%2==0:
                value=(712-value if mirror else value)+16
            else:
                value+=16
            result.append(f'{value:g}')
            coordinate+=1
    return ' '.join(result)

heart=transform_path(left_e)+' '+transform_path(left_e,True)
hw,hh=744,540

def save(name,content):
    file=ROOT/name
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(content)

def svg(path,width,height,title,color):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">threed® identity. Two lowercase e letters face one another; the standalone symbol joins their curves into a heart. Outlined vectors with a transparent background and no font dependency.</desc>
<path fill="{color}" fill-rule="evenodd" d="{path}"/>
</svg>\n'''

for name,color in (('',INK),('-ivory',IVORY),('-vermilion',ACCENT)):
    save(f'logo/wordmark/threed{name}.svg',svg(word,ww,wh,'threed® wordmark',color))
    save(f'logo/mark/threed-heart{name}.svg',svg(heart,hw,hh,'threed® mirrored ee heart',color))

# Reusable app icon with generous breathing room.
size=512
scale=350/max(hw,hh)
tx=(size-hw*scale)/2
ty=(size-hh*scale)/2
app=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="threed® app icon">
<rect width="512" height="512" rx="110" fill="{ACCENT}"/>
<path fill="{IVORY}" fill-rule="evenodd" d="{heart}" transform="translate({tx} {ty}) scale({scale})"/>
</svg>'''
save('icons/app/threed-app-icon.svg',app)

word_scale=960/ww
heart_scale=310/hw
preview=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" role="img" aria-label="threed® identity with mirrored ee heart">
<rect width="1536" height="1024" fill="{IVORY}"/>
<text x="38" y="52" fill="{INK}" font-size="18" font-family="Arial, sans-serif">threed® / Identity</text>
<path fill="{INK}" fill-rule="evenodd" d="{word}" transform="translate(288 220) scale({word_scale})"/>
<path d="M36 520H1500" stroke="{INK}" stroke-width=".7" opacity=".45"/>
<path fill="{INK}" fill-rule="evenodd" d="{heart}" transform="translate(613 600) scale({heart_scale})"/>
</svg>'''
save('previews/threed-heart-preview.svg',preview)

save('README.md','''# threed® branding

The name is **threed®**. The two middle e letters face one another. The standalone
mark pairs a regular e with its exact mirror into a heart, with diagonal
crossbars and a fine central gap. The two halves remain distinct.

Current assets:
- `logo/wordmark/threed.svg`: main transparent outlined wordmark, including ®.
- `logo/mark/threed-heart.svg`: standalone mirrored-ee heart.
- Both logo folders also contain ivory and vermilion color versions.
- `icons/3d/threed-heart-3d.png`: transparent 3D icon render, satin vermilion.
- `icons/app/threed-app-icon.svg`: flat app icon.
- `previews/threed-heart-preview.svg` and `.png`: current vector identity preview.
- `colors/`: ivory, ink, and vermilion palette.
- `typography/` and `guidelines/`: usage notes.
- `references/threed-heart-concept.png`: generated wordmark concept board.
- `references/threed-heart-refined.png`: revised heart geometry reference.
- `source/build_threed_heart.py`: current SVG builder; Pillow and NumPy required.
- `source/generation-prompts.md`: prompts used with the built-in image generation tool.

Previous ThreeDee versions remain in `archive/` and under their original filenames.
The 3D PNG is a rendered image, not an editable 3D mesh.
''')
save('typography/README.md','''# Typography

Use the supplied outlined `threed.svg` wordmark, including its small ®.
It keeps the soft rounded lettering of the earlier identity. The second of the
two e letters is mirrored inward. Do not retype the logo using a standard font.

Supporting text: quiet regular sans serif, such as Satoshi Regular or system sans.
Logo SVGs contain no text nodes and require no installed fonts.
''')
save('guidelines/README.md','''# threed® identity

- Name: threed®, all lowercase, with the supplied superscript ®.
- Main signature: rounded wordmark with inward-facing e letters.
- Compact signature: the mirrored-ee heart. Preserve its diagonal crossbars,
  two counters, and fine central gap; never fuse the halves into a solid base.
- The heart replaces the previous eye concept; do not add pupils or a mouth.
- Colors: ink #252823, ivory #F5F2EA, vermilion #E2694B.
- Use ink on ivory or the ivory vector on a solid dark background.
- Keep clear space of half the symbol height around the heart.
- Suggested minimum widths: full wordmark 160 px; heart 32 px.
- Use the transparent 3D PNG for larger decorative placements. Use flat SVGs at small sizes.
- SVG logos are outlined and transparent. The app icon has a vermilion background.
''')
save('source/build_brand.py','''"""Build the current threed® identity."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('build_threed_heart.py')), run_name='__main__')
''')
print(f'Wordmark: {ww}×{wh}; heart: {hw}×{hh}. Six SVG logo variants and app icon saved.')
