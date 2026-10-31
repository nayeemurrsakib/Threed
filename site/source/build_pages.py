"""Stamp shared components (components/*.html) into every page.

Pages mark where a component goes:
  <!-- component:header action=guide --> … <!-- /component:header -->
  <!-- component:footer link=design --> … <!-- /component:footer -->
Run from site/:  python3 source/build_pages.py
"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
C = lambda name: (ROOT / 'components' / f'{name}.html').read_text().strip()
ARROW = '<svg class="footer-link-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9 9 3M4 3h5v5"/></svg>'
LINKS = {
    'design': f'<a class="footer-link" href="design-system.html">Design System{ARROW}</a>',
    'studio': f'<a class="footer-link" href="./">Back to Studio{ARROW}</a>',
}
def render(name, args):
    if name == 'header':
        return C('header').replace('{{action}}', C(f"action-{args.get('action', 'guide')}"))
    if name == 'footer':
        return C('footer').replace('{{link}}', LINKS[args.get('link', 'design')])
    raise SystemExit(f'Unknown component: {name}')
MARK = re.compile(r'<!-- component:(\w+)([^>]*)-->.*?<!-- /component:\1 -->', re.S)
def stamp(m):
    args = dict(a.split('=', 1) for a in m.group(2).split())
    return f'<!-- component:{m.group(1)}{m.group(2)}-->{render(m.group(1), args)}<!-- /component:{m.group(1)} -->'
for page in sorted(ROOT.glob('*.html')):
    src = page.read_text(); out = MARK.sub(stamp, src)
    if out != src:
        page.write_text(out); print('stamped', page.name)
