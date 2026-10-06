# Geographic base for Vector Space

Source: US Atlas 3.0.1 `states-10m.json`, a redistribution of U.S. Census Bureau 2017 cartographic boundaries.

- Project documentation: https://github.com/topojson/us-atlas
- Exact data: https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-10m.json
- License: adjacent `LICENSE` (ISC).

`python3 scripts/video/build_vector_space_us_map.py` generates the local SVG at `course-assets/vector-space/vector-space-us-map.svg` and the projection constants in `projection.json`. It uses the contiguous 48 states plus DC, retaining coastlines, islands, and state boundaries. Alaska, Hawaii, and territories are outside this lesson's city map.

The live markers use the same Albers equal-area projection and fit as the SVG, with the lesson's approximate coordinates. No remote map service or runtime mapping dependency is used. The cream land and boundary colors come from the existing course palette. The white map background matches the inner stage, surrounded by the interaction's pale blue outer frame.
