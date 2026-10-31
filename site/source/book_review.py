"""A close-up motion artifact for the individual bound-book study."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
from render_previews import render,font
ROOT=Path(__file__).resolve().parents[1]

if __name__=='__main__':
    catalog=json.loads((ROOT/'catalog.json').read_text());asset=next(a for a in catalog['assets'] if a['id']=='pocket-notebook')
    frames=[];bg=(235,233,226)
    for i in range(20):
        rgba=render(asset,840,.85,opening_time=i/19*1.25).resize((560,560),Image.Resampling.LANCZOS)
        im=Image.new('RGB',rgba.size,bg);im.paste(rgba,mask=rgba.getchannel('A'));frames.append(im)
        print(f'Book motion frame {i+1}/20',flush=True)
    sequence=[frames[0]]*7+frames+[frames[-1]]*12+list(reversed(frames))+[frames[0]]*6
    sequence[0].save(ROOT/'reports/studies/BOOK-PAGE-TURN.gif',save_all=True,append_images=sequence[1:],duration=70,loop=0,optimize=True,disposal=2)
    board=Image.new('RGB',(1680,650),bg);d=ImageDraw.Draw(board)
    for i,(im,label) in enumerate([(frames[0],'Bound / closed'),(frames[7],'Cover opens / leaves turn'),(frames[-1],'Open / spine stays connected')]):
        board.paste(im,(i*560,70));d.text((i*560+22,24),label,font=font(22),fill=(37,46,40))
    board.save(ROOT/'reports/studies/BOOK-STUDY.png')
