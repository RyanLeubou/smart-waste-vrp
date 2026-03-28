"""
Module de traitement des données IA

- Filtrage des poubelles (seuil 40%)
- Attribution des priorités (VRPTW)
"""

def process_ai_output(bins):
    """
    Transforme les données issues du système IA
    en données exploitables par le VRP
    """

    processed = []

    for b in bins:
        level = b["level"]

        # ------------------------
        # FILTRAGE IA
        # ------------------------
        if level < 40:
            continue

        # ------------------------
        # PRIORITÉ (VRPTW)
        # ------------------------
        if level >= 90:
            b["time_window"] = (0, 50)      # urgent
        elif level >= 70:
            b["time_window"] = (0, 200)     # prioritaire
        else:
            b["time_window"] = (0, 500)     # normal

        processed.append(b)

    return processed