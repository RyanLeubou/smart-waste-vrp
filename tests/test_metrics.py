"""
Tests des KPI 
"""

from metrics import compute_metrics, compute_global_metrics


# ------------------------
# TEST KPI TOURNÉE
# ------------------------
def test_metrics():

    routes = [[0, 1, 2, 0]]

    matrix = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    demands = [0, 5, 5]

    result = compute_metrics(
        routes,
        matrix,
        demands,
        capacity=20,
        total_bins=2,
        num_depots=1
    )

    assert result["distance"] > 0
    assert 0 <= result["fill"] <= 100
    assert result["co2"] >= 0
    assert result["uncollected"] >= 0
    assert result["collected"] > 0


# ------------------------
# TEST KPI GLOBAL
# ------------------------
def test_global_metrics():

    kpis = [
        {
            "distance": 100,
            "fill": 10,
            "co2": 50,
            "uncollected": 1,
            "collected": 20,
            "capacity_total": 50
        },
        {
            "distance": 200,
            "fill": 20,
            "co2": 100,
            "uncollected": 2,
            "collected": 40,
            "capacity_total": 50
        }
    ]

    result = compute_global_metrics(kpis)

    assert result["distance"] == 300
    assert result["co2"] == 150
    assert result["uncollected"] == 3

    # fill pondéré = (20+40)/(50+50) = 60%
    assert round(result["fill"], 2) == 60.0


# ------------------------
# TEST LOGIQUE (PAS > 100%)
# ------------------------
def test_fill_never_exceeds_100():

    kpis = [
        {
            "distance": 100,
            "fill": 90,
            "co2": 50,
            "uncollected": 0,
            "collected": 45,
            "capacity_total": 50
        },
        {
            "distance": 100,
            "fill": 95,
            "co2": 50,
            "uncollected": 0,
            "collected": 48,
            "capacity_total": 50
        }
    ]

    result = compute_global_metrics(kpis)

    assert result["fill"] <= 100