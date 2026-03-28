"""
MAIN - VRP dynamique contrôlé (démo)
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

depots = [
    {"coord": (4.05, 9.75)},
    {"coord": (4.06, 9.76)},
    {"coord": (4.07, 9.77)}
]

vehicles = [
    {"capacity": 50, "depot": 0},
    {"capacity": 50, "depot": 0},
    {"capacity": 50, "depot": 1},
    {"capacity": 50, "depot": 2}
]

NUM_BINS = 15
ITERATIONS = 3   # 🔥 nombre de cycles dynamiques


# ------------------------
# EXECUTION
# ------------------------

def run_dynamic():

    print("\n🚀 Lancement VRP dynamique (mode démo)\n")

    reset_bins()

    # ------------------------
    # Initialisation
    # ------------------------
    bins = generate_bins(NUM_BINS)

    for step in range(ITERATIONS):

        print(f"\n🔄 Itération {step + 1}/{ITERATIONS}")

        # ------------------------
        # Mise à jour dynamique
        # ------------------------
        bins = update_bins(bins)
        save_bins(bins)

        bins = get_bins()

        # ------------------------
        # LOCATIONS
        # ------------------------
        locations = [d["coord"] for d in depots] + [
            (b["lat"], b["lon"]) for b in bins
        ]

        # ------------------------
        # MATRICE
        # ------------------------
        matrix = get_distance_matrix(locations)

        # ------------------------
        # DEMANDES
        # ------------------------
        demands = [0]*len(depots) + [
            int(b["level"]/10) for b in bins
        ]

        # ------------------------
        # TIME WINDOWS
        # ------------------------
        time_windows = [(0, 10000)] * len(locations)

        # ------------------------
        # MODELE
        # ------------------------
        data = create_data_model(
            matrix,
            demands,
            vehicles,
            depots
        )

        # ------------------------
        # VRP
        # ------------------------
        routes = solve_vrp(data, time_windows)

        print("🚛 ROUTES :")
        for i, r in enumerate(routes):
            depot_id = vehicles[i]["depot"]
            print(f"Camion {i} (dépôt {depot_id}) → {r}")

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

        print("📊 KPI :", result)

        # pause pour voir évolution
        time.sleep(2)

    # ------------------------
    # KPI GLOBAL
    # ------------------------
    compute_global_metrics()

    # ------------------------
    # CARTE FINALE
    # ------------------------
    display_routes(locations, routes, len(depots))
    print("\n🗺️ Carte finale générée : map.html")

    # ------------------------
    # GRAPHE FINAL
    # ------------------------
    print("\n📊 Affichage du graphe final...")
    G = build_graph(locations)
    draw_graph(G, routes, len(depots))

    print("\n✅ FIN DU PROGRAMME")


# ------------------------
# MAIN
# ------------------------

if __name__ == "__main__":
    run_dynamic()