"""
Génération de poubelles aléatoires inititialement vides AVEC fenêtres de temps
"""

import random

def generate_random_bins(n):
    bins = []

    for _ in range(n):
        start = random.randint(0, 500)
        end = start + random.randint(100, 500)

        bins.append({
            "id": random.randint(1000,9999),
            "lat": random.uniform(4.03,4.08),
            "lon": random.uniform(9.70,9.80),
            "level": 0,
            "time_window": (start, end)  # 🔥 VRPTW sur poubelle
        })

    return bins