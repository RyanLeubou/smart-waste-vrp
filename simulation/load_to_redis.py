"""
Simulation complète des poubelles (dynamique)
"""

import time
import random

from simulation.generate_random_bins import generate_random_bins as generate_bins
from simulation.update_bins import update_bins
from simulation.specific_bins import create_specific_bin
from services.redis_service import get_bins, save_bins


def start_simulation(num_bins):
    """
    Simulation dynamique réaliste :
    - remplissage
    - ajout de nouvelles poubelles
    - persistance Redis
    """

    # 🔹 initialisation
    bins = generate_bins(num_bins)

    while True:

        # 🔥 récupérer aussi les nouvelles poubelles ajoutées via interface
        redis_bins = get_bins()

        if redis_bins:
            bins = redis_bins

        # 🔹 mise à jour du remplissage
        bins = update_bins(bins)

        # 🔥 ajout aléatoire de nouvelles poubelles (événement)
        if random.random() < 0.2:  # 20% de chance
            new_bin = create_specific_bin(
                lat=random.uniform(4.03, 4.08),
                lon=random.uniform(9.70, 9.80),
                start=0,
                end=500
            )

            bins.append(new_bin)

            print("🆕 Nouvelle poubelle ajoutée (simulation)")

        # 🔹 sauvegarde
        save_bins(bins)

        print(f"♻️ Mise à jour {len(bins)} poubelles")

        time.sleep(5)