# Flood Risk Priority Mapper

A prototype tool for ranking localities/wards by flood-intervention
priority, starting with Bengaluru. Built to expand to other cities and to
real geospatial datasets (satellite imagery, IMD rainfall, drain vectors)
over time — see [`docs/architecture.md`](docs/architecture.md) for the full
plan and current status.

> **Data disclaimer:** the current locality scores are illustrative
> estimates based on public reporting patterns, not verified official
> measurements. This is a prototyping tool, not a decision-making source of
> truth yet.

## Quick start

```bash
git clone <this-repo>
cd flood-risk-mapper
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

Opens at `http://localhost:8501`.

## Project layout

```
app/
  data/localities.py   # current seed dataset (swap point for real data)
  scoring.py            # composite score engine, framework-agnostic
  map_utils.py           # Folium map builder
  main.py                # Streamlit UI
docs/
  architecture.md        # current + target architecture, migration steps
tests/
  test_scoring.py         # scoring engine unit tests
```

## Development

```bash
pip install -r requirements-dev.txt
pytest              # run tests
ruff check .        # lint
```

## Contributing / workflow

- Work off feature branches, open a PR into `main`.
- CI (`.github/workflows/ci.yml`) runs lint + tests on every push/PR.
- Keep `app/scoring.py` free of UI or web-framework imports — it's meant to
  be reusable as-is by a future API layer.

## License

MIT — see [LICENSE](LICENSE).
