"""
Test d'intégration global du système VRP
"""

import time

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins
from services.redis_service import save_bins, get_bins, reset_bins
from services.osrm_service import get_distance_matrix
from vrp.model import create_data_model
from vrp.solver import solve_vrp
from metrics import compute_metrics


def test_full_system():
    """
    Test complet :
    Simulation → Redis → VRP → Metrics
    """

    # ------------------------
    # 1. RESET
    # ------------------------
    reset_bins()

    # ------------------------
    # 2. SIMULATION (génération)
    # ------------------------
    bins = generate_bins(5)

    # mise à jour (remplissage)
    bins = update_bins(bins)

    # sauvegarde Redis
    save_bins(bins)

    # ------------------------
    # 3. RÉCUPÉRATION
    # ------------------------
    bins = get_bins()

    assert len(bins) == 5

    # ------------------------
    # 4. PRÉPARATION VRP
    # ------------------------
    depots = [{"coord": (4.05, 9.75)}]

    vehicles = [
        {"capacity": 50, "depot": 0}
    ]

    locations = [d["coord"] for d in depots] + [
        (b["lat"], b["lon"]) for b in bins
    ]

    matrix = get_distance_matrix(locations)

    demands = [0] + [int(b["level"]/10) for b in bins]

    time_windows = [(0, 10000)] * len(locations)

    # ------------------------
    # 5. VRP
    # ------------------------
    data = create_data_model(
        matrix,
        demands,
        vehicles,
        depots
    )

    routes = solve_vrp(data, time_windows)

    # ------------------------
    # 6. VALIDATION ROUTES
    # ------------------------
    assert isinstance(routes, list)
    assert len(routes) > 0

    # ------------------------
    # 7. METRICS
    # ------------------------
    result = compute_metrics(
        routes,
        matrix,
        demands,
        capacity=50,
        total_bins=len(bins),
        num_depots=1
    )

    assert result["distance"] >= 0
    assert result["fill"] >= 0
    assert result["co2"] >= 0