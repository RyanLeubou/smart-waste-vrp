from vrp.model import create_data_model
from vrp.solver import solve_vrp

def test_cvrp_capacity():

    matrix = [
        [0, 10, 10],
        [10, 0, 5],
        [10, 5, 0]
    ]

    demands = [0, 5, 10]

    vehicles = [{"capacity": 10, "depot": 0}]
    depots = [{"coord": (0, 0)}]

    time_windows = [(0, 10000)] * 3

    data = create_data_model(matrix, demands, vehicles, depots)

    routes = solve_vrp(data, time_windows)

    assert routes is not None