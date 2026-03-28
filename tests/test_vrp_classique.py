from vrp.model import create_data_model
from vrp.solver import solve_vrp


def test_vrp_classic():

    matrix = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    demands = [0, 0, 0]

    vehicles = [{"capacity": 100, "depot": 0}]
    depots = [{"coord": (0, 0)}]

    time_windows = [(0, 10000)] * 3

    data = create_data_model(matrix, demands, vehicles, depots)

    routes = solve_vrp(data, time_windows)

    assert routes is not None