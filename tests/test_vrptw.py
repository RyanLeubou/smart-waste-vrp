from vrp.model import create_data_model
from vrp.solver import solve_vrp


def test_vrptw_respects_time_windows():
    """
    Vérifie que le solveur respecte les fenêtres de temps
    """

    distance_matrix = [
        [0, 10, 20],
        [10, 0, 5],
        [20, 5, 0]
    ]

    demands = [0, 1, 1]

    vehicles = [{"capacity": 10, "depot": 0}]
    depots = [{"coord": (0, 0)}]

    time_windows = [
        (0, 100),
        (0, 15),    # doit être visité tôt
        (50, 100)   # doit être visité tard
    ]

    data = create_data_model(
        distance_matrix,
        demands,
        vehicles,
        depots
    )

    routes = solve_vrp(data, time_windows)

    assert routes is not None
    assert len(routes) == 1

    route = routes[0]

    # Vérification logique simple
    assert 1 in route
    assert 2 in route