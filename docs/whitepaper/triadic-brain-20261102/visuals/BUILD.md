# Local rendering and document checks

These files are documentation assets, not product runtime code. All inputs needed to reproduce the visuals are in `source/`.

## Existing local tools

- Python 3 standard library
- Inkscape (SVG → PNG)
- Graphviz `dot` (editable focused DOT graphs → SVG)

No package installation, paid resource or external rendering service is required. Do not submit a private source map to a hosted renderer.

From this directory:

```sh
python3 source/render_atlas.py
python3 source/render_special.py
python3 source/render_focus.py
python3 source/build_index.py
```

`render_atlas.py --svg-only` skips PNG rendering for its pages. The focus renderer uses 72-DPI SVG geometry, then exports a 1600-pixel-wide PNG; this avoids mismatched Graphviz scale/viewBox clipping. The DOT files are also directly editable.

## Before repository publication

1. Check the public source snapshot still matches the concept-map edition being released.
2. Confirm all 86 IDs remain unique in the data ledger, with one primary editorial home each.
3. Confirm F79 has no operational edge or capability placement; F02 remains historical lineage.
4. Inspect every final PNG at full size and fix clipping, overlaps or unreadable labels. Read SVG text alternatives as well.
5. Keep source-connected, bounded component evidence, installed behavior, missing joins and research separate.
6. Publish only the coordinator's explicit public allowlist. Never recursively upload a sibling private directory.

Source, diagram and accessibility inspection is not product runtime testing or CI.
