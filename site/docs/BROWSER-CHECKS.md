# Review-edition checks

## Asset checks

`source/validate_pack.py` passes for 60 unique GLBs and 60 transparent 1024px PNGs. It checks binary glTF structure, accessor alignment and bounds, finite positions, unit normals, valid indices and materials, named finite explosion vectors, floor origins, display scale, file uniqueness and PNG dimensions/alpha channel. See `VALIDATION.json`.

## Browser checks performed

- The studio renders the revised camera, radio and lamp without reported WebGL/shader errors in the Codex in-app browser.
- Palette, finish and light-preset changes update the object.
- The first viewer revision's edited GLB download was read back and checked for geometry validity and retained color/roughness values; its downloaded PNG was checked as 2048 × 2048 RGBA with transparent and opaque pixels.
- The refined viewer's hover interaction was observed entering the separated state at 0.85 and returning to the assembled state at 0.00 after the pointer left.
- Hold layers open works independently of hover. Camera lens rings, rear panel, grips, viewfinder, top dial and shutter separate as authored.
- Shadow rendering follows the translated parts. The scene lifts enough to keep lowered parts above the floor, and framing widens with separation.
- Desktop and 390px mobile layouts were inspected. Mobile has no horizontal document overflow; the Hold layers open control works in the narrow layout.
- The button demo's palette, spin, and next-object actions were checked; the component rendered without reported errors during those checks.
- JavaScript module syntax checks pass for the modified renderer, studio and custom element modules.

This is not a full cross-browser/device certification, a production performance benchmark, or a Khronos validator report. All 60 files received structural checks; only representative objects received live visual inspection.

## Camera study / 0.4.0

The new camera was inspected assembled and expanded in the live viewer. It renders without reported shader/WebGL errors, and its hollow covers, film insert and optical layers are visible when expanded. The material pipeline now draws transparent optics after opaque parts. Opening uses authored per-group delays and reassembly reverses their order; a coordinated yaw accompanies the separation.

`source/validate_camera_export.mjs` recolors the camera's glass and body through the actual renderer methods, re-exports the GLB, reads it back and checks that the transparent material's BLEND mode, 0.08 alpha, layer delays and hollow-front-cover mesh are retained. The exported file also passes the pack's structural geometry checks with 280,220 triangles.


## Bound-book study / 0.5.1

The notebook was inspected closed and open in the live WebGL viewer. The cover
hinges at the spine; three thin leaves turn with curvature. Printed rules share
the leaf deformation. Leaving hover returns to the assembled state at 0.00;
Hold open retains the interaction at 0.85. The shader and shadow pass share the
same page deformation. No shader errors were reported during the live check. The cloth cover was recolored with the Cherry palette; the printed rules followed the turned leaves. At a 390px viewport, the document stayed 390px wide and Hold open worked without hover. The viewport override was reset afterward.

`source/validate_book_motion.mjs` checks both book models at four interaction
amounts: the spine remains invariant, leaf curvature is finite, there are three
turning leaves and no translated layer fallback. The full collection also passes
recolor and finish round trips through the actual studio exporter. These tests
verify behavior and file integrity, not curation status.

The 60-object broad pass has authored assemblies and newly rendered review
boards, but it is not an individually curated release. See
`refinement/COLLECTION-V05.md` for current defects and statuses. The camera is the
only user-approved benchmark. Other object motions still require individual art
direction rather than applying the book's hinge behavior indiscriminately.

## 0.6.1 / functional hover and studio corrections

Live WebGL checks: fitted radio front; connected headphones; continuous controller
grip; closed webcam front; pot handles and lid; complete bottle loop; sewn tote
and cap; whole kettle with spout-attached water; feeding paper; lantern glow;
small rocket lift/flame; fixed sand frame with transfer and paused action clock.
Blender stays closed and its blade assembly rotates; terminal card feeds through
the slot while its keys wave. All 60 models have explicit gestures and no
generic separation vectors. Review boards show rest/active poses in six families.

Selected Workshop, switched objects and reloaded: palette stayed selected.
Selected Cherry: gallery image paths changed to Cherry and loaded successfully.
Edited the secondary material: 60 custom thumbnail blobs were generated; the
same hex color was present on the next object that uses that material and after
a reload. Presets cancel custom rendering. No error/warning logs in final check.

The removed intro is absent. Measured interaction-bar to export-bar gap: 40 CSS
pixels. The gallery grid computes overflow:visible, with a padded outer scroller
to protect selection and focus outlines. Scene settings computes a 999px corner
radius. Cutout download has its own PNG icon and treatment. See
refinement/STUDIO-UPDATE.png. Existing branding remains pending user assets.

## Rotation / ground clipping correction

The fixed Y=0 shadow receiver could occlude the keyboard's lower rows after a
downward tilt. The receiver now follows the minimum height of the final rotated
vertices, including page bend and functional motion. Resting geometry anchors
the receiver so lift gestures retain clearance. The orbit center stays fixed.
The same receiver transform is used for its rendered surface and shadow lookup.

The regression reproduces the old keyboard intersection and checks all 60 models
at five pitches, two yaws and resting/active/optional blast amounts (1,800 poses). No posed
vertex falls under the receiver. Live WebGL verification covers positive/negative
keyboard pitch, a side angle and key motion. See reports/validation/ROTATION-VALIDATION.json and
refinement/ROTATION-FIX.png.

## 0.7.0 / threed® studio

Applied the user supplied smiling identity. Theme controls are icon-only, with 36×36 circular buttons and a 36×36 sliding selected disc; the guide remains last. Removed download and guide arrows, centered the reset SVG, and removed the duplicate header divider. Range tracks reflect values. Settings have 16px right clearance inside their scroller, including room for the 6px focus outline and overlay scrollbar. Gallery names and indices share a row.

Optional authored Explode poses exist on all sixty icons; normal hover stays functional and assembled. Object changes and reloads reset the optional pose. Latest lamp models and all twelve lamp palette thumbnails omit the wires. Desk review hashes were refreshed.

The project now lives in `threed/site`; a compatibility symlink preserves the old local server path. The 3D EE models are isolated in `branding/3d-studies/smiling-ee`, served through `site/studies`, and explicitly excluded from the customer archive pending approval.

## October 31 / field padding, canvas labels and headphones

Material finish keeps its native select behavior with a separate inert chevron, 12px from the right edge; text has 12px left padding and reserves space for the icon. Search focus surrounds the complete field, including its search icon, with 10px horizontal padding. Filtering and finish selection were checked live in both appearance themes.

Moved the object index/category row into the stage, 18px from the top on desktop. Removed the four decorative headphone fork strips and changed the exposed headband spring to neutral ink. The headband attaches directly to the earcups; the slight swivel gesture stays intact. Regenerated the headphone model, assembled render, six palette thumbnails and Devices review board. Catalog requests revalidate and preset thumbnails use each asset's current byte count in their cache key so older trim does not remain in the gallery.

The supplied logo attachment matches the current reference byte-for-byte and is retained in `branding/references/user-supplied/threed-wordmark.png` at the project root. The three separate EE proposals still await approval for integration. See `reports/studies/FIELD-HEADPHONE-UPDATE.png` for the live studio check.

## October 31 / inline orange EE, smile, cap and functional gestures

The 3D EE replaces only the paired letters inside the original wordmark. The surrounding letters retain the supplied vector shapes. A static full-wordmark fallback remains available if WebGL fails. A smaller 137,982-triangle header mesh is included under assets/brand, separate from the sixty base objects. The user supplied warm orange is applied in both themes, with an ivory base and darker orange edge. The vertex expression raises the lip corners and squints the crescent eyes; it has a small idle cycle and a stronger pointer/focus response. It is disabled under reduced motion. A minimum deformation Jacobian greater than 0.41 verifies that the smile never folds the mesh.

Speaker cone, dust cap and rubber surround pulse together while the cabinet and basket stay fixed. The scale plate and stem compress under load, then settle through an exponentially decaying bounce, replaying on reactivation. Cap bill roots sit within the sweatband and its side ends taper smoothly into the crown rather than projecting square tabs. The corresponding assembled renders, palette previews and review boards were regenerated.

The browser tab uses a solid rounded tile behind the smiling EE, orange/ink in light mode and ink/peach in dark mode. The favicon follows the saved app theme on initial load and the appearance switch. The title is “threed® — The 3D object library”; collection and object totals are derived from the catalog.

## Framer integration

The studio's Use on a website panel snapshots named materials, lighting, surface
finish and view. Browser checks exercised the camera's transparent hover embed,
loop, still, solid dark backdrop, clipboard confirmation and a downloaded
Threed.tsx containing the actual scene. The player resolves object IDs through
the catalog and leaves exploded views off. Localhost hosting limits are explicit.
`source/validate_embed.mjs` checks round-trip serialization, glass alpha, view,
URL validation, escaped markup and every catalog ID.
`source/validate_framer_component.mjs` executes the TypeScript component with
React/Framer stubs and checks iframe output, setup fallback, RGB conversion,
scene options and property-control definitions. Both checks pass under Node
24.19.0. The stubs do not verify Framer's editor or build runtime; no real Framer
or Webflow import or deployment was performed in this session.

The separate guide.html page is linked from Read the guide and the export panel.
It uses official local Framer/Webflow logos with light/dark variants. Browser
checks covered the actual 689px user viewport, 390px mobile (no horizontal
overflow), and 1440px desktop; platform anchors and disclosure content work.
The studio export panel has Framer/Webflow instructions for the same live embed.
Platform docs were verified against official Framer/Webflow pages on 2026-10-31.

The studio's Use on a website button and inline panel were removed by user
request. Integration controls now live only on guide.html under Prepare your
embed; its real camera preview still loads. Read the guide uses native beveled
3D Framer/Webflow marks, transparent PNGs backed by editable GLB assets in
assets/platforms/3d. Both appearance modes were checked and studio downloads
remain enabled. Source: branding/source/build_platform_marks.py.

Latest header/export adjustments: small 2D Framer/Webflow marks share a 30 × 30px
circular backdrop, with .78 opacity for a softer idle appearance. The guide's
Back to the studio control uses a left arrow. The studio website CTA remains
removed; integration preparation stays on the guide page.

Cutout and scene-settings controls now open Download / Copy code menus. Both
copy actions returned confirmation. Actual downloads were checked: 2048 × 2048
RGBA PNG with transparency, and parsed camera scene JSON. Keyboard opening and
Escape/focus restoration work. At390px, menu bounds remain inside the viewport
(x154..378) with no page overflow. Menus anchor to their button while scrolling,
so focus scrolling cannot close a menu before its action fires.

Latest export behavior supersedes the earlier code-copy description: cutout is
Download / Copy PNG (real image/png clipboard data). Scene settings are Download
(JSON recipe) / Copy code (self-contained live 3D HTML iframe). A copied scene
is no longer raw JSON. The source viewer and gzip model are embedded in srcdoc,
with no external or localhost asset URL. A camera round-trip test verifies gzip
bytes, HTML escaping and script syntax; the resulting isolated browser iframe
renders the camera and reports data-ready=true. Current browser copy actions
confirmed PNG copied and 3D embed copied. The actual Framer project is not
modified by these local tests.

Latest guide CTA: only a small 2D Framer mark in a 30px circle, idle opacity .78,
7px left button padding. The guide back control uses a left arrow.

PNG export regression repair: render to an independent 2048px WebGL framebuffer,
read/flip/unpremultiply into a separate PNG canvas, then release its GPU targets.
The live canvas is never resized and its transparency setting is not mutated.
Two clock PNG copies and one download kept the live dimensions exactly752×800
(376×400 CSS px). The resulting file was verified as2048×2048 RGBA with alpha0..255.
`source/validate_png_export.mjs` covers unchanged canvas/settings, correct
orientation/alpha conversion and framebuffer cleanup. Portable embed validation
also passes after the shared renderer change.

Save PNG / Save JSON are the final button labels, with dropdown chevrons and no
upper labels. Header guide/back buttons match theme-switch height:46px desktop,
44px mobile;390px browser check has no horizontal overflow. Save JSON hover
border uses a muted mix rather than full ink.
