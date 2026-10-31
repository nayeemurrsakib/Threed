"""Render true material-slot palette thumbnails; no tint filters or extra WebGL contexts."""
import json,concurrent.futures,argparse
from render_previews import ROOT,render
from PIL import Image

def one(job):
    a,name,colors=job
    image=render(a,256,palette=colors)
    dest=ROOT/'previews/palettes'/name;dest.mkdir(parents=True,exist_ok=True);image.save(dest/(a['id']+'.png'))
    return a['id']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='+');args=parser.parse_args()
    assets=json.loads((ROOT/'catalog.json').read_text())['assets'];palettes=json.loads((ROOT/'presets/palettes.json').read_text())
    if args.only:assets=[a for a in assets if a['id'] in args.only]
    jobs=[(a,name,colors) for name,colors in palettes.items() for a in assets]
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        for i,result in enumerate(pool.map(one,jobs)):
            if i%20==0:print(f'Palette thumbnails {i+1}/{len(jobs)}: {result}',flush=True)
    print('All six collection palettes rendered.',flush=True)
