import random

def update_bins(bins):
    """
    Mise à jour des poubelles :
    - niveau de remplissage
    - fenêtre de temps (VRPTW)
    """

    for b in bins:

        # ------------------------
        # Remplissage dynamique
        # ------------------------
        b["level"] = min(100, b["level"] + random.randint(5, 20))

        # ------------------------
        # VRPTW (fenêtre de temps)
        # ------------------------
        start = random.randint(0, 500)
        end = start + random.randint(200, 500)

        b["time_window"] = (start, end)

    return bins