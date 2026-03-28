"""
Tests du module graph
"""

from visualization.graph import build_graph


def test_graph_creation():
    """
    Vérifie création du graphe
    """

    locations = [(4.05, 9.75), (4.06, 9.76)]

    G = build_graph(locations)

    assert len(G.nodes) == 2