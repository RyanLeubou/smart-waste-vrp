from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins


def test_dynamic_behavior():

    bins = generate_bins(5)

    levels_before = [b["level"] for b in bins]

    bins = update_bins(bins)

    levels_after = [b["level"] for b in bins]

    assert any(a > b for a, b in zip(levels_after, levels_before))