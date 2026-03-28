"""
Visualisation des routes VRP sur carte (Folium)
"""

import folium


def display_routes(locations, routes, num_depots):
    """
    Affiche :
    - dépôts (verts)
    - poubelles (bleues)
    - routes par camion (couleurs différentes)
    """

    # 🔹 centre de la carte
    m = folium.Map(location=locations[0], zoom_start=13)

    # 🔹 couleurs des routes
    colors = ["red", "blue", "green", "orange", "purple", "black"]

    # --------------------------
    # 🔥 MARQUEURS
    # --------------------------

    for i, loc in enumerate(locations):

        if i < num_depots:
            # dépôts
            folium.Marker(
                location=loc,
                popup=f"Dépôt {i}",
                icon=folium.Icon(color="green", icon="home")
            ).add_to(m)

        else:
            # poubelles
            folium.Marker(
                location=loc,
                popup=f"Poubelle {i}",
                icon=folium.Icon(color="blue", icon="trash")
            ).add_to(m)

    # --------------------------
    # 🔥 ROUTES
    # --------------------------

    for i, route in enumerate(routes):

        points = [locations[idx] for idx in route]

        folium.PolyLine(
            points,
            color=colors[i % len(colors)],
            weight=5,
            opacity=0.8
        ).add_to(m)

    # --------------------------
    # 🔹 sauvegarde
    # --------------------------

    m.save("map.html")

    print("🗺 Carte générée avec succès")