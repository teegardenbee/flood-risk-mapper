from app.data.localities import load_localities
from app.scoring import DEFAULT_WEIGHTS, score_localities, tier_of


def test_scores_sorted_descending():
    scored = score_localities(load_localities(), DEFAULT_WEIGHTS)
    scores = [row["composite"] for row in scored]
    assert scores == sorted(scores, reverse=True)


def test_bellandur_is_top_ranked_by_default():
    scored = score_localities(load_localities(), DEFAULT_WEIGHTS)
    assert scored[0]["name"] == "Bellandur"


def test_weights_dont_need_to_sum_to_100():
    a = score_localities(load_localities(), {"elevation": 1, "drainage": 1, "lakebed": 1, "density": 1})
    b = score_localities(load_localities(), {"elevation": 30, "drainage": 30, "lakebed": 30, "density": 30})
    assert [r["name"] for r in a] == [r["name"] for r in b]


def test_tier_boundaries():
    assert tier_of(75) == "Critical"
    assert tier_of(74.9) == "High"
    assert tier_of(60) == "High"
    assert tier_of(40) == "Medium"
    assert tier_of(39.9) == "Low"
