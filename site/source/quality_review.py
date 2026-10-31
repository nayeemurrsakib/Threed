"""Render assembled/expanded review boards; bind evidence to exact model hashes."""
import argparse,hashlib,json,time
from pathlib import Path
from PIL import Image,ImageDraw
from render_previews import render,font
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--category',action='append');args=parser.parse_args()
    catalog=json.loads((ROOT/'catalog.json').read_text());dest=ROOT/'refinement/review-v05';dest.mkdir(exist_ok=True)
    path=dest/'evidence.json';evidence=json.loads(path.read_text()) if path.exists() else {}
    for category in catalog['categories']:
        if args.category and category not in args.category:continue
        assets=[a for a in catalog['assets'] if a['category']==category];tile=320;gap=22
        board=Image.new('RGB',(tile*5+gap*2,1440),(235,233,226));d=ImageDraw.Draw(board)
        d.text((gap,24),f'{category} / collection craft review',font=font(29),fill=(37,46,40))
        d.text((gap,66),'Resting above / authored interaction below. Original surfaces, pearl palette, studio light.',font=font(16),fill=(87,94,87))
        for i,a in enumerate(assets):
            x=gap+i%5*tile;y=105+i//5*655
            rgba=Image.open(ROOT/'renders'/f'{a["id"]}.png').convert('RGBA').resize((tile,tile),Image.Resampling.LANCZOS)
            board.paste(rgba,(x,y),rgba.getchannel('A'))
            expanded=render(a,640,.85).resize((tile,tile),Image.Resampling.LANCZOS)
            board.paste(expanded,(x,y+tile),expanded.getchannel('A'))
            d.text((x+10,y+tile-26),a['name'],font=font(17),fill=(37,46,40))
            d.text((x+10,y+tile*2-16),f'{len(a["assemblies"])} assemblies / {a["triangles"]:,} triangles',font=font(12),fill=(87,94,87))
            evidence[a['id']]={'sha256':hashlib.sha256((ROOT/a['model']).read_bytes()).hexdigest(),'board':f'refinement/review-v05/{category.lower()}.png','views':['assembled','expanded'],'standard':a['qualityStandard']}
            print('Review rendered: '+a['id'],flush=True)
        board.save(dest/(category.lower()+'.png'));path.write_text(json.dumps(evidence,indent=2)+'\n')
    print('Review boards refreshed.')
if __name__=='__main__':main()
