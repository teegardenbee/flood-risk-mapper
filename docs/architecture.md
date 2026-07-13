# Architecture

## Why Python instead of a client-side app

The original prototype was a single HTML file: all scoring logic and data
lived in the browser tab, computed in JS, using the user's own device and
memory. That's fine for a 15-row demo. It stops being fine once real inputs
enter the picture — satellite rasters, IMD rainfall grids, and drain vector
layers are easily hundreds of MB to multiple GB, and zonal statistics
(combining a raster with ward polygons) is real CPU/IO work that has no
business running in a browser tab.

So the whole app moves server-side. The browser (or whatever renders the
final map) only ever receives pre-computed results — a rendered map or a
JSON/GeoJSON response — never raw rasters, never the scoring computation.

## Current state (MVP)

```
app/
  data/localities.py   -- seed dataset (15 localities, hand-estimated sub-scores)
  scoring.py            -- pure scoring logic, no UI imports
  map_utils.py           -- Folium map builder (wraps Leaflet, written in Python)
  main.py                -- Streamlit entrypoint: sliders + map + ranked list
```

This intentionally mirrors the layer boundaries of the target architecture
even though, today, `localities.py` just returns a Python list instead of
querying a database. `scoring.py` has zero Streamlit or Folium imports on
purpose — it's the piece that gets reused unchanged by a future API layer.

Run it:

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

## Target architecture (as data sources are added)

```
External data sources                  (satellite imagery, IMD rainfall,
                                         drain vectors, ward boundaries)
        |
        v
Geoprocessing pipeline                 (GeoPandas for vectors, Rasterio /
                                         xarray for rasters, computes
                                         zonal statistics per ward)
        |
        v
PostGIS  +  Object storage             (vector layers in PostGIS; raw
                                         satellite/rainfall rasters as
                                         GeoTIFF/NetCDF in object storage,
                                         e.g. MinIO or S3)
        |
        v
FastAPI scoring service                (REST + GeoJSON endpoints; the
                                         existing scoring.py logic moves
                                         here, reads inputs from PostGIS
                                         instead of a Python list)
        |
        v
Dashboard                              (Streamlit to start; can be swapped
                                         for a React/Leaflet client later
                                         without touching the scoring logic)
```

### Migration steps, in order

1. **Vector data first.** Replace the hand-coded lat/lng points with real
   ward boundary polygons (BBMP ward shapefiles / GeoJSON) using GeoPandas.
   Localities become wards; `load_localities()` becomes a GeoDataFrame read.
2. **Stand up PostGIS.** Load ward boundaries and drain vector data as
   tables. `docker-compose` with a `postgis/postgis` image is the fastest
   path locally.
3. **Add drain vector risk.** Compute real distance-to-drain per ward with
   GeoPandas spatial joins, replacing the estimated `drainage` sub-score.
4. **Add rainfall.** Pull IMD gridded rainfall (NetCDF), use `rasterstats`
   or `xarray` to compute per-ward rainfall exposure over time.
5. **Add satellite-derived elevation/impervious surface.** Use Rasterio to
   compute zonal statistics (mean elevation, % impervious surface) per ward
   from a DEM (e.g. SRTM/Copernicus) and land-cover raster.
6. **Extract the API.** Move `scoring.py` behind a FastAPI app once there's
   more than one consumer (e.g. dashboard + a future mobile view).
7. **Swap the dataset for a new city.** Because every layer keys off ward
   polygons rather than hardcoded coordinates, a new city needs new ward
   boundaries + fresh raster/vector inputs, not new application code.

## Why these libraries

- **GeoPandas** — the standard for vector geodata in Python (shapefiles,
  GeoJSON, spatial joins, distance calculations).
- **Rasterio / xarray** — Rasterio for straightforward raster I/O and zonal
  stats; xarray for multi-dimensional rainfall data (time x lat x lon).
- **PostGIS** — battle-tested open-source spatial database; works with
  GeoPandas (`geopandas.read_postgis`) with no extra glue code.
- **FastAPI** — async, typed, auto-generates OpenAPI docs, plays well with
  GeoJSON responses.
- **Streamlit** — fastest way to keep the dashboard 100% Python while this
  is still a small planning tool; swappable later without touching the
  scoring or data layers underneath it.

All of the above are open source with permissive licenses (MIT/BSD/Apache),
which matters if this is going to live on GitHub as a public or
BBMP-shareable repository.
