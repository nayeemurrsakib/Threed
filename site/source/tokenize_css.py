"""Snap raw CSS values to threed® design tokens (viewer/tokens.css).

Usage: python3 source/tokenize_css.py viewer/studio.css viewer/guide.css viewer/buttons.css
Rewrites font sizes, gaps, padding, margins and corner radii to the nearest token,
and swaps colour/font literals that have a token. Safe to re-run: tokens are left alone.
"""
import re, sys

FONT = {7: '2xs', 8: '2xs', 9: 'xs', 10: 'xs', 11: 'sm', 12: 'sm', 13: 'sm', 14: 'md', 15: 'md', 16: 'md',
        17: 'lg', 18: 'lg', 19: 'lg', 20: 'lg', 21: 'xl', 22: 'xl', 24: 'xl', 26: 'xl', 28: '2xl', 30: '2xl',
        32: '2xl', 34: '3xl', 36: '3xl', 38: '3xl', 40: '3xl', 42: '4xl', 44: '4xl', 48: '4xl'}
SPACE = [2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64]
RADIUS = {2: 'xs', 3: 'xs', 4: 'xs', 5: 'xs', 6: 'sm', 7: 'sm', 8: 'sm', 9: 'sm', 10: 'sm', 11: 'md', 12: 'md',
          13: 'md', 14: 'md', 16: 'md'}  # >=15px on small controls is a pill

def space(px):
    best = min(SPACE, key=lambda s: (abs(s - px), -s))  # nearest, ties round up
    return f'var(--space-{best})'

def snap_space_value(value):
    def one(m):
        neg, num = m.group(1), float(m.group(2))
        if num <= 1:  # hairlines stay exact
            return m.group(0)
        tok = space(round(num))
        return f'calc(-1 * {tok})' if neg else tok
    return re.sub(r'(?<![\w.(-])(-?)(\d+(?:\.\d+)?)px', lambda m: one(m) if not m.group(1) else one(m), value)

def snap_radius_value(value):
    def one(m):
        num = round(float(m.group(1)))
        if num <= 1:
            return m.group(0)
        if num >= 15:
            return 'var(--radius-pill)'
        return f'var(--radius-{RADIUS.get(num, "md")})'
    return re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)px', one, value)

def snap_font_value(prop, value):
    def one(m):
        num = round(float(m.group(1)))
        return f'var(--fs-{FONT[num]})' if num in FONT else m.group(0)
    if prop == 'font-size':
        return re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)px', one, value)
    # font shorthand: only the size (the first px value, optionally followed by /line-height)
    return re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)px(?=\s*/|\s)', one, value, count=1)

DECL = re.compile(r'(?<![\w-])(font-size|font|gap|row-gap|column-gap|padding(?:-top|-right|-bottom|-left|-inline|-block)?'
                  r'|margin(?:-top|-right|-bottom|-left|-inline|-block)?|border-radius)\s*:\s*([^;}]+)')

def rewrite(css):
    def decl(m):
        prop, value = m.group(1), m.group(2)
        if prop.startswith('font'):
            value = snap_font_value(prop, value)
        elif prop == 'border-radius':
            value = snap_radius_value(value)
        else:
            value = snap_space_value(value)
        return f'{prop}:{value}'
    css = DECL.sub(decl, css)
    for old, new in [('Georgia,"Times New Roman",serif', 'var(--serif)'), ('Georgia, "Times New Roman", serif', 'var(--serif)'),
                     ('Georgia,serif', 'var(--serif)'), ('max-width:1800px', 'max-width:var(--page-max)'),
                     ('#c6c9be', 'var(--track)'), ('color:#fff8ee', 'color:var(--on-accent)')]:
        css = css.replace(old, new)
    return css

if __name__ == '__main__':
    for path in sys.argv[1:]:
        src = open(path).read()
        out = rewrite(src)
        open(path, 'w').write(out)
        uses = len(re.findall(r'var\(--(?:fs|space|radius)-', out))
        print(f'{path}: {uses} token uses')
