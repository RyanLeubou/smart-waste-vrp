from vrp.model import create_data_model
from vrp.solver import solve_vrp


def test_vrptw_logic():

    distance_matrix = [
        [0, 20000, 20000],
        [20000, 0, 5000],
        [20000, 5000, 0]
    ]

    demands = [0, 1, 1]

    vehicles = [{"capacity": 10, "depot": 0}]
    depots = [{"coord": (0, 0)}]

    time_windows = [
        (0, 100),
        (0, 5),
        (6, 10)
    ]

    data = create_data_model(
        distance_matrix,
        demands,
        vehicles,
        depots
    )

    routes = solve_vrp(data, time_windows)

    route = routes[0]

    visited = set(route)
    visited.discard(0)

    assert len(visited) < 2