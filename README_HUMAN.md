# India Trip Generator — human guide

## Use the finished page

Open **India_Trip_Generator.html** in a modern browser. The downloaded compiled page needs no build, server or login. Mapbox maps and Wikimedia photographs need internet. If those cannot load, the embedded coordinate map and local route planner remain usable. Phone file-preview apps may disable JavaScript; open the file in a browser instead.

## Build from this source ZIP

1. Unzip the project and open a terminal in `india-trip-generator`.
2. Install Python 3.10 or newer if needed. There are no Python packages to install.
3. Run `python build.py` (on Windows, `py build.py` may be the command).
4. Open `dist/India_Trip_Generator.html`. This is the single portable page to copy or share. `dist/data.json` is an intermediate test/build file and is not required beside the page.

The build uses only local source files; it makes no network requests. You can also run `python /absolute/path/to/build.py` from another directory. Optional: `python build.py --output /path/to/Trip.html`.

## Mapbox configuration

Mapbox tokens are not committed. Copy `config/mapbox.example.json` to `config/mapbox.public.json` (or `config/mapbox.local.json`) and put your public `pk.` token there, or set `MAPBOX_TOKEN`. The build inserts it into the compiled HTML; changing the token requires rebuilding. Precedence: environment → local → public config. `--config /path/to/config.json` chooses an alternative base file and skips the local override. Mapbox usage is subject to the token owner's account settings and allowances.

All generated outputs belong in ignored `dist/`. The source archive deliberately contains no compiled HTML or generated data.

## Explore and plan

- The filter icon beside Explore opens a panel with **Experiences** and **Regions** tabs. Experiences cover temples/shrines, history/forts, adventure, caves, beaches/water, wildlife, culture and night skies. Selected experiences or regions match **any** within that group; search and the season checkbox narrow results further. Clear filters resets both tabs.
- Hover a pin for a photo preview. Move onto the preview to browse its photo arrows, open a large image, view details or add the destination. A large cluster previews its member destinations; separate arrows change the place and the photograph. Click a cluster to keep its preview open, then choose **Zoom into group** if desired. Touch users can tap clusters or use the destination list. Individual pin clicks open the detail card; Shift-click adds/removes a stop.
- Add at least two places, choose dates and route settings, then Generate route. The optimizer automatically rearranges stops into the best order for your time/cost priority. The time/cost slider previews its priority as you drag and recalculates once when released. The optimizer preserves the selected set; it does not silently discard places.
- Expand **Compare travel options** for compact alternatives. Each mode has its own price and time; selected-path details show ranges, handling buffers and source links. USD is primary, original INR secondary. The editable conversion rate changes display, not the optimizer's INR calculations.
- Remove a stop with its ×. Clear route removes calculated legs while keeping selected places; Clear all removes both. Reset view restores the full map. Use the theme button for light/dark mode.
- Weather uses Fahrenheit first, Celsius below, with a seasonal-condition icon. These are historical climate bands or regional proxies, **not a live forecast**. Visit durations and prices are planning estimates. Transport connections and permits still need checking against your actual dates and traveler status.
- Export JSON to back up selections/settings and Markdown for the itinerary. File-browser storage support varies; exports are the dependable backup.

Keyboard: `/` search; Escape closes overlays; `F` fits visible places; Ctrl/Cmd+Z undoes a selection/settings change. Tab and Enter operate list and popup controls. Photo galleries use left/right arrows when focused. Stop order is chosen by the route optimizer (optional start/end pins remain in Route settings). Motion respects reduced-motion preferences.

## Scope and limitations

280 destinations, 349 transport nodes and 708 stored corridors are included. Route geometry is illustrative rather than road navigation. Totals run to the nearest airport or train station; last-mile gateway transfers are assumed separately. Flight/train handling buffers are modeled; timetables, connection guarantees, hotels and activity fees are not. Climate, permit, photo and transport provenance remains in the cards/help and `RESEARCH.md`. Some destinations have a verified regional Reddit report; others offer a clearly labeled search, not an invented review. Gallery imagery is optional and needs its displayed source/attribution.
