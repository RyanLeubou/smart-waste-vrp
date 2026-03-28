"""
Tests du module simulation
"""

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins


def test_generate_bins():
    """
    Vérifie que les poubelles sont bien générées
    """
    bins = generate_bins(10)

    assert len(bins) == 10
    assert "lat" in bins[0]
    assert "lon" in bins[0]
    assert bins[0]["level"] == 0


def test_update_bins():
    """
    Vérifie que les niveaux augmentent
    """
    bins = generate_bins(5)

    updated = update_bins(bins)

    for b in updated:
        assert b["level"] >= 0
        assert b["level"] <= 100