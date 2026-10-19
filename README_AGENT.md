# India Trip Generator — agent guide

## Build contract

Use Python 3.10+ standard library. Run `python build.py`; output is `dist/India_Trip_Generator.html` plus intermediate `dist/data.json`, and the Express/Helmet hosting pair `dist/views/india_trip_planner.ejs` + `dist/public/js/india_trip_planner.js`. Compilation is deterministic for the same source/config and requires no network. The portable HTML embeds JS, CSS, destination data and build configuration. The hosting EJS is a markup/CSS shell (nonce CSP); the single JS bundle is dual-purpose (TripEngine worker + main-thread planner with embedded data). Mapbox GL and optional imagery load remotely at runtime; offline planning uses a schematic coordinate map.

Never commit Mapbox tokens. Copy `config/mapbox.example.json` to ignored `config/mapbox.public.json` or `config/mapbox.local.json`, or set `MAPBOX_TOKEN`. Precedence: environment → local → public config. `--config` chooses a base file and skips the local override; `--output` chooses the compiled filename. Build validates a public `pk.` token before generating output. The token is embedded in the portable HTML at build time; the hosting EJS receives it only as `mapboxToken` at render time (`{ nonce, mapboxToken }`) and must never bake the token into the JS bundle—never print it in logs or paste it into app source.

Generated outputs, ZIP archives, cache files, local config, node_modules and verifier outputs are gitignored. Do not put build products into the source archive. Default builds must never modify source files.

## Source map

- `shell.html`: semantic application shell and build placeholders.
- `theme.css`: layout, themes, responsive panels, mode badges, galleries and motion. The v6 tail overrides older compact sizes.
- `app.js`: local state, events, Mapbox/fallback map, galleries, popups, route UI and exports.
- `presentation.js`: pure category matching, Fahrenheit conversion, seasonal weather kinds and concise experience formatting.
- `engine.js`: transport graph, score, stop-order optimization and worker interface.
- `cartography.js`: curated borders, state/region labels and contextual city filtering. Andaman retains labels/focus, no ring or wash.
- `build.py`: config loading and single-file compilation.
- `build_data.py`: assembles original bank + expansion modules, sources and transport network. Reads `data/destination_bank.md`; intermediate JSON goes to `TRIP_DATA_OUTPUT` or `dist/data.json`.
- `expansion.py`, `expansion_v3.py`, `expansion_v5.py`: subsequent destination/transport expansions. `media_data.py`: photo subjects, credited seeds and researched Reddit report mappings.
- `data/destination_bank.md`: reusable destination research/context. `ADVENTURE_MAP_CROSSWALK.md` records the earlier unavailable-image limitation; do not claim the lost attachment was read.
- `RESEARCH.md`: research provenance and scope notes.

## Interaction invariants

Keep slider `input` handlers cosmetic: optimize on `change`/release only. Do not replace the slider DOM during a drag. Preserve route settings, exact selected set, scroll and map viewpoint during recomputation. Stale optimizer results must remain ignored/cancelled.

Experience and region filters live in one panel (`#categoryPanel`) with tabs. Category selection is OR across categories; region selection is OR across regions; both AND with search/season. Derive experience counts from the pool with other filters applied but categories ignored; derive region counts with regions ignored. Clearing panel filters must not clear selected stops. Selected pins remain visible when their destination is filtered out. Use `TripPresentation` everywhere for consistent matching.

All list, detail and hover images use `galleryHtml` and shared photoCache/photoIndex state. Popup controls stop propagation; avoid duplicate app/Mapbox click handling. Gallery photo arrows differ from cluster place arrows. Popup leave has a 380ms bridge so the pointer can reach the popup; popup enter/focus cancels it. Click-pinned clusters stay until explicit close/move/action. Close on map movement/filter rebuild. Cluster queries support both callback and Promise Mapbox contracts; epoch guards suppress late results after dismissal. Do not infer cluster membership from screen-space radius.

Weather is a seasonal tendency, not prediction. Show F first, C second, accessible icons; retain the baseline/proxy caveats. Experiences should have a bold short title and at most one explanatory sentence/phrase. Keep modal focus trapping/restoration, Escape behavior, accessible names and reduced-motion handling.

Prices are stored and optimized in INR. USD is display conversion only. Preserve road shared/private-car accounting, party scaling, flight/rail handling and provenance flags. Concise alternatives must retain per-mode cost/time and access to full segments/sources. Do not invent scheduled services or treat straight lines as routable geometry. Route scope and permit eligibility must remain explicit.

## Packaging

Ship editable source (not `dist/`) plus one compiled HTML. Do not include generated data, local token overrides, caches or archives. Human instructions are in `README_HUMAN.md`.
