# Smiling EE — three 3D studies

The user authorized integration. Soft keys is the implemented direction, replacing only the EE inside the supplied wordmark. The header version has warm orange faces for contrast and a real lip/crescent-eye smile deformation. Other concepts remain alternatives.

1. **Soft keys:** sage caps, ivory bases and a thin coral gasket.
2. **Porcelain twins:** ivory ceramic and coral reverse, deeper sculptural letters.
3. **Ink cushions:** plump ink forms and a soft breathing gesture; the preview reverses this material to ivory in dark mode.

`preview.html` includes idle and hover behavior, drag rotation, light/dark backgrounds, pause and reduced-motion support. Open http://localhost:8765/studies/smiling-ee/preview.html while the local studio runs.

`models/` contains editable GLB geometry with semantic materials and motion metadata. `renders/` contains transparent 1024px renders. `source/build_studies.py` rebuilds actual curved geometry from the supplied logo contours, using rounded extrusion and marching tetrahedra; it does not use raster billboards. Run it in the bundled Python environment with NumPy and Pillow.

The crescent eyes and shared smile are real cutouts. GLBs are assembled static geometry; motion metadata is interpreted by the included renderer. These three study masters remain separate from the 60-object catalog. The downloadable site includes the smaller header variant in `assets/brand/ee-soft-keys.glb`.

Geometry validation reports no non-manifold edges or collapsed triangles, with finite positions and unit normals for all three GLBs. Run `source/validate_studies.py` to repeat it.
