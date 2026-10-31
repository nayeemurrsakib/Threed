"""Small CPU-rendered illustration of the same authored layer offsets used by the viewer."""
import json
from pathlib import Path
from PIL import Image
from render_previews import render
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    catalog=json.loads((ROOT/'catalog.json').read_text());asset=next(a for a in catalog['assets'] if a['id']=='rangefinder-camera')
    frames=[]
    for i in range(12):
        t=i/11;rgba=render(asset,720,.95,opening_time=t*.8).resize((480,480),Image.Resampling.LANCZOS)
        image=Image.new('RGB',rgba.size,(235,233,226));image.paste(rgba,mask=rgba.getchannel('A'));frames.append(image)
        print(f'Layer animation {i+1}/12',flush=True)
    frames[-1].save(ROOT/'reports/studies/EXPLODED-CAMERA.png')
    sequence=[frames[0]]*5+frames+ [frames[-1]]*7+list(reversed(frames))+[frames[0]]*4
    sequence[0].save(ROOT/'reports/studies/HOVER-LAYERS.gif',save_all=True,append_images=sequence[1:],duration=60,loop=0,optimize=True,disposal=2)
    print(ROOT/'reports/studies/HOVER-LAYERS.gif')
