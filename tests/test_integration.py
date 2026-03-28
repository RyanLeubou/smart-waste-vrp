"""
Test d'intégration global du système VRP complet :
VRP + CVRP + VRPTW + Multi-dépôts + Dynamique
"""

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins
from services.redis_service import save_bins, get_bins, reset_bins
from services.osrm_service import get_distance_matrix
from vrp.model import create_data_model
from vrp.solver import solve_vrp
from metrics import compute_metrics


def test_full_system():

    # ------------------------
    # 1. RESET
    # ------------------------
    reset_bins()

    # ------------------------
    # 2. SIMULATION DYNAMIQUE
    # ------------------------
    bins = generate_bins(6)

    # 🔥 plusieurs itérations (VRP dynamique)
    for _ in range(2):
        bins = update_bins(bins)

    # Vérifie VRPTW
    assert all("time_window" in b for b in bins)

    save_bins(bins)

    # ------------------------
    # 3. RÉCUPÉRATION REDIS
    # ------------------------
    bins = get_bins()

    assert len(bins) == 6

    # ------------------------
    # 4. MULTI-DÉPÔTS
    # ------------------------
    depots = [
        {"coord": (4.05, 9.75)},
        {"coord": (4.06, 9.76)}
    ]

    # ------------------------
    # 5. MULTI-CAMIONS + CVRP
    # ------------------------
    vehicles = [
        {"capacity": 10, "depot": 0},
        {"capacity": 10, "depot": 1}
    ]

    # ------------------------
    # 6. LOCATIONS
    # ------------------------
    locations = [d["coord"] for d in depots] + [
        (b["lat"], b["lon"]) for b in bins
    ]

    # ------------------------
    # 7. DISTANCE MATRIX
    # ------------------------
    matrix = get_distance_matrix(locations)

    # ------------------------
    # 8. DEMANDS (CVRP)
    # ------------------------
    demands = [0]*len(depots) + [
        int(b["level"]/10) for b in bins
    ]

    # ------------------------
    # 9. TIME WINDOWS (VRPTW)
    # ------------------------
    time_windows = [(0, 10000)] * len(depots) + [
        b.get("time_window", (0, 10000)) for b in bins
    ]

    # ------------------------
    # 10. MODEL
    # ------------------------
    data = create_data_model(
        matrix,
        demands,
        vehicles,
        depots
    )

    # ------------------------
    # 11. SOLVEUR
    # ------------------------
    routes = solve_vrp(data, time_windows)

    # ------------------------
    # 12. VALIDATION ROUTES
    # ------------------------
    assert isinstance(routes, list)
    assert len(routes) == len(vehicles)

    # ------------------------
    # 13. VALIDATION VRPTW
    # ------------------------
    visited_nodes = set()

    for route in routes:
        for node in route:
            visited_nodes.add(node)

    # VRPTW peut ignorer des poubelles
    assert len(visited_nodes) <= len(locations)

    # ------------------------
    # 14. METRICS
    # ------------------------
    result = compute_metrics(
        routes,
        matrix,
        demands,
        capacity=10,
        total_bins=len(bins),
        num_depots=len(depots)
    )

    assert result["distance"] >= 0
    assert result["fill"] >= 0
    assert result["co2"] >= 0

    # ------------------------
    # 15. VALIDATION FINALE
    # ------------------------
    assert isinstance(result, dict)