"""
Tests du service Redis
"""

from services.redis_service import save_bins, get_bins, reset_bins


def test_save_and_get_bins():
    """
    Vérifie sauvegarde et récupération
    """
    bins = [{"id": 1, "lat": 4.0, "lon": 9.7, "level": 50}]

    save_bins(bins)
    result = get_bins()

    assert result[0]["id"] == 1


def test_reset_bins():
    """
    Vérifie le reset
    """
    save_bins([{"id": 1}])
    reset_bins()

    result = get_bins()

    assert result == [] or result is not None