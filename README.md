# threed®

- `site/` — editable 60-object studio (served at the root: `index.html`, `catalog.json`, `models/`, `renders/`, `previews/`).
  - `docs/` — internal quality standard, expansion plan, release checklist, browser checks.
  - `reports/validation/` — generated validation JSON; `reports/studies/` — generated comparison boards and GIFs.
  - `source/` — Python/Node generators and validators; `refinement/` — per-object refinement notes.
  - Customer-facing files stay at the root: `START-HERE.md`, `CUSTOMER-LICENSE-DRAFT.md`, `CONTACT-SHEET.png`, `CATALOG.csv`, `SHA256SUMS.txt`.
- `branding/` — supplied identity, original explorations, current smiling logo and separate 3D studies.
- `downloads/` — packaged studio; historical archives stay in `archive/`.

The local studio remains at http://localhost:8765. The former `little-things-pack` path is a compatibility symlink to `site/`.

The supplied smiling threed® wordmark is the current identity. Older heart and eye explorations remain as history. The user authorized integration of the 3D EE inside the wordmark. Soft keys is used with a high-contrast smiling expression; the other two studies remain alternatives.

## Run locally

```sh
cd site
python3 serve.py
```

Open [the studio](http://localhost:8765), [the platform guide](http://localhost:8765/guide.html), or [the live design system](http://localhost:8765/design-system.html). No build step is required.

Before editing, read `site/AGENTS.md`. Shared values live in `site/viewer/tokens.css`; shared page components live in `site/components/`. Run `python3 site/source/build_pages.py` after component edits. Native controls and their design-system specimens share `site/viewer/motion-controls.js`.

Approved avatar masters live in `branding/avatars/`; the green portrait is the footer default, with the yellow-beanie portrait retained as an alternative. Local backups, generated download archives, credentials and local helper tools are excluded from Git.
