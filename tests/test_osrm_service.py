"""
Tests OSRM (fallback inclus)
"""

from services.osrm_service import get_distance_matrix


def test_distance_matrix():
    """
    Vérifie génération matrice
    """
    locations = [(4.05, 9.75), (4.06, 9.76)]

    matrix = get_distance_matrix(locations)

    assert len(matrix) == 2
    assert len(matrix[0]) == 2
    assert matrix[0][0] == 0