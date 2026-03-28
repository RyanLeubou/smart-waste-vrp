"""
Metrics complet :
- temps réel (par tournée)
- global (historique)
"""

# 🔥 stockage global
history = []


def compute_metrics(routes, distance_matrix, demands, capacity, total_bins, num_depots):

    print("\n📊 ===== KPI TOURNÉE =====")

    total_distance = 0
    total_load = 0
    visited_bins = set()

    for route in routes:

        route_load = 0

        for i in range(len(route) - 1):

            from_node = route[i]
            to_node = route[i+1]

            total_distance += distance_matrix[from_node][to_node]

            # ignorer dépôts
            if from_node >= num_depots:
                route_load += demands[from_node]
                visited_bins.add(from_node)

        print(f"🚛 Charge camion : {route_load}/{capacity}")
        total_load += route_load

    # éviter division par 0
    avg_fill = (total_load / (capacity * len(routes))) * 100 if routes else 0

    uncollected = total_bins - len(visited_bins)

    co2 = total_distance * 0.27

    print(f"📏 Distance : {round(total_distance,2)}")
    print(f"📦 Remplissage : {round(avg_fill,2)} %")
    print(f"🗑️ Non collectées : {uncollected}")
    print(f"🌍 CO2 : {round(co2,2)} kg")

    # 🔥 stocker dans historique
    history.append({
        "distance": total_distance,
        "fill": avg_fill,
        "co2": co2,
        "uncollected": uncollected
    })

    return {
        "distance": total_distance,
        "fill": avg_fill,
        "co2": co2,
        "uncollected": uncollected
    }


# 🔥 METRICS GLOBAL
def compute_global_metrics():

    if not history:
        print("⚠ Aucun historique")
        return

    total_distance = sum(h["distance"] for h in history)
    avg_fill = sum(h["fill"] for h in history) / len(history)
    total_co2 = sum(h["co2"] for h in history)
    total_uncollected = sum(h["uncollected"] for h in history)

    print("\n📊 ===== KPI GLOBAL =====")
    print(f"📏 Distance totale : {round(total_distance,2)}")
    print(f"📦 Remplissage moyen : {round(avg_fill,2)} %")
    print(f"🌍 CO2 total : {round(total_co2,2)} kg")
    print(f"🗑️ Total non collectées : {total_uncollected}")