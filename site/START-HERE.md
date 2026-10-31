# threed® / Volume 01

An original library of 60 editable 3D object studies in six families. Version
0.7.0 uses restrained default motion throughout: small gestures from real use, with
attached parts staying attached. The camera remains the finish benchmark; other
objects are still individual studies. This is a working review edition.

## What is included

- **60 distinct GLB models**, with editable geometry and named material slots. These are actual 3D meshes, not images on rotating planes.
- **60 transparent PNG illustrations at 1024 × 1024**, with soft shadows, in `renders/`.
- **360 gallery thumbnails across six Color Stories**, plus `CONTACT-SHEET.png` showing the full collection.
- **Six shared palettes**: Workshop, Cobalt, Cherry, Butter, Lilac and Graphite.
- **Five light rigs**: Softbox, Daylight, Golden hour, Gallery and Product studio.
- **Local customization studio**: recoloring, surface finishes, light direction, elevation, strength, fill, warmth, shadow density and softness, mouse response, drag rotation and keyboard rotation.
- **Exports from the studio**: edited GLB; cutout dropdown with Download or Copy PNG, and scene-settings dropdown with Download or Copy code. The cutout downloads or copies a 2048 × 2048 transparent PNG with shadow. Scene settings download the JSON recipe or copy a self-contained live 3D HTML embed for Framer’s Embed → HTML field.
- **Guide-page embed tool** with Framer and Webflow instructions, copyable live embed code and URL, a downloadable Framer code component with controls, a standalone embed player, an HTML embed component, an embedding example, and an original button kit with outline, tactile and restrained magnetic treatments.
- **Editable Python generator** with individual category recipes and a specific-object rebuild command; no Blender installation is needed to regenerate the GLBs.

There are 60 base objects. Palettes and light rigs are presets, not additional unique models. No source meshes, code, images or brand assets were extracted from Shopify.

## Open the studio

In Terminal, change to this folder and run:

```sh
python3 serve.py
```

Open **http://localhost:8765**. The server binds only to your own computer. Press Control-C in Terminal to stop it. An alternative port is supported: `python3 serve.py --port 8766`.

Opening `index.html` by double-clicking it may block model loading because browsers restrict local module/file access. The included server avoids that restriction. The studio uses no external services, fonts, packages, analytics or network dependencies. WebGL 2 with hardware acceleration is required for the live 3D view; the PNG files are usable without it.

## Appearance and identity

The supplied smiling **threed®** identity appears in both themes. The icon-only sun and moon controls switch the interface, stage and gallery between light and dark. A contrasting circular highlight indicates the active mode; changes animate, with reduced-motion support. Color Story remains independent of appearance.

Everything is organized under `threed/`: this studio is in `site/`, identity assets and approval previews are in `branding/`, and packaged downloads are in `downloads/`. The 3D EE is now integrated inside the wordmark, in the user supplied warm orange, with idle and hover/focus smiling expressions. Reduced motion leaves it static. The other two EE concepts remain alternative studies. The existing studio address and former project path remain compatible.

The lamps have no trailing wires. Gallery names and indices sit side by side. Range tracks fill to their current value; settings scrollers leave room for control and focus outlines. The download row remains 40px below the interaction controls.

## Collections

| Family | Objects |
| --- | --- |
| Desk | Dome lamp, task lamp, pencil cup, stapler, pocket notebook, calculator, tape dispenser, alarm clock, sand timer, fountain pen |
| Devices | Studio camera, portable radio, headphones, game controller, bookshelf speaker, desktop display, keyboard, pocket console, studio microphone, web camera |
| Kitchen | Pour-over kettle, stovetop brewer, toaster, lidded pot, blender, espresso cup, insulated bottle, citrus press, kitchen scale, pepper mill |
| Commerce | Shopping tote, ribbon gift, payment terminal, delivery parcel, market basket, price tag, coin stack, storefront, receipt printer, piggy bank |
| Travel | Cabin suitcase, backpack, binoculars, pocket compass, camp lantern, travel mug, passport wallet, sunglasses, sun cap, key fob |
| Play | Orbit sculpture, stacking rings, little rocket, rubber duck, tiny robot, cloud sculpture, ceramic rainbow, flower vase, wind-up bird, balance mobile |

## Editing colors, lights and shadows

The semantic mesh material slots include `body`, `accent`, `secondary`, `ink`, `metal`, `lens`, `paper`, `rubber`, `glass`, `circuit`, `fabric`, `leather`, `coffee` and `sand`. Each object uses only the slots it needs. Choosing a Color Story updates all collection thumbnails and remains selected as you switch objects or reload. Individual material edits also carry to the next object by material name. A surface preset overrides roughness and metallic values across the object. Return to **Object original** to restore the authored surface values while retaining color edits.

Material colors are stored in linear space inside the GLB and shown as sRGB hex colors in the UI. The studio includes an approximate studio environment and procedural highlights; it does not use path tracing or an HDR environment map. The CPU-rendered previews and live WebGL view will differ slightly in lighting and finish.

Mouse follow makes a subtle spring-like tilt. **Animate on hover** plays the object's authored interaction and returns it when the cursor leaves. **Keep active** keeps that state visible, including on touch devices. **Interaction amount** controls its extent.

All sixty objects now use restrained functional motion. The camera focuses and
presses its shutter; the bound books lift their covers and flutter thin leaves;
the blender spins its blades inside a closed base and jar; the payment terminal
slides a card while its keys wave. Tape feeds from its roll, sand runs inside a
fixed hourglass frame, toast rises from real slots, lids move with their fittings,
and a lantern lights up. There are no default exploded views. **Explode** opens an optional authored inspection pose for every icon. Use **Assemble** to return; selecting another icon or reloading starts assembled. The default hover stays functional. Older stills and GIFs with "exploded" or "layers" in their names are historical studies.

Drag rotates more freely. Focus the canvas and use the arrow keys to rotate, Shift+arrows for a larger step, and Home to reset. Turntable and automatic hover motion respect the browser's reduced-motion preference. With reduced motion enabled, Keep active shows a static functional pose immediately. Mouse interaction is **viewer behavior**, not a baked animation clip in the GLB file. Assembly names and functional motion metadata are retained as mesh extras inside the GLB.

The studio remembers the most recently selected object and edits in that browser. A downloaded scene recipe records the chosen materials, lighting, view rotation and viewer options. It is an editable configuration file; the current studio does not have a recipe-import control.

## Platform guides

Open **Read the guide** in the header, or visit [guide.html](guide.html), for
Framer, Webflow and custom website instructions. The guide includes official
platform logos, format selection, hosting and troubleshooting for Lottie uploads.

## Use an object in Framer

Open **Read the guide → Prepare your embed**. It previews your current
materials, lighting and view with Still / On hover / Loop, light / dark and
transparent / solid background options. Copy the embed code into Framer's
**Insert → Embed → HTML**, or download **Threed.tsx** for a code component with
Framer property controls. Set Library URL to your hosted HTTPS library address;
localhost is local preview only. See [the Framer guide](integrations/framer/README.md).

For a still illustration, use **Save PNG** in an image layer. GLB models
and scene JSON recipes cannot be played by a Lottie component. The pack does not
export SVG path animations or Lottie files. The component has been checked locally
with React/Framer stubs; importing into Framer and publishing on either platform
still require end-to-end verification.

## Use an object on a website

Copy the `viewer/` folder and your chosen `models/` files to your own site and serve them over HTTP(S). For example:

```html
<script type="module" src="viewer/little-object.js"></script>
<little-object
  src="models/rangefinder-camera.glb"
  body="#e8e4d8"
  secondary="#a2b1dc"
  accent="#3054d7"
  azimuth="-40"
  elevation="48"
  intensity="3"
  fill="0.65"
  warmth="0.15"
  shadow="0.55"
  softness="2.5"
  label="Interactive camera. Drag or use arrow keys to rotate."
  style="height:420px"
></little-object>
```

Try `embed-example.html`. Optional attributes include `background="#1529b6"`, `follow="false"` and `spin="true"`.

Functional hover motion is enabled by default. The existing embed attributes stay
compatible: `explode="false"` disables hover actions, `hold-open="true"` keeps
an action active, and `separation="1.0"` controls its amount. These legacy API
names now drive purposeful gestures. Exported GLBs stay assembled and carry
functional motion metadata; use the included viewer to reproduce it.

```js
const object = document.querySelector('little-object');
object.setMaterial('accent', '#a82e40');
object.setOptions({ intensity: 3.5, shadow: 0.7, softness: 3 });
object.resetView();
```

Wait for `object-ready` before calling `setMaterial()` in integration code. The element dispatches `object-error` if loading fails. It disposes its GPU resources when removed from the page. Use PNG thumbnails for large galleries and activate only one or a few 3D views at once: each active instance uses a WebGL context and a 2048px shadow map.

The included renderer is intentionally limited to this pack's indexed geometry, PBR colors, alpha-blended glass and authored hinge/page metadata. For broader glTF support, richer environment lighting, animation or a large production application, use an established engine such as Three.js and retain this pack's material naming conventions. Three.js is not bundled here.

## Technical conventions

- Binary glTF 2.0, indexed triangle meshes with positions and smooth normals.
- Y up; centered horizontally; floor at Y = 0. Longest dimension normalized to 2 display units. This is a presentation scale, not real-world product measurement.
- Separate, named mesh parts and named PBR material slots. No image textures, UV unwraps, skeletal rigs or baked animations are included.
- Overlapping and open meshes are intentional in places. These assets are intended for illustration and screen rendering, not manufacturing or 3D printing.
- GLB files can be imported into a 3D editor for further art direction. No native `.blend`, `.spline` or `.fig` files are included. The downloadable Framer code component wraps the hosted live embed; a published Framer project still needs end-to-end verification.
- Light position, environment fill, contact shadows and pointer behavior are configured at runtime. A GLB export carries geometry and material edits. A PNG is a flattened render. A scene recipe is needed to describe the intended lighting and interaction.
- The `lens` slot is a dark glossy solid material. The new camera also has a transparent `glass` slot with Fresnel-like studio reflections and visible aperture blades behind it. It uses alpha blending rather than physically refractive ray tracing. Its `circuit` slot colors the internal board. Material presets offer metal, enamel, satin and clay-like appearances.

## Rebuild or expand

```sh
python3 source/rebuild_object.py pocket-notebook
python3 source/render_previews.py --size 1024 --only pocket-notebook
python3 source/quality_review.py --category Desk
python3 source/validate_pack.py
node source/validate_collection_export.mjs
node source/validate_book_motion.mjs
```

The model generator uses only the Python standard library. Preview rendering requires NumPy and Pillow. Building resets the GLB files to the authored original palette. The PNG renderer uses deterministic studio shading and a soft illustrative ground shadow; the viewer uses dynamic shadow maps.

Work on one object at a time. Use `source/object_registry.json` and its category recipe, and read `docs/QUALITY-STANDARD.md` before adding future icons. `python3 source/build_pack.py` regenerates the entire draft collection; it does not establish curation status. Review close-up geometry and natural motion before moving to the next silhouette. Read `docs/EXPANSION-PLAN.md` for the broader backlog.

## Before selling

The product name is threed®. Finalize the seller identity, approve the remaining object art direction, finalize the customer license, test your supported applications and browsers, and build the product listing around the actual included files. `CUSTOMER-LICENSE-DRAFT.md` is a decision template, not an active license. See `docs/RELEASE-CHECKLIST.md` for the remaining product work.

The design reference was [Shopify Editions Fall 2026](https://www.shopify.com/editions/fall2026). The collection is an original interpretation of rounded everyday objects and tactile controls. It is not affiliated with Shopify.

Reference documentation: [Three.js physical materials](https://threejs.org/docs/pages/MeshPhysicalMaterial.html), [GLTFExporter](https://threejs.org/docs/pages/GLTFExporter.html), [Blender glTF export](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html). These are integration references; they are not dependencies of this pack.
