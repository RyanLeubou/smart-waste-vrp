"""
Création du modèle VRP complet :
- multi-dépôts
- multi-véhicules
- compatible OR-Tools
"""

def create_data_model(distance_matrix, demands, vehicles, depots):
    """
    vehicles = [
        {"capacity": 50, "depot": 0},
        {"capacity": 40, "depot": 1}
    ]

    depots = [
        {"coord": (...)},
        {"coord": (...)}
    ]
    """

    # 🔹 capacités
    vehicle_capacities = [v["capacity"] for v in vehicles]

    # 🔹 départs (index des dépôts)
    starts = [v["depot"] for v in vehicles]

    # 🔹 retours (même dépôt)
    ends = [v["depot"] for v in vehicles]

    return {
        "distance_matrix": distance_matrix,
        "demands": demands,
        "vehicle_capacities": vehicle_capacities,
        "num_vehicles": len(vehicles),
        "starts": starts,
        "ends": ends,
    }