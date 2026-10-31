# Refinement pass / 0.2.0

The first collection was created procedurally. It was not modeled by hand in Blender or sculpted by an artist. The first pass had visibly coarse corners, stepped curved profiles and point-like specular highlights; describing it as a finished premium product would have overstated the work.

This revision keeps the studio interface and improves the asset foundations:

- The rounded-box topology concentrates eight subdivisions in each bevel region instead of spacing a small number of vertices uniformly across the entire face.
- Spheres, tubes and toroidal parts use smoother curved sections. Cylinders have multi-segment rounded rims instead of single chamfer segments.
- The dome lamp has an individually revised continuous shade, rolled rim, recessed diffuser, integrated flared stem and base, small switch and inset rubber foot.
- The rangefinder has a revised shell, inset grip panels, rear panel, recessed viewfinder, layered lens barrel, convex optical surface, knurled control, shutter assembly, screws and strap loops. A painted-on white reflection dot was removed.
- The radio has a revised soft enclosure, a perforated grille with actual openings and wall depth, inset tuner and dial, telescoping antenna, denser curved handle and rubber feet.
- The viewer uses broad analytic softbox reflections in place of point-sized specular glints. These remain a lightweight approximation of a studio environment, not path tracing or a captured HDRI.
- All 60 models inherit the denser shared corner and curve geometry. Three hero objects received individual construction revisions; the other 57 have not each received an equivalent detailed art-direction pass.

The denser geometry increases the collection from roughly 416,000 to 1.99 million triangles in total, and the GLB files from about 11.6 MB to 50.5 MB. That tradeoff makes the curved silhouettes smoother. A future release should offer optimized LODs after measuring the intended device and viewport sizes.

`reports/studies/REFINEMENT-COMPARISON.png` compares the original three PNGs with this revision. The render treatment changed alongside the geometry, so this is a comparison of the full visual pass, not an isolated geometry experiment. The earlier generator is preserved in `refinement/build_pack_v01.py` for reference; it is not a separate set of delivered models.

This remains an art-direction review edition. Further individual model cleanup, reference checks and production integration testing are still needed before claiming a uniformly hand-finished professional collection.

## Layer motion / 0.3.0

Each mesh now carries a named layer and an explosion offset in GLB extras. The viewer animates those offsets on pointer entry with a damped spring, reverses them on pointer leave, and keeps lighting/shadows attached to the moving parts. A hold-open control supports touch and static inspection, and spacing is adjustable. Camera, radio and lamp groups are authored individually; the other models use general upper/lower/detail offsets.

The viewer widens the framing and lifts the assembly as needed so lowered parts remain above the floor. Automatic motion is disabled under a reduced-motion preference; explicit hold-open changes snap to the requested state. This is illustrative separation of the supplied model parts, not a representation of how to repair or manufacture a real product.
