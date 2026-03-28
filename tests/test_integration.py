"""
Test d'intégration complet du système :
Simulation → Redis → IA → VRP → Metrics
"""

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins

from services.redis_service import save_bins, get_bins, reset_bins
from services.osrm_service import get_distance_matrix

from vrp.model import create_data_model
from vrp.solver import solve_vrp

from metrics import compute_metrics

from ai.preprocessing import process_ai_output


def test_full_system():
    """
    Test complet du pipeline :
    IA + VRP + Metrics
    """

    # ------------------------
    # RESET
    # ------------------------
    reset_bins()

    # ------------------------
    # SIMULATION
    # ------------------------
    bins = generate_bins(10)
    bins = update_bins(bins)

    save_bins(bins)

    # ------------------------
    # IA PROCESSING
    # ------------------------
    raw_bins = get_bins()
    bins = process_ai_output(raw_bins)

    # ------------------------
    # TEST 1 : FILTRAGE IA
    # ------------------------
    for b in bins:
        assert b["level"] >= 40

    # Cas possible : aucune poubelle à collecter
    if not bins:
        return

    # ------------------------
    # TEST 2 : PRIORITÉS IA
    # ------------------------
    for b in bins:
        assert "time_window" in b

    # ------------------------
    # SETUP VRP
    # ------------------------
    depots = [
        {"coord": (4.05, 9.75)},
        {"coord": (4.06, 9.76)}
    ]

    vehicles = [
        {"capacity": 50, "depot": 0},
        {"capacity": 50, "depot": 1}
    ]

    # ------------------------
    # LOCATIONS
    # ------------------------
    locations = [d["coord"] for d in depots] + [
        (b["lat"], b["lon"]) for b in bins
    ]

    # ------------------------
    # MATRICE DES DISTANCES
    # ------------------------
    matrix = get_distance_matrix(locations)

    # ------------------------
    # DEMANDS (CVRP)
    # ------------------------
    demands = [0]*len(depots) + [
        max(1, int(b["level"]/10)) for b in bins
    ]

    # ------------------------
    # TIME WINDOWS (VRPTW)
    # ------------------------
    time_windows = [(0, 10000)] * len(depots) + [
        b["time_window"] for b in bins
    ]

    # Sécurité
    assert len(time_windows) == len(locations)

    # ------------------------
    # VRP
    # ------------------------
    data = create_data_model(
        matrix,
        demands,
        vehicles,
        depots
    )

    routes = solve_vrp(data, time_windows)

    # ------------------------
    # TEST 3 : STRUCTURE ROUTES
    # ------------------------
    assert isinstance(routes, list)
    assert len(routes) == len(vehicles)

    # ------------------------
    # TEST 4 : ROUTES VALIDES
    # ------------------------
    for route in routes:
        assert len(route) >= 2  # au moins dépôt → dépôt

    # ------------------------
    # METRICS
    # ------------------------
    result = compute_metrics(
        routes,
        matrix,
        demands,
        capacity=50,
        total_bins=len(bins),
        num_depots=len(depots)
    )

    # ------------------------
    # TEST 5 : KPI
    # ------------------------
    assert result["distance"] >= 0
    assert 0 <= result["fill"] <= 100
    assert result["co2"] >= 0