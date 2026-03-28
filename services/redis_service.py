import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

FILE_PATH = "data/bins_backup.json"


def save_bins(bins):
    """
    Sauvegarde dans Redis + fichier
    """

    # 🔹 Redis
    try:
        r.set("bins", json.dumps(bins))
    except Exception as e:
        print("⚠ Redis indisponible :", e)

    # 🔹 Backup fichier
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(bins, f)
    except Exception as e:
        print("Erreur sauvegarde fichier :", e)


def get_bins():
    """
    Récupère depuis Redis ou fichier
    """

    try:
        data = r.get("bins")
        if data:
            return json.loads(data)
    except Exception as e:
        print("⚠ Redis indisponible :", e)

    # 🔹 fallback fichier
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Erreur lecture fichier :", e)
        return []


def reset_bins():
    """
    Reset simulation MAIS garde backup
    """
    try:
        r.delete("bins")
    except Exception as e:
        print("Erreur reset Redis :", e)


def add_bin(bin_data):
    """
    Ajout d'une nouvelle poubelle dynamique
    """

    bins = get_bins() or []

    # 🔥 ID unique
    bin_data["id"] = int(time.time()*1000)

    bins.append(bin_data)

    save_bins(bins)