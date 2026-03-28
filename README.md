Smart Waste VRP - Optimisation des tournées de collecte

Description:

Ce projet propose un système d’optimisation des tournées de collecte des déchets basé sur le Vehicle Routing Problem.
Il prend en compte plusieurs contraintes :
- capacité des camions
- fenêtres de temps
- plusieurs dépôts
- mise à jour dynamique des données

Objectifs:

- optimiser les trajets des camions
- réduire les coûts de collecte
- limiter les émissions de CO2
- améliorer la gestion des déchets

Technologies utilisées :

- Python
- OR-Tools
- Redis
- OSRM
- Folium
- NetworkX

Fonctionnement:

1. génération des poubelles
2. mise à jour des niveaux de remplissage
3. stockage dans Redis
4. calcul des distances avec OSRM
5. optimisation avec OR-Tools
6. calcul des KPI
7. affichage des résultats (carte et graphe)

Modèles utilisés:

- VRP classique
- CVRP
- VRPTW
- VRP multi-dépôts
- VRP dynamique

KPI calculés:

- distance totale
- taux de remplissage
- émissions de CO2
- poubelles non collectées

Exécution:

python main.py

Tests:

python -m pytest -v

Auteur:

LEUBOU YAMDJEU EDDY RAYAN
