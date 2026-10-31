# Grow a library, keep a point of view

The product idea is an editable object collection: a designer can find an object, match a brand palette, choose a light rig, and either export an image or embed the interactive model. A consistent style, simple controls and reliable delivery make the collection useful.

## Visual rules for every new object

- Start with a recognizable silhouette at 64px. Pick an everyday object with an expressive form.
- Use soft industrial shapes, visible material separation and a small number of deliberate details. Avoid brand-specific product silhouettes, logos and copied source meshes.
- Keep base color separate from highlights and shadows. Author solid PBR colors and runtime lights so buyers can recolor and relight the object.
- Reuse the semantic material slot names in QUALITY-STANDARD.md. Do not bake the palette into image textures.
- Keep the same floor origin, scale convention, naming and preview angle. Use `catalog.json` for search and integration metadata.
- Target a practical mesh budget based on the object. The current high-detail studies need measured optimization for their intended device; do not set a mesh budget by increasing polygons alone.
- Inspect the object from the front, side, rear and underside. Accept intentional intersections only when they remain clean in the intended illustration views.
- Review a contact sheet after each batch. The collection must feel authored as a family.

## Expansion backlog: 120 new silhouettes

These are planned objects, not files already delivered. Adding them would bring the library from 60 to 180 distinct base objects. Palette variants would still not count as new objects.

| Collection | Twenty potential additions |
| --- | --- |
| Creative studio | Scissors, utility knife, ruler, drawing compass, sketchbook, paint palette, paint tube, brush pot, stamp, ink bottle, paper tray, binder clip, hole punch, bookend, document folder, desk organizer, magnifying glass, rotary sharpener, drafting triangle, paper roll |
| Audio and technology | Turntable, cassette player, tape cassette, vinyl record, handheld recorder, sound mixer, projector, portable drive, router, charging dock, walkie-talkie, desk telephone, smartwatch, trackball, graphics tablet, camera flash, camcorder, film canister, computer mouse, power bank |
| Home and kitchen | French press, teapot, water jug, colander, saucepan, frying pan, knife block, chopping board, rolling pin, whisk, oven mitt, timer dial, butter dish, sugar bowl, honey jar, oil cruet, cookie jar, lemon squeezer, mortar and pestle, countertop mixer |
| Commerce and work | Handcart, warehouse shelf, barcode scanner, checkout bell, open sign, coin purse, wallet, shopping cart, packing tape gun, envelope, mailbox, delivery van, forklift, cash register, display pedestal, product bottle, shipping tube, clothes hanger, folded T-shirt, safety cone |
| Outdoors and travel | Hiking boot, water canteen, tent, camping stove, sleeping bag, trail map, carabiner, pocket knife, head torch, thermos flask, picnic basket, fishing reel, beach umbrella, snorkeling mask, swim ring, bicycle helmet, trekking pole, binocular case, luggage tag, folding chair |
| Play and expression | Spinning top, yo-yo, chess knight, chess rook, chess pawn, die, puzzle cube, maraca, tambourine, toy train, spinning pinwheel, paper plane sculpture, balloon dog sculpture, trophy, medal, heart sculpture, star sculpture, floating ring stack, abstract knot, ceramic cactus |

## Production sequence

1. Finish one object at a time against the approved camera, including its natural behavior. The bound-book study replaces separated slabs with hinges and turning leaves. Prioritize a small coherent curated selection before expansion.
2. Test the editing and download experience with a few designers using those hero objects. Observe whether they want PNGs, editable 3D, a website component or all three.
3. Release the 60-object collection with accurate previews and supported formats.
4. Add new silhouettes in coherent batches of 10–20. Generate metadata, previews and validation in the same build.
5. Add native integrations only when the audience asks for them: a React wrapper, a Framer code component or a Spline version are separate integration projects that need their own testing.

## A sensible product structure to test

| Offering | Contents |
| --- | --- |
| Free sampler | A handful of the strongest objects, PNGs and a working interaction demo. |
| Illustration collection | All 60 PNGs plus curated palette/lighting renders. |
| Interactive collection | All 60 GLBs, the viewer, palette/light settings and embedding documentation. |
| Studio/source tier | Generator recipes and a clearly defined team or client-work license. |

These are suggested packaging experiments. Pricing, audience demand and conversion have not been researched or validated. Choose a price after comparing the products you actually want to compete with and testing the paid offer with buyers.

## Listing copy starting point

**Everyday objects with a little personality.**

A collection of 60 editable 3D illustrations for websites, product interfaces and presentations. Change colors and surface finishes, move the studio light, soften the shadow, and export a transparent image. Use the included HTML component to add gentle mouse response and drag rotation to a website.

**Includes:** 60 GLB models, 60 transparent 1024px PNGs, a 2048px PNG export tool, six palettes, five light presets, a browser studio, a plain HTML embed component and editable procedural source.

Use this copy only after release checks are complete and your final product tiers and license are defined. Promise only the integrations and devices you have tested.
