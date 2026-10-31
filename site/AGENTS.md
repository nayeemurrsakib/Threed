# threed® craft requirements

The user chose the Studio camera in `source/camera_benchmark.py` as the quality
benchmark for **every current and future illustration**. Preserve the existing
studio design unless the user requests a change. Read `docs/QUALITY-STANDARD.md`
before creating or modifying a model.

The user explicitly rejected rushing out a bulk procedural collection. Work on
one object at a time, including its close-up finish and its natural behavior.
The camera is user-approved; other models remain studies unless the user says
otherwise. Do not promote a bulk rebuild or a passing script as curated quality.
For a book, the cover hinges on the spine and thin pages bend and turn while
remaining bound. Do not substitute floating cover/page-block slabs. Choose each
future object's motion from its real construction and use, not a universal
separation effect. Prefer `source/rebuild_object.py ID` for individual work.

Persistent user feedback: animation must demonstrate real use. Keep housings,
handles, sewn straps, headband joints, ribbons and labels attached. The current rule applies to EVERY icon, including the camera: keep the
object assembled and author only slight, smooth motion tied to its real use.
Never reinstate exploded views by default. Tape unrolls; clocks move their hands (no floating extra crystal);
hourglasses transfer sand within a fixed frame; calculator keys can wave;
headphone cups swivel on connected yokes; controller controls press/tilt; a webcam
aims while its optical front stays fitted; a kettle pours; toast pops up; a pot
lifts only its lid with its knob; a bottle lid unscrews with its complete loop;
gift side ribbon and parcel front tape stay fixed; a tote lifts whole; a printer
feeds paper; a lantern lights up; a cap stays sewn together; a rocket lifts a
little with an engine flame. Never expose a solid cap where a lifted part should
reveal a bore. Thin fitted panels need an independent corner radius matching the
housing; a thickness-limited box bevel is not sufficient. Check transitions for
intersections and frame-rate-dependent stutter as well as their endpoints.

- Author a recognizable silhouette with continuous curvature and properly sampled
  bevels. Adding polygons, global gloss or a palette alone is not a quality pass.
- Use meaningful fitted parts. Open objects must show inner surfaces; lens rings
  need real apertures; separated lids and shells need presentable undersides.
- Keep material response appropriate: polished ceramic, satin molded parts,
  brushed metal, soft rubber, paper, leather and fabric are distinct surfaces.
  Preserve alpha when recoloring/exporting glass.
- Every mesh must belong to an explicitly named assembly with an authored offset
  and delay. Never restore a position-based top/middle/bottom fallback.
- Keep the approved camera intact unless the user requests a camera change.
- New objects go in `source/object_registry.json` and the relevant `craft_*.py`
  recipe. Use `quality_geometry.py`; unknown recipes must fail instead of silently
  generating a generic object. Existing IDs are stable download/embed URLs.
- Generate assembled PNGs and assembled/expanded category review boards, inspect
  them, and run the structural/round-trip checks described in the quality guide.
  Record defects and repairs honestly. A metadata label or passing binary check
  does not certify an object's aesthetic quality.
- Do not count palettes, renders, layers or variations as additional base models.
- Keep original editable geometry, recoloring, relighting and subtle functional hover motion;
  do not replace models with flat AI images to simulate editable 3D.
- Continue within the user's requested scope. No extra approval ceremony is
  required for local reversible modeling, rendering, or verification.

Color Story is a collection-wide choice. Preserve it when switching objects or
reloading the studio and show the same palette in all gallery thumbnails. Keep
the removed intro section out. Use the supplied smiling threed® wordmark. Keep proposed 3D EE mascots in separate studies until the user approves integration.

Studio spacing: keep exactly 40 CSS px between the motion controls and the
download row. Gallery selection/focus outlines must remain visible, including
at the top of its scroll area. Keep the scene settings button fully rounded.

Keep the shadow receiver below final rotated/deformed geometry at every view
angle. Never let a fixed ground plane clip a tilted object. Preserve its orbit
center and resting-ground anchor so real lift/launch gestures retain clearance.

Latest user direction: optional exploded views are explicitly requested for every icon through a button. They must be off on initial load, reload and object changes; default hover remains slight and purposeful. Author distinct semantic blast groups. Never use blast metadata for default hover.

Keep all work under `/Users/nayeemurrahmansakib/Works/threed`: `site/`, `branding/` and `downloads/`. The old project path is a compatibility symlink. Remove lamp power wires. Display gallery names and indices side by side. Use circular icon-only theme controls, clear selected states, animated theme changes and filled range tracks. Reserve scroller padding for complete focus rings.

Headphones use a directly attached neutral ink headband, with no gold/brass trim or exposed decorative fork strips. Search focus wraps the complete padded field, including the icon; dropdown chevrons sit inset from their right border.

The user authorized 3D logo integration, then clarified: replace only the EE inside the supplied wordmark; never add a separate EE badge. Use high-contrast ink/ivory faces for light/dark and an actual smiling lip/crescent-eye expression, with restrained idle and hover motion. The speaker cone, dust cap and rubber surround pulse together; scale plate dips under weight and settles with a decaying bounce. Cap bill ends taper smoothly into the crown rather than exposing square corners.

Latest logo color: use the warm orange from the user supplied EE reference on the 3D EE faces in both themes, with an ivory base and darker orange edge. Keep the remaining wordmark letters ink/ivory for light/dark. Use an actual smile expression; do not move a separate EE badge.

Browser identity uses separate light/dark smiling EE favicons with a solid rounded backdrop. Keep the title “threed® — The 3D object library” and marketing copy free of a fixed collection size; derive navigation counts from the catalog.

Framer integration uses the live 3D embed and downloadable Threed.tsx property controls. Keep PNG for still illustrations, GLB for geometry and scene JSON for configuration. Never label a GLB or scene recipe as Lottie/SVG animation. Embed snapshots preserve materials including glass alpha, lighting, view and reduced-motion behavior. State clearly that localhost embeds require hosted HTTPS assets for published Framer sites.

Read the guide opens guide.html, a human-readable light/dark platform guide. Keep its platform logos sourced from official assets (assets/platforms/SOURCES.md), and distinguish PNG images, live 3D embeds, editable GLBs and JSON settings. The export panel is named Use on a website and supports Framer and Webflow instructions.

The user removed the Use on a website entry from the studio. Keep integration preparation on guide.html only, under Prepare your embed; do not restore a studio integration CTA.

The Read the guide CTA uses small native 3D Framer and Webflow marks, with dark/light Framer variants. Preserve the editable GLB sources and transparent renders; do not put the removed website CTA back in the studio.

Latest guide CTA direction overrides 3D marks: use small 2D Framer/Webflow logos in one shared backdrop. Cutout and scene-settings buttons open two-choice menus: Download or Copy code. Cutout code is a self-contained HTML image; scene code is the JSON recipe.

Guide badge is exactly 30 × 30 CSS px with 50% radius and softened .78-opacity 2D marks. Back to the studio uses a simple left arrow. Export menus must survive automatic focus scrolling, support Escape/keyboard navigation, and stay inside mobile viewport edges.

Latest guide CTA supersedes the paired-mark direction: only the 2D Framer logo, centered inside the circular backdrop. Desktop left button padding is reduced to 7px.

Latest cutout menu direction: Download or Copy PNG, copying actual image/png clipboard data, never an HTML image snippet. Scene settings keep Download or Copy code (JSON). Preserve clipboard activation by supplying the PNG Blob promise to ClipboardItem within the click handler.

Scene-settings Copy code must produce a renderable self-contained HTML 3D embed, never raw JSON text. Download keeps the JSON recipe. The embedded viewer and compressed edited model travel with the copied HTML; no localhost URL is required. Cutout Copy PNG remains an actual PNG clipboard item.

Export labels are now Save PNG and Save JSON inside their buttons, with chevrons; no labels above them. Header guide/back controls match theme-switch height (46px desktop /44px mobile). PNG uses a separate framebuffer and never resizes the live preview canvas.

Save JSON hover border is subtle: 80% line color mixed with muted text, never the full ink foreground.

Back to the studio arrow uses the same soft 30px circular backdrop and7px left padding as the guide’s Framer mark, with matched46px/44px header heights.

The guide headline uses the actual supplied wordmark with its orange 3D EE, replacing plain text threed® while retaining “A little” and “Anywhere you build.” Header and headline logo instances each initialize independently and respect themes/reduced motion.

Layout 0.9: desktop is an app shell (page never scrolls; collection, studio and properties each scroll inside the window). At 870px and below the collection is a two-row sideways strip; on phones the stage stays pinned at the top while the caption, strip, controls and properties scroll beneath it. Category chips stay on one scrollable row. Backdrop swatches show a BACKDROP label on hover/focus; the stage hint hides when the stage is narrower than 480px. Header edition reads VOL. 01.

Light GLBs: every model has a quantized copy in `models-light/` (KHR_mesh_quantization, identical parts, materials, extras and triangle counts; geometry within 0.003%). Save 3D object offers Full detail or Light; both carry the edited colours and finish. The studio renderer reads only the full files. Rebuild with `node source/build_light_glb.cjs models models-light [ID.glb]` after any model change.

Footer centre is the creator credit: tiny round avatar (assets/brand/nayeemur-r-s.jpg, stored locally) + "A PROJECT BY NAYEEMURRSAKIB" in footer mono caps, linking to https://x.com/nayeemur_r_s. Keep the padding around the stage; the user tried edge-to-edge and preferred the padded version. On desktop the collection runs to the bottom edge, flush with the property panel.

Design system (0.9.4): `viewer/tokens.css` is the single source for colour (light + dark), type scale (--fs-2xs 8 … --fs-5xl 64), text styles (.t-label, .t-meta, .t-caption, .t-body-sm, .t-body, .t-title, .t-heading, .t-display), spacing (--space-2 … --space-64 on a 4px grid), radii (--radius-xs/sm/md/pill/round), layout (--page-max, --page-gutter, --header-h, --control-h) and motion. Every page loads it first. Never write raw px for font size, gap, padding, margin or radius; run `python3 source/tokenize_css.py viewer/*.css` after CSS edits. Header and footer are components in `components/` stamped by `python3 source/build_pages.py`; never edit the copies between the component markers. `design-system.html` is the live reference and now holds the button kit; `buttons.html` redirects to it. The footer's right link points to the design system. Explode is an "Exploded view" switch, not a button. Two hairlines frame the workspace on both sides.

Page gutter (window edge to the frame lines) is 32px on tablet and desktop; header content aligns with the workspace content (gutter + 20px). Frame lines run through the footer to the bottom.

User rule: whenever a new component is created, add it to design-system.html (live specimen + class name) in the same change. Footer link keeps the footer mono style with an accent arrow icon (not sans).

Footer credit avatar flips on hover (coin flip, 640ms; fade under reduced motion) from the X photo to assets/brand/nayeemur-r-s-3d.svg, a very minimal hand-drawn avatar of the user (pill-shaped head, swept black hair, rectangular dark frames, moustache bar, chin beard, navy sweater; soft gradients only, no other detail) on the warm stage backdrop with a contact shadow, matching the library objects. Not the logo.

Design-system specimens must be built with the same code the studio uses (e.g. exportMenu from viewer/export-menu.js), never hand-copied markup, so they cannot drift. Reset is .reset-button (icon pill; hover winds the icon back, click spins it). Material colours are .color-control chips: whole chip opens the picker, swatch grows on hover, the hex appears as a floating ink tag above the chip.

Stage backdrop swatches: Bone and Ink only (Cobalt removed; saved cobalt falls back to the theme default). Credit avatar: the user will supply his own generated image at assets/brand/nayeemur-r-s-3d.png, which takes priority over the SVG fallback. Do not redraw the avatar unless asked.

Footer live status (viewer/status.js, loaded by the footer component): .site-status beside the right-hand link. Green pulsing dot + "ALL SYSTEMS OPERATIONAL"; turns red ("SOMETHING WENT WRONG" / "YOU ARE OFFLINE", reason on hover) on script errors, unhandled promise errors (not aborted view transitions), failed loads (HTTP 400+ or element load errors), missing WebGL 2 on 3D pages, the studio reporting data-ready=error, or going offline. Optional files (the avatar PNG) are listed in OPTIONAL and never trigger it. Colours: --status-ok / --status-error tokens.

Calm studio (0.11): orbit frame off by default (and after Reset); stage hint shows only until the first hover (2.2s), drag or key press on the object, remembered in localStorage threed-hint-seen; model facts moved from under the buttons into the Save 3D object menu (export-menu `note`). Settings panel: 01 Color story, 02 Surface (finish, interaction amount; always visible), 03 Studio light (presets only), 04 Fine-tune — a <details> holding the Light sliders and Shadow sliders, closed by default, open state remembered (threed-fine-tune-open).

Browsing (0.12): .stage-nav previous/next buttons on the stage (fade in on stage hover, always visible on touch); left/right arrow keys step through the visible collection (ignored while typing, on the focused canvas, or in menus); objects crossfade (stage.is-switching: fade + blur) and the "Preparing the object" pill appears only if a load takes over 1.2s. Collection: tile hover is the original small lift only (the user rejected the tilt + hover shadow; do not reintroduce), "/" focuses search (kbd hint, hidden on touch), live "n of 60" count while searching. Export row: one family, all with a 2px edge shadow (hover lifts 1px, press sinks 1px); Save PNG and Save JSON are identical paper secondaries with a 28px leaf icon circle in both themes (the user may revisit this). Copy: sentence case for interface text (sentence() helper for hints); mono caps only for meta labels (index, category, edition, footer, status, backdrop).

Stable stage: the object caption has a fixed height (title one line with ellipsis, description clamped to exactly 2 lines, full text in its title attribute) so the stage keeps one size for every object. Keep new descriptions to about two lines.

Secondary export buttons (Save PNG, Save JSON) share one subtle hover border: --secondary-hover-border (80% line mixed with muted).

Secondary button component: .btn-secondary is the ONLY source of a quiet button's surface, border, edge shadow, hover, press and focus (tokens --secondary-border, --secondary-hover-border). Used by Read the guide / Back to the studio (header), Save PNG, Save JSON and the round reset-view button. Never style those properties on the individual button classes again; any new quiet button gets .btn-secondary and a design-system specimen.

Chip component: .chip-option is the one source for pill chips with a round visual on the left (paper surface, line border, hover border + 2px edge, focus ring, selected = ink ring). Variants: .color-control (colour picker, hex tag on hover) and .light-option (light preset; lit-sphere swatch built by lightChip()/lightSwatch() in viewer/chips.js, shared with the design system page). Labels wrap to two lines rather than truncating.

Selected state: every pick-one option (palette, .chip-option colour/light chips, backdrop dots) uses one 1px ink border/ring via --selected-border — never doubled or filled. Filled ink is reserved for segmented filters (category chips, export platforms). Keyboard focus shows the accent ring only with :focus-visible; clicking never leaves a dark border behind.
Chips share the secondary-button border tokens: .chip-option rests on --secondary-border and hovers to --secondary-hover-border, with no shadow on hover (no edge shadow at all on chips).

Theme control: the header pill switch was removed. Light/dark is a standard .switch (`.switch.theme-toggle`, input[data-theme-toggle], moon icon, "DARK MODE" in footer mono caps) placed in the header nav before the Read the guide / Back to the studio button, stamped by the header component (the user moved it from the footer to the nav); all pages bind to [data-theme-toggle].

Motion controls (0.13): the main studio row has a shared native Still / Hover / Loop radio control plus Mouse follow and Exploded view switches. Turntable and Orbit frame live under Fine-tune → View. Build the radio and view switches through viewer/motion-controls.js in both the studio and design-system specimens. Map legacy explodeOnHover/explodeHold state through motionFromState/motionState; preserve export semantics, reset to Hover, and keep the orbit frame off by default. --fs-2xs aliases --fs-xs, establishing a 10px minimum without changing the established scale.

The owner now explicitly authorized generating his avatar from his supplied photo and character references. Latest direction: no cap or pencil, normal aligned eyes, and a clearly stylized clay avatar rather than a realistic portrait. Use a different muted pastel palette. Preserve his likeness, glasses, swept hair and neat facial hair. Keep variations under branding/avatars; the chosen footer PNG remains assets/brand/nayeemur-r-s-3d.png.

Theme control (final): the original pill .theme-switch with sun/moon [data-theme-choice] buttons in the header nav. A toggle-switch version was tried (footer, then nav) and the user preferred the pill. Theme changes apply instantly with CSS colour transitions (startViewTransition removed for reliability).

Motion control (.motion-control / .motion-options, viewer/motion-controls.js): styled like the theme pill — stage-coloured track with a line border and an ink thumb that slides between Still / Hover / Loop (selected text in bone). The earlier outlined-segment look was rejected as visually poor.
Motion label: "Motion" is a .badge (leaf pill) in the sans font, sentence case, muted — same type as the Fine-tune hint — sitting on the top edge of the segmented control, like the collection count badge — not beside it, not as plain text above.
Badge component: .badge (leaf fill, mono, pill) is the one style for count badges (Collection 60) and control labels.

Final avatar selection supersedes exploration directions: the owner approved the exact green-background blue-crewneck portrait and the exact lavender-background yellow-beanie floating head. Preserve both unchanged as branding/avatars/nayeemur-portrait-green-final.png and nayeemur-beanie-pastel-final.png. The green portrait is the footer default (assets/brand/nayeemur-r-s-3d.png); the beanie is an approved alternative (assets/brand/nayeemur-r-s-3d-beanie.png). Production files are resized derivatives only; do not redraw either approved image.

Full-bleed dividers: horizontal lines inside the side columns (search underline, settings section dividers) run edge to edge between the frame line and the column divider; content keeps 20px padding (--col-pad). Applies at 561px and up.
Motion control has no visible label (tried beside, above, and as a badge; the user removed it). It keeps aria-label="Motion" for screen readers.
