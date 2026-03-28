"""
MAIN - VRP dynamique complet 
"""

import time

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins
from services.redis_service import save_bins, get_bins, reset_bins
from services.osrm_service import get_distance_matrix
from vrp.model import create_data_model
from vrp.solver import solve_vrp
from metrics import compute_metrics, compute_global_metrics
from visualization.map import display_routes
from visualization.graph import build_graph, draw_graph


# ------------------------
# CONFIGURATION
# ------------------------

# Dépôts 
depots = [
    {"coord": (4.0511, 9.7679)},  
    {"coord": (4.0435, 9.7080)},  
    {"coord": (4.0300, 9.7200)},  
    {"coord": (4.0600, 9.6800)},  
    {"coord": (4.0900, 9.8000)}   
]

# 4 camions par dépôt (total = 20)
vehicles = []
for depot_id in range(len(depots)):
    for _ in range(4):
        vehicles.append({
            "capacity": 50,
            "depot": depot_id
        })

# Nombre de poubelles
NUM_BINS = 50

# Nombre d’itérations (VRP dynamique)
ITERATIONS = 3


# ------------------------
# EXECUTION
# ------------------------

def run_dynamic():

    print("\nLancement VRP dynamique (version finale)\n")

    # Reset Redis
    reset_bins()

    # Stockage des KPI globaux (cumul)
    global_kpis = []

    # ------------------------
    # Initialisation
    # ------------------------
    bins = generate_bins(NUM_BINS)

    if not bins:
        print("Aucune poubelle générée")
        return

    for step in range(ITERATIONS):

        print(f"\nIteration {step + 1}/{ITERATIONS}")

        # ------------------------
        # Mise à jour dynamique
        # ------------------------
        bins = update_bins(bins)
        save_bins(bins)

        bins = get_bins()

        if not bins:
            print("Aucune donnée récupérée")
            continue

        # ------------------------
        # LOCATIONS
        # ------------------------
        locations = [d["coord"] for d in depots] + [
            (b["lat"], b["lon"]) for b in bins
        ]

        # ------------------------
        # MATRICE DES DISTANCES (OSRM)
        # ------------------------
        matrix = get_distance_matrix(locations)

        # ------------------------
        # DEMANDES (CVRP)
        # ------------------------
        demands = [0] * len(depots) + [
            int(b["level"] / 10) for b in bins
        ]

        # ------------------------
        # TIME WINDOWS (VRPTW)
        # ------------------------
        time_windows = [(0, 10000)] * len(depots) + [
            b.get("time_window", (0, 10000)) for b in bins
        ]

        # Sécurité
        assert len(time_windows) == len(locations)

        # ------------------------
        # MODELE VRP
        # ------------------------
        data = create_data_model(
            matrix,
            demands,
            vehicles,
            depots
        )

        # ------------------------
        # SOLVEUR
        # ------------------------
        routes = solve_vrp(data, time_windows)

        print("\nRoutes optimisées :")
        for i, r in enumerate(routes):
            depot_id = vehicles[i]["depot"]
            print(f"Camion {i} (arrondissement {depot_id}) -> {r}")

        # ------------------------
        # KPI TOURNÉE
        # ------------------------
        result = compute_metrics(
            routes,
            matrix,
            demands,
            capacity=50,
            total_bins=len(bins),
            num_depots=len(depots)
        )

        print("\nKPI tournée :", result)

        # Stockage pour KPI global
        global_kpis.append(result)

        # Pause simulation
        time.sleep(2)

    # ------------------------
    # KPI GLOBAL (CUMUL)
    # ------------------------
    print("\n===== KPI GLOBAL =====")
    compute_global_metrics(global_kpis)

    # ------------------------
    # CARTE
    # ------------------------
    display_routes(locations, routes, len(depots))
    print("\nCarte générée : map.html")

    # ------------------------
    # GRAPHE
    # ------------------------
    print("\nAffichage du graphe...")
    G = build_graph(locations)
    draw_graph(G, routes, len(depots))

    print("\nFin du programme")


# ------------------------
# MAIN
# ------------------------

if __name__ == "__main__":
    run_dynamic()