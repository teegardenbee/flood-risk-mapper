"""
Composite flood-risk scoring engine.

Kept deliberately free of any UI or web-framework imports. This is the
piece that gets reused as-is when the app grows a FastAPI layer -- the
API will just call `score_localities()` and return the result as JSON
instead of handing it to Streamlit.
"""

from dataclasses import asdict
from typing import TypedDict

from app.data.localities import Locality

FACTOR_KEYS = ("elevation", "drainage", "lakebed", "density")

DEFAULT_WEIGHTS: dict[str, int] = {
    "elevation": 30,
    "drainage": 30,
    "lakebed": 25,
    "density": 15,
}


class ScoredLocality(TypedDict):
    name: str
    lat: float
    lng: float
    elevation: int
    drainage: int
    lakebed: int
    density: int
    note: str
    composite: float
    tier: str


def tier_of(score: float) -> str:
    if score >= 75:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def score_localities(
    localities: list[Locality],
    weights: dict[str, int] = DEFAULT_WEIGHTS,
) -> list[ScoredLocality]:
    """Compute composite risk scores and sort descending.

    Weights don't need to sum to 100 -- they're normalized here, so a UI
    can pass raw slider values (0-100 each) without doing math itself.
    """
    total_weight = sum(weights.get(k, 0) for k in FACTOR_KEYS) or 1

    scored: list[ScoredLocality] = []
    for loc in localities:
        weighted_sum = sum(
            getattr(loc, key) * weights.get(key, 0) for key in FACTOR_KEYS
        )
        composite = round(weighted_sum / total_weight, 1)
        row = asdict(loc)
        row["composite"] = composite
        row["tier"] = tier_of(composite)
        scored.append(row)  # type: ignore[arg-type]

    scored.sort(key=lambda r: r["composite"], reverse=True)
    return scored
