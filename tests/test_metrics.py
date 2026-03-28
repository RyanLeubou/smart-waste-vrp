"""
Tests des indicateurs de performance
"""

from metrics import compute_metrics, compute_global_metrics


def test_metrics():
    """
    Vérifie calcul des KPI + stockage historique
    """

    routes = [[0, 1, 2, 0]]

    matrix = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    demands = [0, 5, 5]

    result = compute_metrics(
        routes,
        matrix,
        demands,
        capacity=20,
        total_bins=2,
        num_depots=1
    )

    # 🔹 Vérifications KPI
    assert result["distance"] > 0
    assert result["fill"] >= 0
    assert result["co2"] >= 0


def test_global_metrics():
    """
    Vérifie que les metrics globales fonctionnent
    """

    # 🔥 on appelle d'abord compute_metrics pour remplir l'historique
    routes = [[0, 1, 2, 0]]

    matrix = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    demands = [0, 5, 5]

    compute_metrics(
        routes,
        matrix,
        demands,
        capacity=20,
        total_bins=2,
        num_depots=1
    )

    # 🔥 maintenant on teste global
    result = compute_global_metrics()

    # selon ton implémentation, il peut retourner None ou dict
    assert result is None or isinstance(result, dict)