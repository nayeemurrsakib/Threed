"""Regenerate the current camera PNG and the before/after quality study."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render_previews import render
ROOT=Path(__file__).resolve().parents[1]
def main():
    catalog=json.loads((ROOT/'catalog.json').read_text());asset=next(a for a in catalog['assets'] if a['id']=='rangefinder-camera')
    image=render(asset,1536,0).resize((1024,1024),Image.Resampling.LANCZOS);image.save(ROOT/'renders/rangefinder-camera.png')
    bg=(235,233,226);flat=Image.new('RGB',image.size,bg);flat.paste(image,mask=image.getchannel('A'));flat.resize((256,256),Image.Resampling.LANCZOS).save(ROOT/'previews/rangefinder-camera.png')
    old=Image.open(ROOT/'refinement/before-v04/rangefinder-camera.png').convert('RGBA')
    board=Image.new('RGB',(1800,1080),bg);draw=ImageDraw.Draw(board);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',26)
    draw.text((45,30),'Camera / finish and construction study',font=font,fill=(37,46,40))
    for i,(item,label) in enumerate([(old,'Previous version'),(image,'New camera benchmark')]):
        thumb=item.resize((850,850),Image.Resampling.LANCZOS);board.paste(thumb,(25+i*900,125),thumb.getchannel('A'));draw.text((45+i*900,98),label,font=font,fill=(87,94,87))
    board.save(ROOT/'reports/studies/CAMERA-QUALITY-STUDY.png')
    # Refresh the catalog sheet from the current thumbnails.
    sheet=Image.new('RGB',(2280,1904),bg);draw=ImageDraw.Draw(sheet);font38=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',38)
    draw.text((40,30),'little things / vol. 01',font=font38,fill=(37,46,40))
    draw.text((40,82),'60 original 3D objects / collection craft review / editable materials',font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',19),fill=(86,94,87))
    for i,a in enumerate(catalog['assets']):
        x=40+i%10*220;y=144+i//10*284;thumb=Image.open(ROOT/a['thumbnail']).resize((220,220),Image.Resampling.LANCZOS);sheet.paste(thumb,(x,y))
        draw.text((x+8,y+222),a['name'],font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',15),fill=(37,46,40))
        draw.text((x+8,y+245),f'{i+1:02d} / {a["category"]}',font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',12),fill=(105,111,103))
    sheet.save(ROOT/'CONTACT-SHEET.png');print('Camera still, thumbnail, quality study and catalog sheet refreshed.')
if __name__=='__main__':main()
