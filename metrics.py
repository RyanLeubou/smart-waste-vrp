"""
Calcul des KPI 
"""


def compute_metrics(routes, matrix, demands, capacity, total_bins, num_depots):
    """
    KPI pour UNE tournée
    """

    total_distance = 0
    total_collected = 0

    for route in routes:

        route_load = 0

        for i in range(len(route) - 1):
            total_distance += matrix[route[i]][route[i + 1]]

        for node in route:
            if node >= num_depots:
                route_load += demands[node]

        total_collected += route_load

    capacity_total = capacity * len(routes)

    fill = (total_collected / capacity_total) * 100 if capacity_total > 0 else 0

    co2 = total_distance * 0.27  # facteur simplifié

    uncollected = total_bins - len({
        node for route in routes for node in route if node >= num_depots
    })

    result = {
        "distance": total_distance,
        "fill": fill,
        "co2": co2,
        "uncollected": uncollected,
        "collected": total_collected,
        "capacity_total": capacity_total
    }

    print("\n===== KPI TOURNÉE =====")
    print(f"Distance : {total_distance}")
    print(f"Remplissage : {round(fill, 2)} %")
    print(f"CO2 : {round(co2, 2)} kg")
    print(f"Non collectées : {uncollected}")

    return result


def compute_global_metrics(kpis):
    """
    KPI globaux cumulés (pondérés)
    """

    total_distance = sum(k["distance"] for k in kpis)
    total_co2 = sum(k["co2"] for k in kpis)
    total_uncollected = sum(k["uncollected"] for k in kpis)

    total_collected = sum(k["collected"] for k in kpis)
    total_capacity = sum(k["capacity_total"] for k in kpis)

    fill = (total_collected / total_capacity) * 100 if total_capacity > 0 else 0

    result = {
        "distance": total_distance,
        "fill": fill,
        "co2": total_co2,
        "uncollected": total_uncollected
    }

    print("\n===== KPI GLOBAL =====")
    print(f"Distance totale : {total_distance}")
    print(f"Remplissage global : {round(fill, 2)} %")
    print(f"CO2 total : {round(total_co2, 2)} kg")
    print(f"Total non collectées : {total_uncollected}")

    return result