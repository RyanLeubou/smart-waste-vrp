"""
Solveur VRP complet
"""

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_vrp(data, time_windows):

    # ------------------------
    # MANAGER
    # ------------------------
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["starts"],
        data["ends"]
    )

    routing = pywrapcp.RoutingModel(manager)

    # ------------------------
    # DISTANCE (coût)
    # ------------------------
    def distance_callback(i, j):
        return int(data["distance_matrix"][
            manager.IndexToNode(i)
        ][manager.IndexToNode(j)])

    transit_cb = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb)

    # ------------------------
    # CAPACITÉ (CVRP)
    # ------------------------
    def demand_callback(i):
        return data["demands"][manager.IndexToNode(i)]

    demand_cb = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_cb,
        0,
        data["vehicle_capacities"],
        True,
        "Capacity"
    )

    # ------------------------
    # TEMPS (VRPTW réaliste)
    # ------------------------
    def time_callback(i, j):
        dist = data["distance_matrix"][
            manager.IndexToNode(i)
        ][manager.IndexToNode(j)]

        # ✔ dist en mètres → temps en minutes
        # ✔ vitesse = 60 km/h → 1 km = 1 min
        return int(dist / 1000)

    time_cb = routing.RegisterTransitCallback(time_callback)

    routing.AddDimension(
        time_cb,
        100,     # attente autorisée
        10000,   # horizon
        False,   # VRPTW réel
        "Time"
    )

    time_dim = routing.GetDimensionOrDie("Time")

    # ------------------------
    # FENÊTRES DE TEMPS
    # ------------------------
    for i, tw in enumerate(time_windows):
        index = manager.NodeToIndex(i)
        time_dim.CumulVar(index).SetRange(tw[0], tw[1])
        time_dim.SlackVar(index).SetRange(0, 10000)

    # ------------------------
    # NODES OPTIONNELS (VRPTW réel)
    # ------------------------
    penalty = max(max(row) for row in data["distance_matrix"]) * 10

    for i in range(len(data["distance_matrix"])):
        if i >= data["num_depots"]:
            routing.AddDisjunction([manager.NodeToIndex(i)], penalty)

    # ------------------------
    # PARAMÈTRES DE RECHERCHE
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
    # RÉSOLUTION
    # ------------------------
    solution = routing.SolveWithParameters(search)

    if not solution:
        print("❌ Aucune solution trouvée")
        return []

    # ------------------------
    # EXTRACTION DES ROUTES
    # ------------------------
    routes = []

    for v in range(data["num_vehicles"]):
        index = routing.Start(v)
        route = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))

        route.append(manager.IndexToNode(index))
        routes.append(route)

    return routes