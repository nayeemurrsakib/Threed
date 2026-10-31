"""Arrange the three preserved first passes beside their refined geometry renders."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil
ROOT=Path(__file__).resolve().parents[1]
def font(size):return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size)
def main():
    bg=(235,233,226);width=1800;cell=560;sheet=Image.new('RGB',(width,1430),bg);draw=ImageDraw.Draw(sheet)
    draw.text((50,35),'little things / refinement study',font=font(38),fill=(37,46,40))
    draw.text((50,96),'Smoother silhouettes. Softer corners. More deliberate construction.',font=font(22),fill=(87,94,87))
    names=[('dome-lamp','Dome lamp'),('rangefinder-camera','Rangefinder'),('portable-radio','Portable radio')]
    for row,(folder,label)in enumerate([('before','FIRST PASS'),('after','REFINED GEOMETRY + STUDIO REFLECTIONS')]):
        top=155+row*615;draw.text((50,top),label,font=font(15),fill=(87,94,87))
        for col,(slug,name)in enumerate(names):
            if folder=='after':shutil.copy2(ROOT/'renders'/f'{slug}.png',ROOT/'refinement/after'/f'{slug}.png')
            rgba=Image.open(ROOT/'refinement'/folder/f'{slug}.png').convert('RGBA').resize((cell,cell),Image.Resampling.LANCZOS)
            image=Image.new('RGB',rgba.size,bg);image.paste(rgba,mask=rgba.getchannel('A'))
            x=40+col*580;sheet.paste(image,(x,top+28));draw.text((x+12,top+568),name,font=font(20),fill=(37,46,40))
    sheet.save(ROOT/'reports/studies/REFINEMENT-COMPARISON.png')
    print(ROOT/'reports/studies/REFINEMENT-COMPARISON.png')
if __name__=='__main__':main()
