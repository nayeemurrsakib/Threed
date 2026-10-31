# The camera is the benchmark

The approved Studio camera establishes the collection's direction: soft but
precise forms, restrained material changes, fitted details and a satisfying view
of the construction when it opens. The goal is consistency of craft, not making
every material or silhouette look like a camera.

The user has explicitly prioritized curation over speed and quantity. The camera
is the approved benchmark. The other objects are studies, including the new
bound-book motion candidate, until their individual finish is accepted. Work on
one silhouette, inspect it closely, repair its defects and complete its motion
before expanding the batch. A 60-object generator run does not advance that
curation status.

## Shape and surface

Check the silhouette at thumbnail size and the surface at 1024px. Curved forms
must be smooth in silhouette as well as in their vertex normals. Sample small
bevels where the radius actually changes. Use continuous lofts or blended skins
where intersecting primitives would leave unwanted creases. Deliberate facets
are acceptable only when they serve the object.

Show a plausible wall, well, throat or rear surface when an object opens.
Rounded box overlays are useful details, not a substitute for every main form.
Keep purposeful seam widths, rolled rims, shallow insets and small fasteners.
Details should support recognition without becoming noisy at 64–128px.

## Materials and lighting

Use the shared semantic slots and add a new one only for a distinct surface:
`body`, `accent`, `secondary`, `ink`, `metal`, `lens`, `paper`, `rubber`,
`glass`, `circuit`, `fabric`, `leather`, `coffee` and `sand`.

Choose roughness for the material, not for the entire collection. Fabric and
paper stay diffuse; metal reflects; enamel carries broad controlled highlights;
rubber remains soft; glass preserves its authored alpha. Colors and lighting
remain editable. Do not paint fixed highlights into the base color.

Review with Product studio lighting and the object's original finish, then a
second palette and side light. The included renderer uses approximate studio
reflections and alpha blending, not path-traced refraction or manufacturing CAD.

## Motion and assembly

Choose a small gesture from real use. Every object stays assembled. The camera
focuses a little, a book cover lifts at its spine, a pot lid rises slightly, a
printer feeds paper and a lantern lights up. Housings, handles, sewn panels,
eyes, ribbons and labels remain attached. Default hover never uses an exploded view. The separately requested Explode button may open an authored inspection pose for any icon; it starts off and resets when selecting another object. `source/hover_policy.py` defines explicit actions for all IDs and
rejects unknown IDs until their behavior is authored.

Keep matching parts on the same pivot/transform. Covers retain their fittings;
pages remain bound. Use independent planar corner radii for thin fitted panels.
Test the midpoint as well as both ends for intersections. Motion should remain
restrained even with Keep active selected. Preserve interruptible damping and
reduced-motion support. Continuous rotation integrates velocity so the blender
blades stop smoothly without snapping back. Static GLBs retain the assembled
geometry; the included viewer interprets their motion metadata.

## Add a future object

1. Add a stable ID, name, family and accurate description to
   `source/object_registry.json`.
2. Add its individual recipe to the appropriate `source/craft_*.py`. Define the
   silhouette and construction first, then assign material response and groups.
   `prepare()` supplies the shared starting palette; `finish()` checks metadata.
3. Run `python3 source/rebuild_object.py ID` while refining one object. Use
   `python3 source/build_pack.py` only when a whole collection rebuild is needed.
   The exporter rejects ungrouped parts.
   Catalogs, dimensions and assembly lists come from the actual geometry.
4. With a Python environment containing NumPy and Pillow, run
   `python3 source/render_previews.py --size 1024` and
   `python3 source/quality_review.py`. For targeted changes use `--only ID ...`
   on preview rendering and `--category Family` on the board renderer.
5. Visually inspect every assembled/expanded board. Inspect the live object from
   front, side, rear and underneath when that object's construction changes.
   Keep the approved camera next to the candidate as the quality reference.
6. Run `python3 source/validate_pack.py` and
   `node source/validate_collection_export.mjs`; check the live studio, a second
   palette, hover out/in, hold-open and recoloring. Regenerate review evidence
   after a model change; old hashes must not pass as current evidence.
7. Update `refinement/COLLECTION-V05.md` (or the next version's review record),
   documentation and archive with `python3 source/package_pack.py`.

## What the gate proves

Structural validation checks geometry, materials, authored groups and current
review evidence. The round-trip check verifies that exports keep material alpha
and assembly metadata. Visual review is a separate human/agent judgment; these
scripts cannot guarantee professional taste or a match to a reference photograph.

Version 0.5.1 contains individual studies and a broad construction draft, still subject to the release checks in
`RELEASE-CHECKLIST.md`. The high-detail meshes are illustration masters; benchmark
and optimize for any device/platform you intend to promise buyers.
