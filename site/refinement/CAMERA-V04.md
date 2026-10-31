# Camera benchmark / 0.4.0

This is the next visual-quality study after the first collection and its shared geometry pass. Only the camera has been rebuilt to this construction standard. The full collection should not yet be described as having a uniform premium finish.

## What the supplied recording showed

The reference separates meaningful assemblies. The camera opens into front cover, telescoping optical elements, rear housing and a rising film-like insert. The lamp separates its shade, small connector/fittings and stem; the pot lifts its lid. The parts remain related spatially instead of spreading as unrelated primitives. The reference also rotates the objects and changes the framing while the parts move. These observations informed this study; the reference's source assets and code were not extracted or reused.

## Geometry changes

- A tall pearl camera with a continuous lofted front cover and a true circular optical opening.
- A hollow rear tray with curved sides, an internal floor, and a separate gasket at the cover seam.
- An inner PCB/chassis with recessed components and a film cartridge that can rise out of the body.
- A periwinkle lens mount with a continuous curved annular profile, focusing sleeve, retaining ring, six-blade iris and a transparent curved window.
- A recessed viewfinder, ribbed flash diffuser, rounded shutter control, film slot and side fittings.
- A lower camera viewing angle and cool silver fittings instead of the previous cream-and-brass treatment.

The benchmark contains about 280,000 triangles and is about 7.1 MB as a GLB. It is intentionally a high-detail review model. Its web delivery should receive a measured optimization/LOD pass after the finish is approved.

## Material and motion changes

The viewer now draws opaque geometry before transparent optical surfaces and retains glass opacity when a color changes or a GLB is exported. The camera's glass window uses alpha blending and Fresnel-like reflections; it is not a physically refractive/path-traced optical simulation. The renderer still uses analytic studio reflections and shadow maps.

Authored mesh groups carry short opening delays. The front cover leads, the lens elements follow, and the film cartridge/top cap reveal the inner body. Reassembly reverses the ordering. A slight coordinated yaw makes the separation easier to read. Hover/hold-open/separation controls remain available. Reduced-motion preferences take priority.

`Product studio` is a new light preset. The revised `Cobalt` palette is a pearl/periwinkle/silver study. The current raster PNG and GIF are CPU-rendered illustrations of the same geometry and group offsets; the live viewer uses WebGL and can differ slightly in shading and timing.

The previous camera GLB, PNG and renderer source are retained in `refinement/before-v04/`. `reports/studies/CAMERA-QUALITY-STUDY.png` shows the prior camera beside this study. The camera's catalog ID remains `rangefinder-camera` so existing links continue to work.
