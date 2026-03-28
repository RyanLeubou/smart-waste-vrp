Smart Waste VRP

Ce projet implémente un système d’optimisation des tournées de collecte des déchets basé sur le Vehicle Routing Problem (VRP).  
L’objectif est d’améliorer l’efficacité des collectes en réduisant les distances parcourues, en respectant les contraintes opérationnelles et en adaptant les tournées en fonction de l’état réel des poubelles.

Le système a été conçu comme un module d’optimisation intégrable dans une architecture plus large comprenant une application web, une application mobile et un module d’intelligence artificielle.

Fonctionnement général

Le système repose sur un pipeline de traitement :

- génération ou récupération des données (poubelles)
- stockage et gestion des données
- filtrage et priorisation via le module IA
- calcul des distances réelles
- optimisation des tournées avec le solveur VRP
- calcul des indicateurs de performance
- visualisation des résultats

Variantes du VRP implémentées

Le solveur prend en charge plusieurs variantes du problème :

- VRP classique : optimisation des tournées en minimisant la distance totale
- CVRP : prise en compte de la capacité maximale des camions
- VRPTW : intégration des fenêtres de temps pour gérer les priorités de collecte
- VRP multi-dépôts : plusieurs points de départ permettant une meilleure couverture géographique
- VRP dynamique : recalcul des tournées en fonction de l’évolution des données à chaque itération

Module IA

Un module de prétraitement simule l’intégration avec un système de détection du niveau de remplissage des poubelles.

Ce module permet :
- de filtrer les poubelles avec un niveau inférieur à 40%
- d’attribuer une priorité aux poubelles restantes

Les priorités sont traduites en fenêtres de temps :
- poubelle pleine : priorité urgente
- niveau élevé : priorité élevée
- niveau moyen : priorité normale

Ainsi, le solveur VRP ne traite que les poubelles pertinentes, ce qui permet de réduire les déplacements inutiles.

Technologies utilisées et rôle

Python  
Langage principal du projet. Il permet de structurer le système en modules, d’implémenter la logique métier et d’orchestrer les différents composants.

OR-Tools  
Bibliothèque d’optimisation développée par Google. Elle est utilisée pour modéliser et résoudre le problème VRP en intégrant les contraintes de capacité, de temps et de multi-dépôts.

OSRM (Open Source Routing Machine)  
Permet de calculer des distances réelles basées sur le réseau routier. Contrairement à une distance géométrique, OSRM fournit des trajets réalistes en tenant compte des routes.

Redis  
Système de stockage en mémoire utilisé pour simuler un environnement temps réel. Il permet de stocker et récupérer rapidement les données des poubelles entre les différentes étapes du pipeline.

Celery  
Outil de gestion des tâches asynchrones. Il permet de lancer les calculs d’optimisation en arrière-plan sans bloquer les applications web ou mobile. Il est adapté aux calculs coûteux comme le VRP.

NetworkX  
Bibliothèque utilisée pour représenter le problème sous forme de graphe. Elle permet d’analyser les relations entre les nœuds (poubelles et dépôts).

Folium  
Utilisé pour la visualisation des tournées sur une carte interactive. Il permet d’afficher les routes optimisées de manière claire.

Pytest  
Framework de test utilisé pour valider le fonctionnement du système. Il permet de tester individuellement chaque module ainsi que l’intégration complète.

Métaheuristique utilisée

Le solveur repose sur une métaheuristique appelée Guided Local Search (GLS).

Le Guided Local Search est une technique d’optimisation qui améliore progressivement une solution initiale en explorant l’espace des solutions.  
Elle fonctionne en pénalisant certaines solutions locales afin d’éviter de rester bloqué dans des minima locaux.

Principe :
- une première solution est générée rapidement
- des pénalités sont ajoutées sur les choix sous-optimaux
- le solveur explore de nouvelles solutions en tenant compte de ces pénalités
- le processus est répété jusqu’à obtenir une solution améliorée

Pourquoi ce choix :

- le VRP est un problème NP-difficile, difficile à résoudre de manière exacte
- GLS permet d’obtenir de bonnes solutions en un temps limité
- elle est efficace pour les problèmes avec de nombreuses contraintes
- elle est intégrée dans OR-Tools et optimisée pour ce type de problème

Modélisation réaliste

Le système intègre plusieurs éléments pour se rapprocher de la réalité :

- distances issues du réseau routier réel (OSRM)
- estimation du temps de trajet avec une vitesse moyenne de 60 km/h
- gestion des priorités via des fenêtres de temps
- capacité limitée des camions
- possibilité d’ignorer certaines poubelles si nécessaire

Tests

Des tests unitaires et d’intégration ont été implémentés pour garantir la fiabilité du système.

Les tests permettent de valider :
- le solveur VRP
- les contraintes (capacité, temps, multi-dépôts)
- le pipeline complet (simulation → IA → VRP → métriques)

Le test d’intégration vérifie le fonctionnement global du système et assure sa cohérence.

Intégration dans le projet global

Le solveur VRP constitue le cœur du module IA d’optimisation des tournées.

Dans une architecture réelle :
- les données proviennent du module IA de détection
- Redis sert de couche intermédiaire
- Celery gère les calculs asynchrones
- les résultats sont envoyés au backend
- les applications web et mobile affichent les tournées

Le fichier main.py sert uniquement à la simulation et à la démonstration.

Auteur

LEUBOU YAMDJEU EDDY RAYAN
