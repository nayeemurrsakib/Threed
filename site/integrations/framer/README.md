# Use threed® in Framer

## Why the Lottie component is blank

The studio downloads GLB models and JSON scene settings. Neither is a Lottie
animation. A scene recipe describes a threed® viewer configuration; renaming it
to `.lottie` or uploading it to a Lottie component does not convert it.

| What you need | Use this | Where it goes in Framer |
| --- | --- | --- |
| A still illustration | Save PNG | An image layer |
| Functional hover or looping 3D | Guide → Prepare your embed · Copy embed code | Insert → Embed → HTML |
| Controls inside Framer | Guide → Prepare your embed · Download Framer component | A new code file, then add Threed to the canvas |
| Editable mesh for a 3D editor | Save 3D object · GLB | A compatible 3D editor |
| Stored studio settings | Save JSON · JSON | Configuration data; not a Lottie player |

## Copy a self-contained 3D embed

In the studio, open **Save JSON → Copy code**. Paste the result into
Framer's **Embed → HTML** field. This is renderable HTML containing the viewer,
compressed edited model, lighting and view. It does not fetch localhost assets.
The code can be several megabytes, depending on the model. The hosted method
below keeps the pasted snippet small; use that method for Webflow's Code Embed.
**Download** on scene settings still saves JSON configuration, which a visual
embed cannot render by itself. **Copy PNG** on the cutout copies actual image data.

## Hosted path: an Embed

1. Select an object in the studio. Choose its colors, surface finish, lighting,
   shadow and view.
2. Open **Prepare your embed** in the platform guide, then choose Still, On hover or Loop. Choose a transparent
   backdrop to blend into the Framer page, or select a solid background.
3. Set **Library URL** to the HTTPS address where this library is hosted.
   `http://localhost:8765/` works for local development on your own computer only;
   it is not an address your published site's visitors can access.
4. Copy the embed code. In Framer, use **Insert → Embed**, select its HTML input,
   and paste the code. Give the Embed a width and height, such as 400 × 400.
5. Preview the Framer page. Hover or drag the object. Keyboard users can focus the
   object and use arrow keys; Home resets the view.

The embed preserves the current model, named materials (including glass alpha),
surface overrides, lighting, shadow and camera orientation. The production URL
is used only in copied/downloaded exports; the studio preview uses its local
runtime so you can inspect the configuration before hosting.

Use **Apply current studio edits** to refresh the open export panel after editing
the main studio. Selecting a different object also refreshes it.

## A component with Framer controls

Download **Threed.tsx** from the customized object's export panel. Create a code
file in your Framer project and paste the full file into it. Add the exported
**Threed** component to your page. It exposes:

- Library URL and object ID (the catalog ID, for example `rangefinder-camera`).
- Body, secondary and accent color overrides; leave a color unset to keep the
  saved material. Other materials retain the downloaded snapshot.
- Light / dark appearance, transparent / solid backdrop and backdrop color.
- Still / Hover / Loop, interaction amount, mouse follow and turntable.
- Light strength and shadow density.

The component loads the same hosted embed in an iframe, keeping renderer modules
out of the Framer build. Changing an object ID retains overrides by material name.
Download a fresh component from that object's studio if you want its exact current
materials and view. The generic `Threed.tsx` in this folder starts with a camera
and an empty Library URL; the studio download fills both from your selection.

Still disables automatic motion and mouse follow while retaining manual drag.
Hover follows the object's authored functional action. Loop repeats that action
with a pause and return to rest. Reduced-motion preferences stop automatic loops
and turntable. Optional exploded views stay off.

## Hosting

Serve the site folder over HTTPS, preserving `embed.html`, `catalog.json`,
`viewer/`, and `models/` at their existing relative paths. Any subfolder is fine:
enter its full trailing-slash URL in Library URL. The host must allow iframe
embedding (its CSP / frame-ancestor and X-Frame-Options headers must permit your
Framer domain). This integration does not publish or upload anything for you.

## Formats

PNG is a flattened image. Live 3D uses WebGL 2 and the included viewer; use only a
few live objects on a page and PNGs for large grids. SVG path-drawing animation
and Lottie export are not provided. A shaded 3D render would need a separate
conversion/rendering pipeline rather than a different filename.

References: [Framer Embed](https://www.framer.com/help/articles/how-to-add-an-iframe-or-embed-script/),
[Framer property controls](https://www.framer.com/developers/property-controls),
[dotLottie format](https://dotlottie.io/spec/2.0/).
