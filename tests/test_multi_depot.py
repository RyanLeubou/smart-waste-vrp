from vrp.model import create_data_model
from vrp.solver import solve_vrp

def test_multi_depot():

    matrix = [
        [0, 10, 10, 20],
        [10, 0, 5, 15],
        [10, 5, 0, 10],
        [20, 15, 10, 0]
    ]

    demands = [0, 0, 5, 5]

    depots = [
        {"coord": (0, 0)},
        {"coord": (1, 1)}
    ]

    vehicles = [
        {"capacity": 10, "depot": 0},
        {"capacity": 10, "depot": 1}
    ]

    time_windows = [(0, 10000)] * 4

    data = create_data_model(matrix, demands, vehicles, depots)

    routes = solve_vrp(data, time_windows)

    assert len(routes) == 2