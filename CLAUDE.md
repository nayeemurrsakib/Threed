# threed® — Claude Code project guide

threed® is a growing library of original, editable 3D objects with a local
customization studio. Owner: Sakib.

## Project layout

- `site/` — the studio, served at the root (`index.html`, `catalog.json`,
  `models/`, `renders/`, `previews/`, `viewer/`).
  - `source/` — Python/Node generators and validators. New objects go in
    `source/object_registry.json` plus the matching `craft_*.py` recipe.
  - `docs/` — quality standard, expansion plan, release checklist, browser checks.
  - `reports/` — generated validation JSON and review boards.
- `branding/` — logo, colors, typography and 3D studies.
- `downloads/` — packaged releases; old versions stay in `downloads/archive/`.

## Commands

```sh
cd site && python3 serve.py            # studio at http://localhost:8765
python3 source/rebuild_object.py ID    # rebuild one object (preferred)
node source/build_light_glb.cjs models models-light          # rebuild all light GLBs
node source/build_light_glb.cjs models models-light ID.glb   # rebuild one light GLB
python3 source/build_pages.py           # stamp components/ (header, footer) into every page
python3 source/tokenize_css.py viewer/*.css   # snap stray CSS values back onto the token scale
```

## Before you change anything

1. Read `site/docs/QUALITY-STANDARD.md` before creating or modifying a model.
2. Work on one object at a time. Never bulk-rebuild the collection.
3. Keep existing object IDs stable; they are public download and embed URLs.
4. Never hard-code the collection size in copy or titles; derive counts from
   `catalog.json`.
5. After adding or changing a model, rebuild its light GLB in `models-light/`.
6. Use the design system: values come from `viewer/tokens.css`, repeated text uses the
   `.t-*` styles, header/footer are edited in `components/`. Reference: `design-system.html`.
   Every new component must be added to `design-system.html` as a live specimen in the same change.
7. Check light and dark themes, mobile width and reduced motion after UI changes
   (see `site/docs/BROWSER-CHECKS.md`).

## Full craft and design rules

The detailed, user-approved rules are kept in one shared file so Claude Code and
other agents stay in sync. Edit that file, not a copy:

@site/AGENTS.md
