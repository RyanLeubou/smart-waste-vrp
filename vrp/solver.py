"""
Solveur VRP complet PRO
"""

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_vrp(data, time_windows):

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["starts"],
        data["ends"]
    )

    routing = pywrapcp.RoutingModel(manager)

    # ------------------------
    # Distance
    # ------------------------
    def distance(i, j):
        return int(data["distance_matrix"][
            manager.IndexToNode(i)
        ][manager.IndexToNode(j)])

    transit = routing.RegisterTransitCallback(distance)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)

    # ------------------------
    # Capacité
    # ------------------------
    def demand(i):
        return data["demands"][manager.IndexToNode(i)]

    demand_cb = routing.RegisterUnaryTransitCallback(demand)

    routing.AddDimensionWithVehicleCapacity(
        demand_cb, 0, data["vehicle_capacities"], True, "Capacity"
    )

    # ------------------------
    # Temps (VRPTW)
    # ------------------------
    routing.AddDimension(
        transit,
        0,
        100000,
        True,
        "Time"
    )

    time_dim = routing.GetDimensionOrDie("Time")

    for i, tw in enumerate(time_windows):
        index = manager.NodeToIndex(i)
        time_dim.CumulVar(index).SetRange(tw[0], tw[1])

    # ------------------------
    # Pénalité (nodes optionnels)
    # ------------------------
    penalty = 10000
    for i in range(len(data["distance_matrix"])):
        routing.AddDisjunction([manager.NodeToIndex(i)], penalty)

    # ------------------------
    # Paramètres recherche
    # ------------------------
    search = pywrapcp.DefaultRoutingSearchParameters()

    search.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search.time_limit.seconds = 5

    # ------------------------
    # Résolution
    # ------------------------
    solution = routing.SolveWithParameters(search)

    if not solution:
        print("❌ Aucune solution trouvée")
        return []

    routes = []

    for v in range(data["num_vehicles"]):
        index = routing.Start(v)
        route = []

        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        # 🔥 ajouter retour dépôt
        route.append(manager.IndexToNode(index))

        routes.append(route)

    return routes