"""
Visualisation du graphe VRP (coloré)
"""

import networkx as nx
import matplotlib.pyplot as plt


def build_graph(locations):
    """
    Crée les noeuds du graphe
    """

    G = nx.Graph()

    for i, loc in enumerate(locations):
        G.add_node(i, pos=loc)

    return G


def draw_graph(G, routes, num_depots):
    """
    Affiche le graphe avec :
    - dépôts en vert
    - poubelles en bleu
    - routes colorées
    """

    pos = nx.get_node_attributes(G, 'pos')

    plt.figure(figsize=(8, 6))

    # 🔹 dessiner les noeuds
    colors = []

    for node in G.nodes:
        if node < num_depots:
            colors.append("green")  # dépôts
        else:
            colors.append("blue")   # poubelles

    nx.draw_networkx_nodes(G, pos, node_color=colors)

    nx.draw_networkx_labels(G, pos)

    # 🔥 routes des camions
    route_colors = ["red", "orange", "purple", "brown", "pink"]

    for i, route in enumerate(routes):

        edges = []

        for j in range(len(route) - 1):
            edges.append((route[j], route[j+1]))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color=route_colors[i % len(route_colors)],
            width=2
        )

    plt.title("Graphe VRP (dépôts / poubelles / routes)")
    plt.show()