# Platform documentation check

Reviewed 2026-10-31. This extends the existing threed® studio; its visual system
and art direction are unchanged. No PRODUCT.md or DESIGN.md was created.

- Checked `START-HERE.md`, `integrations/framer/README.md`,
  `docs/BROWSER-CHECKS.md` and `AGENTS.md` against `index.html`, `guide.html`,
  the export controller and `Threed.tsx`. The current entry points are
  **Read the guide** and **Use on a website**, with Framer / Webflow choices,
  **Apply current studio edits**, **Library URL**, **Copy embed code**,
  **Copy URL** and **Download Framer component**. The panel says **On hover**;
  the Framer property's matching option is **Hover**.
- Corrected the remaining “Framer export panel” wording in START-HERE and
  documented the component test's actual scope. The Framer README and agent
  guidance already match the current controls, snapshot behavior and hosting
  requirements.
- Inspected `GUIDE-DESKTOP.png`, `GUIDE-MOBILE.png`, `GUIDE-DARK.png` and
  `desktop.png`. The guide evidence shows the platform logos, format table,
  platform instructions and troubleshooting in the existing light/dark design.
  Panel captures were subsequently refreshed at 1440px and 390px and reviewed
  by the finish reviewer: both show “Use on a website”, the platform selector
  and Webflow-specific host help.
- The implementation's browser checks report loaded guide images, valid local
  links, working anchors/disclosures and no horizontal overflow at 390px. These
  interaction checks were not rerun during this documentation pass. Logo sources
  are recorded in `assets/platforms/SOURCES.md`.
- Reran `node source/validate_embed.mjs` and
  `node source/validate_framer_component.mjs` under Node 24.19.0: both passed.
  The first covers scene round trips, glass alpha, view, disabled exploded poses,
  URL/markup safety and all 60 catalog IDs. The second executes the actual
  component with React/Framer stubs and checks iframe/setup output, RGB colors,
  scene options and property-control definitions.

The docs distinguish PNG stills, editable GLB meshes, JSON settings and live 3D.
They explain the blank Lottie result and require hosted HTTPS assets for visitors.
No real Framer/Webflow import or deployment was performed; stub execution and
local browser checks do not certify those published workflows.
