# Authors: Ulrich COUDIN, Hugo MOLINIER, Mélissa COQUERELLE, Noé LAMARQUE
# Groupe : Ulrich COUDIN, Hugo MOLINIER, Mélissa COQUERELLE, Noé LAMARQUE
# Date: 23-06-2023
# SAÉ : SAÉ 2.01 - Développement Orienté Objets

import csv
import heapq
from typing import List, Dict, Any
from queue import PriorityQueue
from collections import defaultdict


class Node:
    """
    Classe Node (Noeud du graphe) représentant une station
    """

    def __init__(self, id: int, nom: str, terminus: bool, numligne: str):
        """
        Initialisation de la station
            :param id: Identifiant de la station
            :param nom: Nom de la station
            :param terminus: true si la station est un terminus, false sinon
            :param numligne: numéro de la ligne de la station
        """
        self.id = id  # Identifiant de la station
        self.nom = nom  # Nom de la station
        self.terminus = terminus  # true si la station est un terminus, false sinon
        self.numligne = numligne  # Numéro de la ligne de la station
        self.station = []  # Liste des stations

    def ajouter_station(self, station_node: Any):
        """
        Ajouter une station à la liste des stations
            :param station_node:  Station à ajouter
            :type station_node: Any
            :return:
        """
        if station_node not in self.station:  # Vérifier si la station n'est pas déjà dans la liste
            self.station.append(station_node)  # Ajouter la station à la liste

    def supprimer_station(self, station_node: Any):
        """
        Supprimer une station de la liste des stations
            :param station_node:  Station à supprimer
            :type station_node: Any
            :return:
        """
        self.station.remove(station_node)  # Supprimer la station de la liste

    def get_id(self) -> int:
        """
        Récupérer l'identifiant de la station
            :return: Identifiant de la station
            :rtype: int
        """
        return self.id

    def get_nom(self) -> str:
        """
        Récupérer le nom de la station
            :return: Nom de la station
            :rtype: str
        """
        return self.nom

    def get_terminus(self) -> bool:
        """
        Récupérer le terminus de la station
            :return: true si la station est un terminus, false sinon
            :rtype: bool
        """
        return self.terminus

    def get_numligne(self) -> str:
        """
        Récupérer le numéro de la ligne de la station
            :return: Numéro de la ligne de la station
            :rtype: str
        """
        return self.numligne

    def get_station(self) -> List[Any]:
        """
        Récupérer la liste des stations
            :return: Liste des stations
            :rtype: List[Any]
        """
        return self.station

    def set_id(self, id: int):
        """
        Modifier l'identifiant de la station
            :param id:  Identifiant de la station
            :type id: int
            :return:
        """
        self.id = id

    def set_nom(self, nom: str):
        """
        Modifier le nom de la station
            :param nom:  Nom de la station
            :type nom: str
            :return:
        """
        self.nom = nom

    def set_terminus(self, terminus: bool):
        """
        Modifier le terminus de la station
            :param terminus:  true si la station est un terminus, false sinon
            :type terminus: bool
            :return:
        """
        self.terminus = terminus

    def set_numligne(self, numligne: str):
        """
        Modifier le numéro de la ligne de la station
            :param numligne: numéro de la ligne
            :type numligne: str
            :return:
        """
        self.numligne = numligne

    def set_station(self, station):
        """
        Modifier la liste des stations
            :param station:
            :type station:
            :return:
        """
        self.station = station

    def __str__(self) -> str:
        """
        Afficher la station
            :return: Affichage de la station
        """
        return f"Station {{ id: {self.id}, nom: {self.nom}, terminus: {self.terminus}, ligne: {self.numligne} }}"


class Edge:
    """
    Classe Edge (Relation du graphe) représentant une relation entre deux stations
    """

    def __init__(self, source: Node, cible: Node, temps: int):
        """
        Initialisation de la relation entre deux stations
            :param source:  Station source
            :type source: Node
            :param cible:  Station cible
            :type cible: Node
            :param temps:  Temps entre la station source et la station cible
            :type temps: int
        """
        self.source = source
        self.cible = cible
        self.temps = temps
        self.edges = []

    def ajouter_edge(self, relation):
        """
        Ajouter une relation entre deux stations
            :param relation:  Relation entre deux stations
            :type relation: Edge
        :return:
        """
        if relation not in self.edges:  # Vérifier si la relation n'est pas déjà dans la liste
            self.edges.append(relation)

    def supprimer_edge(self, relation):
        """
        Supprimer une relation entre deux stations
            :param relation:
            :type relation:
        :return:
        """
        self.edges.remove(relation)  # Supprimer la relation de la liste

    def get_source(self):
        """
        Récupérer la station source
            :return: Station source
        """
        return self.source

    def get_cible(self):
        """
        Récupérer la station cible
            :return:  Station cible
        """
        return self.cible

    def get_temps(self):
        """
        Récupérer le temps entre la station source et la station cible
        :return:
        """
        return self.temps

    def set_source(self, source):
        """
        Modifier la station source
            :param source:
            :type source:
        :return:
        """
        self.source = source

    def set_cible(self, cible):
        """
        Modifier la station cible
            :param cible:
            :type cible:
        :return:
        """
        self.cible = cible

    def set_temps(self, temps):
        """
        Modifier le temps entre la station source et la station cible
            :param temps:
            :type temps:
        :return:
        """
        self.temps = temps

    def __str__(self):
        """
        Afficher la relation entre deux stations
            :return: Affichage de la relation entre deux stations
        """
        return f"[source={self.source}, cible={self.cible}, temps={self.temps}]"


class Csv:
    """
    Classe Csv permettant de lire un fichier csv
    """

    def __init__(self, filename):
        """
        Initialisation de la lecture du fichier csv
            :param filename: Nom du fichier csv
            :type filename: str
        """
        self.stations = []
        self.relations = []
        self.filename = filename

    def lecture_csv_station(self):
        """
        Lire le fichier csv contenant les stations
            :return:  Liste des stations
        """
        with open(f"data/{self.filename}", newline='', encoding='utf-8') as csvfile:  # Ouvrir le fichier csv
            reader = csv.reader(csvfile, delimiter=';')  # Lire le fichier csv
            next(reader)  # Ignorer la première ligne
            for row in reader:  # Parcourir le fichier csv
                terminus = int(row[2]) == 1  # Vérifier si la station est un terminus
                station = Node(int(row[0]), row[3], terminus, row[1])  # Créer une station
                self.stations.append(station)  # Ajouter la station à la liste
        return self.stations  # Retourner la liste des stations

    def lecture_csv_relation(self):
        """
        Lire le fichier csv contenant les relations entre les stations
            :return:  Liste des relations entre les stations
        """
        with open(f"data/{self.filename}", newline='', encoding='utf-8') as csvfile:  # Ouvrir le fichier csv
            reader = csv.reader(csvfile, delimiter=';')  # Lire le fichier csv
            next(reader)  # Ignorer la première ligne
            for row in reader:  # Parcourir le fichier csv
                relation = Edge(int(row[0]), int(row[1]), int(row[2]))  # Créer une relation entre deux stations
                self.relations.append(relation)  # Ajouter la relation à la liste
        return self.relations  # Retourner la liste des relations


class DisjointSets:
    """
    Classe DisjointSets permettant de créer des ensembles disjoints
    """

    def __init__(self):
        """
        Initialisation des ensembles disjoints
        """
        self.parent = {}  # Parent de l'arbre
        self.rank = {}  # Rang de l'arbre

    def make_set(self, x: int):
        """
        Créer un ensemble
            :param x: Ensemble à créer
            :type x: int
        """
        self.parent[x] = x  # Le parent de l'arbre est lui-même
        self.rank[x] = 0

    def find_set(self, x: int):
        """
        Trouver un ensemble
            :param x: Ensemble à trouver
            :type x: int
        """
        if x != self.parent[x]: # Vérifier si le parent de l'arbre est lui-même
            self.parent[x] = self.find_set(self.parent[x])
        return self.parent[x] # Retourner le parent de l'arbre

    def union(self, x, y):
        """
        Unir deux ensembles
            :param x: Ensemble à unir
            :type x: int
            :param y: Ensemble à unir
            :type y: int
        """
        x_root = self.find_set(x) # Trouver le parent de l'arbre
        y_root = self.find_set(y) # Trouver le parent de l'arbre

        if x_root == y_root: # Vérifier si les deux parents sont les mêmes
            return

        if self.rank[x_root] < self.rank[y_root]: # Vérifier si le rang de l'arbre est inférieur
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]: # Vérifier si le rang de l'arbre est supérieur
            self.parent[y_root] = x_root
        else: # Vérifier si le rang de l'arbre est égal
            self.parent[y_root] = x_root
            self.rank[x_root] += 1


class Graph:
    """
    Classe Graph représentant le graphe des stations
    """

    def __init__(self, direction: bool):
        """
        Initialisation du graphe des stations
            :param direction: true si le graphe est orienté, false sinon
            :type direction: bool
        """
        self.stations = []  # Liste des stations
        self.dictionnaire = {}  # Dictionnaire des relations
        self.direction = direction  # Vérifier si le graphe est orienté

    def add_node(self, node: Node):
        """
        Ajouter une station au graphe
            :param node: Station à ajouter
            :type node: Node
            :return:
        """
        self.stations.insert(node.get_id(), node)  # Ajouter la station à la liste
        self.dictionnaire[node.get_id()] = []

    def add_edge(self, source: int, target: int, temps: int):
        """
        Ajouter une relation entre deux stations
            :param source:  Station source
            :type source: Node
            :param target:  Station cible
            :type target: Node
            :param temps:  Temps entre la station source et la station cible
            :type temps: int
            :return:
        """
        if source not in self.dictionnaire:  # Vérifier si la station source n'est pas dans le dictionnaire
            self.dictionnaire[source] = []  # Ajouter la station source au dictionnaire
        self.dictionnaire[source].append(Edge(source, target, temps))  # Ajouter la relation entre les deux stations

        if not self.direction:  # Vérifier si le graphe n'est pas orienté
            if target not in self.dictionnaire:  # Vérifier si la station cible n'est pas dans le dictionnaire
                self.dictionnaire[target] = []  # Ajouter la station cible au dictionnaire
            self.dictionnaire[target].append(Edge(target, source, temps))  # Ajouter la relation entre les deux stations

    def get_stations(self):
        """
        Obtenir la liste des stations
            :return: Liste des stations
        """
        return self.stations

    def find_min_spanning_tree(self) -> list:
        """
        Trouver l'arbre minimum couvrant du graphe en utilisant l'algorithme de Kruskal
            :return: Liste des arêtes de l'arbre minimum couvrant
            :rtype: list
        """
        # Créer une liste pour stocker les arêtes de l'arbre minimum couvrant
        min_spanning_tree = []

        # Créer un ensemble pour stocker les ensembles disjointes des sommets
        disjoint_sets = DisjointSets()

        # Créer un ensemble pour stocker les sommets du graphe
        for node in self.stations:
            disjoint_sets.make_set(node.get_id())

        # Trier toutes les arêtes du graphe par ordre croissant de poids
        edges = []
        for node_id in self.dictionnaire:
            for edge in self.dictionnaire[node_id]:
                edges.append(edge)
        edges.sort(key=lambda x: x.temps)

        # Parcourir toutes les arêtes triées
        for edge in edges:
            source = edge.get_source()
            target = edge.get_cible()

            # Vérifier si l'ajout de l'arête crée un cycle dans l'arbre minimum couvrant
            if disjoint_sets.find_set(source) != disjoint_sets.find_set(target):
                # Les sommets ne sont pas dans le même ensemble, ajouter l'arête à l'arbre minimum couvrant
                min_spanning_tree.append(edge)

                # Fusionner les ensembles des sommets
                disjoint_sets.union(source, target)

        return min_spanning_tree

    def dijkstra(self, source: int, target: int) -> List[List[Any]]:
        """
        Algorithme de Dijkstra permettant de trouver le plus court chemin entre deux stations
            :param source: Station source
            :type source: Node
            :param target: Station cible
            :type target: Node
            :return:
        """
        distances = {node: float('inf') for node in self.dictionnaire}  # Initialiser les distances
        distances[source] = 0  # Initialiser la distance de la station source à 0
        previous = {node: None for node in self.dictionnaire}  # Initialiser les nœuds précédents

        queue = [(0, source)]  # Initialiser la file de priorité
        heapq.heapify(queue)  # Créer la file de priorité

        while queue:  # Parcourir la file de priorité
            current_distance, current_node = heapq.heappop(queue)  # Récupérer le nœud courant et sa distance
            if current_node == target:  # Vérifier si le nœud courant est la station cible
                # Construire le chemin à partir des nœuds précédents
                path = []  # Initialiser le chemin
                while current_node is not None:  # Parcourir les nœuds précédents
                    node_info = [current_node, distances[current_node]]  # Récupérer le nœud précédent et sa distance
                    node = self.get_station_by_id(current_node)  # Récupérer la station précédente
                    node_info.extend([node.get_nom(), node.get_numligne(), node.get_terminus()])  # Ajouter les infos
                    path.append(node_info)  # Ajouter le nœud précédent au chemin
                    current_node = previous[current_node]  # Récupérer le nœud précédent
                path.reverse()  # Inverser le chemin
                return path  # Retourner le chemin

            if current_distance > distances[current_node]:  # Vérifier si la distance courante est supérieure à la
                continue

            for edge in self.dictionnaire[current_node]:  # Parcourir les relations du nœud courant
                neighbor = edge.cible  # Récupérer la station cible
                distance = current_distance + edge.temps  # Calculer la distance entre le nœud courant et la station
                # cible

                if distance < distances[neighbor]:  # Vérifier si la distance est inférieure à la distance de la station
                    distances[neighbor] = distance  # Mettre à jour la distance de la station
                    previous[neighbor] = current_node  # Mettre à jour le nœud précédent
                    heapq.heappush(queue, (distance, neighbor))  # Ajouter la station à la file de priorité

        # Aucun chemin trouvé
        return []

    def shortest_way(self, source: int, target: int) -> list:
        """
        Retourne le plus court chemin entre deux stations (liste -> (id de stations (chemin),temps)) grâce à
        l'algorithme de Dijkstra
            :param source: Station source
            :type source: Node
            :param target: Station cible
            :type target: Node
            :return: Plus court chemin
            :rtype: list
        """
        shortest_path = self.dijkstra(source, target)  # Plus court chemin
        total_time = 0  # Temps total du plus court chemin
        if shortest_path:  # Vérifier si le plus court chemin existe
            total_time = shortest_path[-1][1]  # Temps total du plus court chemin
        # On garde que les id des stations
        shortest_path = [node[0] for node in shortest_path]
        return [shortest_path, total_time]

    def stations_list(self, line: str) -> List[Node]:
        """
        Retourne la liste des stations d'une ligne
            :param line: Ligne
            :type line: str
            :return:  Liste des stations
            :rtype: List[Node]
        """
        stationsList = []  # Liste des stations
        for station in self.stations:  # Parcours des stations
            if station.get_numligne() == line:  # Si la ligne est la même que celle passée en paramètre
                stationsList.append(station)  # Ajout de la station à la liste
        return stationsList  # Retour de la liste des stations

    @staticmethod
    def shortest_path_message(shortest_path: List[List[Any]]) -> str:
        """
        Retourne le message du plus court chemin
            :param shortest_path: Plus court chemin
            :type shortest_path: List[List[Any]]
            :return: Message
            :rtype: str
        """
        message = ""  # Message
        for nodeInfo in shortest_path:  # Parcours du chemin
            message += "Station : " + str(nodeInfo[2]) + " - Ligne : " + str(nodeInfo[3]) + " - Terminus : " + str(
                nodeInfo[4]) + " - Temps : " + str(nodeInfo[1]) + " secondes. \n"  # Ajout des informations du sommet
        return message  # Retour du message

    @staticmethod
    def stations_list_message(stations_list: List[Node]) -> str:
        """
        Retourne le message de la liste des stations
            :param stations_list:
            :return: Message
            :rtype: str
        """
        # Trier la liste des stations par ID
        stations_list.sort(key=lambda x: x.get_id())

        message = ""  # Message
        for station in stations_list:  # Parcours de la liste des stations
            message += "Station : " + station.get_nom() + " \n"  # Ajout des informations de la station
        return message  # Retour du message

    def find_correspondance(self, line1: str, line2: str) -> set[int]:
        """
        Retourne l'ensemble des correspondances entre deux lignes
            :param line1: Ligne 1
            :param line2: Ligne 2
            :return: Ensemble des correspondances
            :rtype: set[int]
        """
        correspondance = set()  # Ensemble des correspondances

        # Récupération de la liste des stations de la ligne 1
        stationsLine1 = self.stations_list(line1)
        print(stationsLine1)
        # Récupération de la liste des stations de la ligne 2
        stationsLine2 = self.stations_list(line2)
        print(stationsLine2)
        # Parcours des stations de la ligne 1
        for stationLine1 in stationsLine1:
            # Récupération des voisins de la station de la ligne 1
            neighbors = self.dictionnaire[stationLine1.get_id()]

            # Parcours des voisins de la station de la ligne 1
            for edge in neighbors:
                # Récupération de l'id du voisin
                neighborId = edge.cible

                # Vérification si le voisin est une station de la ligne 2
                for stationLine2 in stationsLine2:
                    if stationLine2.get_id() == neighborId:
                        # Ajouter la correspondance à l'ensemble
                        correspondance.add(stationLine1.get_id())
                        correspondance.add(stationLine2.get_id())
                        break

        return correspondance

    def find_paths(self, source: int, cible: int) -> List[List[Any]]:
        """
        Retourne la liste des chemins entre deux stations
            :param source: Station source
            :param cible: Station cible
            :return: Liste des chemins
            :rtype: List[List[Any]]
        """
        # Récupération de la station source
        s = self.get_station_by_id(source)
        c = self.get_station_by_id(cible)

        # Cas 0 : Station A = Station B
        if s.get_id() == c.get_id():
            print("Les stations de départ et d'arrivée sont identiques.")
            return []  # Retourne une liste vide

        # Cas 1 : Station A → Station B (voisin)
        if self.is_neighbor(s.get_id(), c.get_id()):
            print("Les stations de départ et d'arrivée sont voisines.")
            path = self.dijkstra(s.get_id(), c.get_id())
            # On affiche le chemin et la durée du trajet;
            print(self.shortest_path_message(self.dijkstra(s.get_id(), c.get_id())))
            return [path]

        # Cas 2 : Station A → Station B (même ligne)
        if s.get_numligne() == c.get_numligne() and not self.is_path_with_correspondence_shorter(s, c):
            print(
                "Les stations de départ et d'arrivée sont sur la même ligne et aucune correspondance n'est nécessaire.")
            path = self.dijkstra(s.get_id(), c.get_id())
            return [path]

        # Correspondances entre les lignes
        correspondance = self.find_correspondance(s.get_numligne(), c.get_numligne())

        # Liste des chemins
        paths = []

        # Pour chaque correspondance
        for station in correspondance:
            # Récupération de la liste des stations de la ligne 1
            stationsLine1 = self.stations_list(s.get_numligne())

            # Récupération de la liste des stations de la ligne 2
            stationsLine2 = self.stations_list(c.get_numligne())

            # Estimation du temps de trajet (3 minutes entre deux stations et 6 minutes pour un changement de ligne)
            estimation = 0

            # Recherche du chemin le plus court de la source à la station de correspondance
            path1 = self.dijkstra(s.get_id(), self.get_station_id_by_name(stationsLine1, station))
            if not path1:
                continue  # Pas de chemin trouvé, passer à la prochaine correspondance
            estimation += self.calculate_total_time(path1)

            # Recherche du chemin le plus court de la station de correspondance à la cible
            path2 = self.dijkstra(self.get_station_id_by_name(stationsLine2, station), c.get_id())
            if not path2:
                continue  # Pas de chemin trouvé, passer à la prochaine correspondance
            estimation += self.calculate_total_time(path2)

            # Ajout du chemin à la liste des chemins
            pathInfo = []
            combinedPath = []

            # Ajout des stations du premier chemin (path1) à combinedPath
            for nodeInfo in path1:
                combinedPath.append(nodeInfo)

            # Ajout des stations du second chemin (path2) à combinedPath, en ignorant la première station (doublon)
            for i in range(1, len(path2)):
                combinedPath.append(path2[i])

            pathInfo.append(combinedPath)
            pathInfo.append(estimation)
            paths.append(pathInfo)

        # Tri des chemins en fonction du temps estimé
        paths.sort(key=lambda path: path[1])

        # Limiter la liste aux 3 chemins les plus rapides
        if len(paths) > 3:
            paths = paths[:3]

        # Affichage des résultats pour chaque chemin
        for pathInfo in paths:
            path = pathInfo[0]
            combinedPath = pathInfo[0]
            estimation = pathInfo[1]

            # Affichage du chemin
            chemin = "Chemin : "
            for nodeInfo in combinedPath:
                chemin += nodeInfo[2] + " -> "
            chemin = chemin[:-4]
            print(chemin)
            print("\nChemin :")
            print(self.shortest_path_message(combinedPath))
            print("Temps estimé : " + str(estimation) + " minutes.")
            print()

            # Nombre de stations
            nbStations = len(combinedPath) - 1

            # Nombre de correspondances
            nbCorrespondances = 0

            # Affichage du nombre de stations et de correspondances
            print("Nombre de stations : " + str(nbStations))
            print("Nombre de correspondances : " + str(nbCorrespondances))
            print()

        return paths

    def is_neighbor(self, source: int, target: int) -> bool:
        """
        Vérifie si deux stations sont voisines
            :param source:  Station source
            :type source: int
            :param target: Station cible
            :type target: int
            :return: True si les stations sont voisines
            :rtype: bool
        """
        if source in self.dictionnaire:  # Si la station source est dans le dictionnaire
            edges = self.dictionnaire[source]  # Récupération des arrêtes
            for edge in edges:  # Pour chaque arrête
                cible = edge.cible  # Récupération de la cible
                if cible == target:  # Si la cible est la station cible
                    return True
        return False  # Sinon, retourne faux

    def is_path_with_correspondence_shorter(self, station1: Node, station2: Node) -> bool:
        """
        Vérifie si le chemin avec correspondance est plus court que le chemin direct
            :param station1: Station 1
            :type station1: Node
            :param station2: Station 2
            :type station2: Node
            :return: True si le chemin avec correspondance est plus court que le chemin direct
            :rtype: bool
        """
        directDistance = abs(station1.get_id() - station2.get_id()) * 3  # Distance directe
        correspondanceDistance = self.get_correspondence_distance(station1, station2)  # Distance avec correspondance
        return directDistance < correspondanceDistance  # Retourne vrai si la distance directe est plus courte

    @staticmethod
    def get_correspondence_distance(station1: Node, station2: Node) -> int:
        """
        Calcule la distance entre deux stations avec correspondance
            :param station1: Première station
            :type station1: Node
            :param station2: Seconde station
            :type station2: Node
            :return: Distance
        """
        directDistance = abs(station1.get_id() - station2.get_id())  # Distance directe
        return directDistance * 3 + 6  # Retourne la distance directe + 6 minutes de correspondance

    @staticmethod
    def calculate_total_time(path: List[List[Any]]) -> int:
        """
        Calcule le temps total d'un chemin
            :param path: Chemin
            :type path: List[List[Any]]
            :return: Temps total
            :rtype: int
        """
        totalTime = 0  # Temps total
        numStations = len(path)  # Nombre de stations

        for i in range(numStations):  # Pour chaque station
            totalTime += 3

            if i < numStations - 1:  # Si ce n'est pas la dernière station
                currentNode = path[i]  # Station actuelle
                nextNode = path[i + 1]  # Station suivante

                if currentNode[2] == nextNode[2]:  # Si les stations sont sur la même ligne
                    totalTime += 6  # Ajout de 6 minutes de correspondance

        return totalTime  # Retourne le temps total

    @staticmethod
    def get_station_id_by_name(stations: List[Node], name: str) -> int:
        """
        Récupère l'id d'une station à partir de son nom
            :param stations: Liste des stations
            :param name: Nom de la station
            :return: id de la station
            :rtype: int
        """
        for station in stations:  # Pour chaque station
            if station.get_nom() == name:  # Si le nom de la station est le même que celui recherché
                return station.get_id()
        return -1  # Retourne -1 si la station n'a pas été trouvée

    def get_station_by_id(self, id: int) -> Node:
        """
        Récupère une station à partir de son id
            :param id: id de la station
            :type id: int
            :return:  Station
            :rtype: Node
        """
        for station in self.stations:  # Pour chaque station
            if station.get_id() == id:  # Si l'id de la station est le même que celui recherché
                return station
        return None  # Retourne None si la station n'a pas été trouvée

    def get_station_name_by_id(self, id: int) -> str:
        """
        Récupère le nom d'une station à partir de son id
            :param id: id de la station
            :type id: int
            :return: Nom de la station
            :rtype: str
        """
        for station in self.stations:  # Pour chaque station
            if station.get_id() == id:  # Si l'id de la station est le même que celui recherché
                return station.get_nom()
        return None  # Retourne None si la station n'a pas été trouvée

    def get_station_line_by_id(self, id: int) -> int:
        """
        Récupère le numéro de ligne d'une station à partir de son id
            :param id: id de la station
            :type id: int
            :return:    Numéro de ligne
            :rtype: int
        """
        for station in self.stations:  # Pour chaque station
            if station.get_id() == id:  # Si l'id de la station est le même que celui recherché
                return station.get_numligne()  # Retourne le numéro de ligne
        return None  # Retourne None si la station n'a pas été trouvée

    def p_distance(self, source: int, cible: int, distance: int) -> bool:
        """
        Vérifie si la distance entre deux stations est inférieure à une distance donnée
            :param source: id de la station source
            :type source: int
            :param cible: id de la station cible
            :type cible: int
            :param distance:  distance
            :type distance: int
            :return:   True si la distance est inférieure à la distance donnée
            :rtype: bool
        """
        if source == cible:  # Si les stations sont les mêmes
            return distance == 0  # Retourne vrai si la distance est nulle

        if distance < 0:  # Si la distance est négative
            return False

        visited = set()  # Stations visitées
        queue = [(source, 0)]  # File d'attente

        while queue:  # Tant que la file d'attente n'est pas vide
            current_station, current_distance = queue.pop(0)  # Récupération de la station et de la distance

            if current_station == cible and current_distance == distance:  # Si la station est la cible et que la
                # distance est la distance recherchée
                return True  # Retourne vrai

            if current_distance > distance:  # Si la distance est supérieure à la distance recherchée
                break  # Arrêt de la boucle

            if current_station not in visited:  # Si la station n'a pas été visitée
                visited.add(current_station)  # Ajout de la station aux stations visitées

                neighbors = self.dictionnaire[current_station]  # Récupération des voisins de la station
                for arc in neighbors:  # Pour chaque voisin
                    neighbor_station = arc.cible  # Récupération de la station voisine
                    new_distance = current_distance + 1  # Calcul de la nouvelle distance

                    if neighbor_station not in visited:  # Si la station voisine n'a pas été visitée
                        queue.append(
                            (neighbor_station, new_distance))  # Ajout de la station voisine à la file d'attente
        return False  # Retourne faux si la distance n'a pas été trouvée

    def find_shortest_path_with_intermediate(self, source: int, intermediate: int, target: int):
        """
        Trouve le chemin le plus court entre la source et la destination en passant par une étape intermédiaire
            :param source: id de la station source
            :type source: int
            :param intermediate:  id de la station intermédiaire
            :type intermediate: int
            :param target:  id de la station cible
            :type target: int
            :return:  Chemin le plus court et temps total
        """
        # Trouver le chemin le plus court de la source à l'étape intermédiaire
        shortest_path1 = self.shortest_way(source, intermediate)

        # Trouver le chemin le plus court de l'étape intermédiaire à la destination
        shortest_path2 = self.shortest_way(intermediate, target)

        # Combiner les deux chemins en un seul
        combined_path = shortest_path1[0] + shortest_path2[0]

        # Calculer le temps total du trajet combiné
        total_time = shortest_path1[1] + shortest_path2[1]

        # Suppression des doublons
        combined_path = list(dict.fromkeys(combined_path))

        # Retourner le chemin combiné et le temps total
        return combined_path, total_time

    def find_shortest_path_min_correspondences_with_intermediate(self, source: int, intermediate: int,
                                                                 target: int) -> tuple:
        """
        Trouve le chemin le plus court entre la source et la destination en passant par une étape intermédiaire
            :param source: id de la station source
            :type source: int
            :param intermediate: id de la station intermédiaire
            :type intermediate: int
            :param target: id de la station cible
            :type target: int
            :return: Chemin le plus court et temps total
            :rtype: tuple
        """
        # Trouver le chemin le plus court de la source à l'étape intermédiaire
        shortest_path1 = self.dijkstra_min_correspondences(source, intermediate)

        # Trouver le chemin le plus court de l'étape intermédiaire à la destination
        shortest_path2 = self.dijkstra_min_correspondences(intermediate, target)

        # Combiner les deux chemins en un seul
        combined_path = shortest_path1[0] + shortest_path2[0]

        # Calculer le temps total du trajet combiné
        total_time = shortest_path1[1] + shortest_path2[1]

        # Suppression des doublons
        combined_path = list(dict.fromkeys(combined_path))

        # Retourner le chemin combiné et le temps total
        return combined_path, total_time

    def dijkstra_min_correspondences(self, source: int, target: int) -> tuple[List[int], int]:
        """
        Trouve le chemin le plus court entre la source et la destination en utilisant l'algorithme de Dijkstra
            :param source: id de la station source
            :type source: int
            :param target: id de la station cible
            :type target: int
            :return: Chemin le plus court et temps total
            :rtype: tuple
        """
        distances = {node: float('inf') for node in self.dictionnaire} # Initialisation des distances
        distances[source] = 0
        previous = {node: None for node in self.dictionnaire} # Initialisation des précédents

        queue = [(0, source)]
        heapq.heapify(queue)
        if source == target:
            return [source], 0

        while queue: # Tant que la file d'attente n'est pas vide
            current_distance, current_node = heapq.heappop(queue)
            if current_node == target:
                # Construire le chemin à partir des nœuds précédents
                path = []
                while current_node is not None: # Tant que le nœud courant n'est pas nul
                    path.append(current_node)
                    current_node = previous[current_node] # Récupération du nœud précédent
                path.reverse()

                total_time = distances[target]  # Temps total
                return path, total_time - 5000

            if current_distance > distances[current_node]:
                continue

            for edge in self.dictionnaire[current_node]:
                neighbor = edge.cible
                distance = current_distance + edge.temps
                if self.get_station_by_id(neighbor).get_numligne() != self.get_station_by_id(
                        current_node).get_numligne(): # Si les deux stations ne sont pas sur la même ligne
                    distance += 5000

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # Aucun chemin trouvé
        return [], 0

    def path_message(self, path: tuple[List[int], int]) -> str:
        """
        Construit le message à partir du chemin
            :param path: chemin
            :type path: tuple
            :return: message à afficher
            :rtype: str
        """
        message = ""  # Initialisation du message
        for i in range(len(path[0])):  # Pour chaque station du chemin
            if i == len(path[0]) - 1:  # Si c'est la dernière station
                station_name = self.get_station_name_by_id(path[0][i])  # Récupération du nom de la station
                station_name = station_name.replace('_', ' ')  # Remplacement des _ par des espaces
                message += station_name  # Ajout du nom de la station au message
                message += " ( " + str(
                    self.get_station_line_by_id(path[0][i])) + " )"  # Ajout de la ligne de la station au message
            else:
                station_name = self.get_station_name_by_id(path[0][i])  # Récupération du nom de la station
                station_name = station_name.replace('_', ' ')  # Remplacement des _ par des espaces
                message += station_name  # Ajout du nom de la station au message
                message += " ( " + str(
                    self.get_station_line_by_id(path[0][i])) + " )"  # Ajout de la ligne de la station au message
                message += " -> "  # Ajout d'une flèche au message
        message += f"\nTemps total : {path[1]} secondes"  # Ajout du temps total au message
        return message  # Retourne le message

    def more_accessibility_1station(self, station: int):
        """
        Retourne la station la plus accessible à partir d'une station
            :param station: id de la station
            :type station: int
            :return: station la plus accessible et distance
            :rtype: tuple
        """
        List = []  # Liste des stations
        accessibility = None  # Station la plus accessible
        min_distance = float('inf')  # Distance minimale
        for i in range(1, 15):  # Pour chaque ligne
            if i != self.get_station_by_id(station).numligne:
                List += self.find_correspondance(str(self.get_station_by_id(station).numligne), str(i))

        for i in List:  # Pour chaque station
            if i != station:
                dijkstra_accessibilité = self.dijkstra(station, i)

                distance = dijkstra_accessibilité[-1][1]
                if distance < min_distance:
                    # on garde le terminus le plus proche
                    min_distance = distance
                    accessibility = self.get_station_by_id(
                        dijkstra_accessibilité[0][0])  # la station du début de la liste
        return (accessibility, min_distance)  # Retourne la station la plus accessible et la distance

    def compare_accessibility(self, stationA: int, stationB: int) -> str:
        """
        Compare l'accessibilité de deux stations
            :param stationA: id de la station A
            :type stationA: int
            :param stationB: id de la station B
            :type stationB: int
            :return: message à afficher
            :rtype: str
            """
        stationB_accessibility = self.more_accessibility_1station(stationB)  # Accessibilité de la station B
        stationA_accessibility = self.more_accessibility_1station(stationA)  # Accessibilité de la station A
        if stationA_accessibility[1] < stationB_accessibility[1]:  # Si l'accessibilité de la station A est meilleure
            return "La station " + str(self.get_station_by_id(stationA)) + " est plus ACCESSIBLE que la station " + str(
                self.get_station_by_id(stationB))  # Retourne le message
        elif stationA_accessibility[1] > stationB_accessibility[1]:
            return "La station " + str(self.get_station_by_id(stationB)) + " est plus ACCESSIBLE que la station " + str(
                self.get_station_by_id(stationA))  # Retourne le message
        else:
            return "Les deux stations sont autant accessibles l'un que l'autre"  # Retourne le message

    def neighbors_stations(self, station: int) -> List[Node]:
        """
        Retourne les voisins d'une station
            :param station:  id de la station
            :type station: int
            :return:  liste des voisins
            :rtype: List[Node]
        """
        neighbors = []  # Initialisation des voisins
        for arc in self.dictionnaire[station]:  # Pour chaque arc de la station
            neighbors.append(self.get_station_by_id(arc.cible).get_id())  # Ajout du voisin à la liste
        return neighbors  # Retourne la liste des voisins

    def compare_centralization_temps(self, station1: int, station2: int, p: int) -> str:
        """
        Compare la centralisation des deux stations
            :param station1: id de la station 1
            :type station1: int
            :param station2: id de la station 2
            :type station2: int
            :param p: temps maximum
            :type p: int
            :return: message à afficher
        """
        count1 = 0
        count2 = 0
        for i in range(376):
            if self.dijkstra(i, station1)[-1][1] <= p:
                count1 += 1
            if self.dijkstra(i, station2)[-1][1] <= p:
                count2 += 1
        if count1 > count2:
            return f"{self.get_station_by_id(station1).get_nom()} est plus centrale que {self.get_station_by_id(station2).get_nom()}."
        elif count1 < count2:
            return f"{self.get_station_by_id(station2).get_nom()} est plus centrale que {self.get_station_by_id(station1).get_nom()}."
        else:
            return "Les deux stations sont aussi centrales."

    def compare_centralization_stations(self, station1: int, station2: int, p: int) -> str:
        """
        Compare la centralisation des stations données à p distance (nombre de stations) de la station.
        Retourne un message indiquant la station la plus centrale.
            :param station1: id de la station 1
            :type station1: int
            :param station2: id de la station 2
            :type station2: int
            :param p: distance
            :type p: int
            :return: message
            :rtype: str
        """
        count1 = 0
        count2 = 0
        for i in range(376):  # Pour chaque station
            if len(self.dijkstra(i, station1)) <= p:  # Si la distance est inférieure à p
                count1 += 1
            if len(self.dijkstra(i, station2)) <= p:  # Si la distance est inférieure à p
                count2 += 1
        if count1 > count2:  # Si la station 1 est plus centrale
            return f"{self.get_station_by_id(station1).get_nom()} est plus centrale que {self.get_station_by_id(station2).get_nom()}."
        elif count1 < count2:  # Si la station 2 est plus centrale
            return f"{self.get_station_by_id(station2).get_nom()} est plus centrale que {self.get_station_by_id(station1).get_nom()}."
        else:
            return "Les deux stations sont aussi centrales."

    def compare_terminus_proximity(self, station1: int, station2: int) -> str:
        """
        Compare la proximité des deux stations à un terminus
            :param station1: id de la station 1
            :type station1: int
            :param station2: id de la station 2
            :type station2: int
            :return: message à afficher
            :rtype: str
        """
        terminus1 = self.find_nearest_terminus(station1)  # Trouve le terminus le plus proche de la station 1

        terminus2 = self.find_nearest_terminus(station2)  # Trouve le terminus le plus proche de la station 2
        if station1 == station2:  # Si les deux stations sont les mêmes
            return "Les deux stations sont les mêmes."
        station1 = self.get_station_by_id(station1)
        station2 = self.get_station_by_id(station2)
        if terminus1[1] < terminus2[1]:  # Si la distance entre la station 1 et le terminus 1 est plus petite que la
            # distance entre la station 2 et le terminus 2
            return f"{station1.get_nom()} est plus proche d'un terminus ({terminus1[0]})que {station2.get_nom()}."
        elif terminus1[1] > terminus2[1]:  # Si la distance entre la station 2 et le terminus 2 est plus petite que la
            # distance entre la station 1 et le terminus 1
            return f"{station2.get_nom()} est plus proche d'un terminus ({terminus2[0]}) que {station1.get_nom()}."
        elif terminus1[1] == terminus2[1]:  # Si les deux stations sont à la même distance d'un terminus
            return "Les deux stations sont également proches d'un terminus."

    def find_nearest_terminus(self, station1: int):
        """
        Trouve le terminus le plus proche de la station donnée
            :param station1: id de la station
            :type station1: int
            :return: terminus le plus proche et distance
            :rtype: tuple
        """
        terminus_stations = [self.get_station_by_id(station) for station in self.dictionnaire.keys() if
                             self.get_station_by_id(station).get_terminus()]  # Liste des stations terminus
        min_distance = float('inf')  # distance infinie
        nearest_terminus = None  # terminus le plus proche

        for terminus in terminus_stations:
            # pour chaque terminus on fait dijkstra entre la station1 et le terminus
            dijkstra_terminus = self.dijkstra(terminus.get_id(), station1)
            distance = dijkstra_terminus[-1][1]
            if distance < min_distance:
                # on garde le terminus le plus proche
                min_distance = distance
                nearest_terminus = self.get_station_by_id(dijkstra_terminus[0][0])  # la station du début de la liste
        return (nearest_terminus, min_distance)  # retourne le terminus le plus proche et la distance

    def __str__(self):
        """
        Affichage du graphe
            :return: graphe et stations
            :rtype: str
        """
        return f"Graphe : {self.dictionnaire} - stations : {self.stations}"  # Retourne le graphe et les stations
