"""
Création d'une poubelle spécifique AVEC fenêtre de temps
"""

def create_specific_bin(lat, lon, start=0, end=1000):

    return {
        "id": 9999,
        "lat": lat,
        "lon": lon,
        "level": 0,
        "time_window": (start, end)
    }