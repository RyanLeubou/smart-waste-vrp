"""
Simulation du remplissage des poubelles en temps réel
"""

import random

def update_bins(bins):
    """
    Augmente aléatoirement le niveau de remplissage
    """

    for b in bins:

        # augmentation aléatoire
        increment = random.randint(1, 10)

        b["level"] = min(100, b["level"] + increment)

        # 🔥 si poubelle devient critique → on peut ajuster la fenêtre
        if b["level"] > 80:
            b["time_window"] = (0, 300)  # urgente

    return bins