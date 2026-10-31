"""Build ThreeDee's original outlined SVG identity. Standard library only."""
from pathlib import Path
from xml.sax.saxutils import escape
import json

ROOT = Path(__file__).resolve().parents[1]
INK, PAPER = '#171717', '#FFFFFF'
GLYPHS = {
    't': ('M21 10Q21 6 25 6H39Q43 6 43 10V32H59Q63 32 63 36V48Q63 52 59 52H43V89Q43 99 53 99H60Q64 99 64 103V115Q64 119 60 119H51Q21 119 21 90V52H8Q4 52 4 48V36Q4 32 8 32H21Z', 64),
    'h': ('M5 4Q5 0 9 0H24Q28 0 28 4V43C34 34 43 29 54 29C76 29 88 43 88 65V116Q88 120 84 120H69Q65 120 65 116V68C65 54 59 48 48 48C36 48 28 57 28 71V116Q28 120 24 120H9Q5 120 5 116Z', 88),
    'r': ('M5 35Q5 31 9 31H23Q27 31 27 35V47C33 35 42 29 56 29Q60 29 60 33V47Q60 51 56 51H54C37 51 28 62 28 82V116Q28 120 24 120H9Q5 120 5 116Z', 60),
    'e': ('M86 82H24C27 95 36 102 49 102C60 102 69 98 76 91L86 105C76 115 64 120 48 120C20 120 1 102 1 75C1 48 19 29 46 29C72 29 88 48 88 73Q88 82 86 82ZM24 66H65C63 54 57 47 46 47C35 47 27 54 24 66Z', 88),
    'd': ('M66 4Q66 0 70 0H85Q89 0 89 4V116Q89 120 85 120H71Q67 120 67 116V107C61 116 51 121 39 121C16 121 1 102 1 75C1 48 17 29 40 29C51 29 60 33 66 42ZM24 75C24 91 32 101 45 101C58 101 67 91 67 75C67 59 58 49 45 49C32 49 24 59 24 75Z', 89),
}

def lettering(word, eyes=()):
    items, x = [], 0
    for i, letter in enumerate(word):
        path, width = GLYPHS[letter]
        items.append(f'<g transform="translate({x} 0)"><path fill-rule="evenodd" d="{path}"/>')
        if i in eyes:
            items.append('<circle cx="55" cy="59" r="4.8"/>')
        items.append('</g>')
        x += width + 7
    return ''.join(items), x - 7

WORD, WORD_WIDTH = lettering('threedee', (6, 7))
MARK, MARK_WIDTH = lettering('ee', (0, 1))

def svg(content, viewbox, title, color=INK, extra=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" fill="{color}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">Original outlined lettering. The final two lowercase e letters contain small pupils. Transparent background; no fonts or raster images.</desc>
  {extra}{content}
</svg>\n'''

def save(relative, content):
    dest = ROOT / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)

for color, suffix in ((INK, ''), (PAPER, '-white')):
    save(f'logo/wordmark/threedee{suffix}.svg', svg(WORD, f'-16 -16 {WORD_WIDTH+32} 153', 'ThreeDee wordmark', color))
    save(f'logo/mark/threedee-eyes{suffix}.svg', svg(MARK, f'-16 13 {MARK_WIDTH+32} 123', 'ThreeDee eye mark', color))

# Quiet review sheet; the actual logo assets are transparent and tightly framed.
preview = f'''<rect width="1440" height="900" fill="{PAPER}"/>
<g transform="translate(200 260) scale({1040/WORD_WIDTH})" fill="{INK}">{WORD}</g>
<g transform="translate(650 620) scale(.8)" fill="{INK}">{MARK}</g>'''
save('previews/threedee-preview.svg', svg(preview, '0 0 1440 900', 'ThreeDee minimal identity preview'))

save('colors/palette.json', json.dumps({'ink': INK, 'paper': PAPER}, indent=2) + '\n')
save('colors/palette.css', ':root {\n  --threedee-ink: #171717;\n  --threedee-paper: #ffffff;\n}\n')
save('typography/README.md', '''# Typography

The wordmark uses original custom vector letterforms, not an installed font.
Do not retype it: use the outlined SVG.

For supporting text, use a quiet sans serif such as Satoshi Regular or the
system sans serif. Keep supporting copy small and let the wordmark lead.
No font files are required by or bundled with the logos.
''')
save('guidelines/README.md', '''# ThreeDee

A minimal black-and-white identity. The only expressive detail is the pair
of pupils inside the final two e letters in **threedee**.

- Use the full wordmark as the main signature.
- Use the isolated **ee** mark where space is limited.
- Use ink on white, or the white SVG on a solid dark background.
- SVG backgrounds are transparent, including the letter counters.
- Keep clear space equal to at least half the lowercase letter height.
- Suggested minimum widths: wordmark 180 px; eye mark 48 px.
- Keep the pupils fixed; do not add a mouth, outline, shadow, or extra eyes.
- Keep the wordmark flat; let the library's 3D objects supply the dimension.

All logo files are editable SVG paths with no embedded images or font dependencies.
The preview is a presentation canvas, not part of the logo.
''')
save('README.md', '''# ThreeDee branding

- `logo/wordmark/`: transparent full wordmark, ink and white SVGs.
- `logo/mark/`: transparent isolated eye mark, ink and white SVGs.
- `colors/`: two-color palette as JSON and CSS.
- `typography/`: supporting type guidance.
- `guidelines/`: basic logo use and spacing.
- `previews/`: minimal identity preview as SVG and PNG.
- `source/`: editable Python builder for the original letterform paths.

Rebuild SVGs and guides with `python3 source/build_brand.py`.
''')
print(f'Created ThreeDee branding at {ROOT}; wordmark width {WORD_WIDTH}.')
