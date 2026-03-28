"""
Calcul des distances via OSRM 
"""

import requests
import math


def get_distance_matrix(locations):

    try:
        # 🔹 format OSRM
        coords = ";".join([f"{lon},{lat}" for lat, lon in locations])
        url = f"http://router.project-osrm.org/table/v1/driving/{coords}"

        response = requests.get(url, timeout=5)

        data = response.json()

        # 🔥 vérification réponse
        if "durations" not in data:
            raise Exception("Erreur OSRM")

        # 🔥 gestion None
        matrix = [
            [int(d) if d is not None else 999999 for d in row]
            for row in data["durations"]
        ]

        return matrix

    except Exception as e:
        print("⚠ OSRM indisponible :", e)

        # 🔹 fallback
        matrix = []

        for i in locations:
            row = []
            for j in locations:
                dist = math.sqrt((i[0]-j[0])**2 + (i[1]-j[1])**2)

                # conversion approx → mètres/temps
                row.append(int(dist * 111000))

            matrix.append(row)

        return matrix