# Components

Repeated page parts live here once and are stamped into every page by
`python3 source/build_pages.py`. Edit the component, run the script, never edit the
copy inside a page (it is between `<!-- component:… -->` markers and gets overwritten).

- `header.html` — top bar: wordmark, edition, theme switch, then `{{action}}`.
- `action-guide.html` / `action-back.html` — the header's right-hand button.
- `footer.html` — tagline, creator credit, then `{{link}}` (set per page).

Visual components (buttons, chips, switches, sliders, tiles, swatches, menus) are CSS
classes; their live reference is `design-system.html`.
