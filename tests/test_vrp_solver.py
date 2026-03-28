"""
Tests du solveur VRP
"""

from vrp.model import create_data_model
from vrp.solver import solve_vrp


def test_vrp_basic():
    """
    Vérifie que le solver retourne des routes
    """

    matrix = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    demands = [0, 5, 5]

    vehicles = [{"capacity": 10, "depot": 0}]

    depots = [{"coord": (0, 0)}]

    data = create_data_model(matrix, demands, vehicles, depots)

    time_windows = [(0, 100)] * 3

    routes = solve_vrp(data, time_windows)

    assert isinstance(routes, list)
    assert len(routes) == 1