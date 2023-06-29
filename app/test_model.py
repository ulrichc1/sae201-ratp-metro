import unittest

from model import Node, Edge, Graph


class NodeTests(unittest.TestCase):

    def setUp(self):
        """
        Création d'un objet Node pour les tests
        :return:
        """
        self.node = Node(id=1, nom="Station A", terminus=False, numligne="Ligne 1")

    def test_ajouter_station(self):
        """
        Test de la méthode ajouter_station
        :return:
        """
        other_node = Node(id=2, nom="Station B", terminus=False, numligne="Ligne 1")

        self.node.ajouter_station(other_node)  # Ajout d'une station
        self.assertEqual(self.node.get_station(), [other_node])  # Vérification de l'ajout

    def test_supprimer_station(self):
        """
        Test de la méthode supprimer_station
        :return:
        """
        other_node = Node(id=2, nom="Station B", terminus=False, numligne="Ligne 1")
        self.node.ajouter_station(other_node)  # Ajout d'une station

        self.node.supprimer_station(other_node)
        self.assertEqual(self.node.get_station(), [])  # Vérification de la suppression

    def test_get_id(self):
        """
        Test de la méthode get_id
        :return:
        """
        self.assertEqual(self.node.get_id(), 1)  # Vérification de l'id

    def test_get_nom(self):
        """
        Test de la méthode get_nom
        :return:
        """
        self.assertEqual(self.node.get_nom(), "Station A")  # Vérification du nom

    def test_get_terminus(self):
        """
        Test de la méthode get_terminus
        :return:
        """
        self.assertEqual(self.node.get_terminus(), False)  # Vérification du terminus

    def test_get_numligne(self):
        """
        Test de la méthode get_numligne
        :return:
        """
        self.assertEqual(self.node.get_numligne(), "Ligne 1")  # Vérification du numéro de ligne

    def test_set_id(self):
        """
        Test de la méthode set_id
        :return:
        """
        self.node.set_id(10)  # Modification de l'id
        self.assertEqual(self.node.get_id(), 10)  # Vérification de la modification

    def test_set_nom(self):
        """
        Test de la méthode set_nom
        :return:
        """
        self.node.set_nom("Pistache")  # Modification du nom
        self.assertEqual(self.node.get_nom(), "Pistache")  # Vérification de la modification

    def test_set_terminus(self):
        """
        Test de la méthode set_terminus
        :return:
        """
        self.node.set_terminus(True)  # Modification du terminus
        self.assertEqual(self.node.get_terminus(), True)  # Vérification de la modification

    def test_set_numligne(self):
        """
        Test de la méthode set_numligne
        :return:
        """
        self.node.set_numligne("18")  # Modification du numéro de ligne
        self.assertEqual(self.node.get_numligne(), "18")  # Vérification de la modification

    def test_str(self):
        """
        Test de la méthode __str__
        :return:
        """
        expected_output = "Station { id: 1, nom: Station A, terminus: False, ligne: Ligne 1 }"
        self.assertEqual(str(self.node), expected_output)  # Vérification de la sortie


class EdgeTests(unittest.TestCase):
    """
    Classe de test pour la classe Edge
    """

    def setUp(self):
        """
        Création d'un objet Edge pour les tests
        :return:
        """
        self.source_node = Node(id=1, nom="Station A", terminus=False, numligne="Ligne 1")  # Création d'un noeud source
        self.target_node = Node(id=2, nom="Station B", terminus=False, numligne="Ligne 1")  # Création d'un noeud cible
        self.edge = Edge(source=self.source_node, cible=self.target_node, temps=5)  # Création d'un edge

    def test_ajouter_edge(self):
        """
        Test de la méthode ajouter_edge
        :return:
        """
        other_edge = Edge(source=self.source_node, cible=self.target_node, temps=10)  # Création d'un autre edge

        self.edge.ajouter_edge(other_edge)  # Ajout d'un edge
        self.assertEqual(self.edge.edges, [other_edge])  # Vérification de l'ajout

    def test_supprimer_edge(self):
        """
        Test de la méthode supprimer_edge
        :return:
        """
        other_edge = Edge(source=self.source_node, cible=self.target_node, temps=10)  # Création d'un autre edge
        self.edge.ajouter_edge(other_edge)  # Ajout d'un edge

        self.edge.supprimer_edge(other_edge)  # Suppression d'un edge
        self.assertEqual(self.edge.edges, [])  # Vérification de la suppression

    def test_get_source(self):
        """
        Test de la méthode get_source
        :return:
        """
        self.assertEqual(self.edge.get_source(), self.source_node)  # Vérification du noeud source

    def test_get_cible(self):
        """
        Test de la méthode get_cible
        :return:
        """
        self.assertEqual(self.edge.get_cible(), self.target_node)  # Vérification du noeud cible

    def test_get_temps(self):
        """
        Test de la méthode get_temps
        :return:
        """
        self.assertEqual(self.edge.get_temps(), 5)  # Vérification du temps

    def test_set_source(self):
        """
        Test de la méthode set_source
        :return:
        """
        new_source = Node(id=3, nom="Station C", terminus=False, numligne="Ligne 2")
        self.edge.set_source(new_source)  # Modification du noeud source
        self.assertEqual(self.edge.get_source(), new_source)  # Vérification de la modification

    def test_set_cible(self):
        """
        Test de la méthode set_cible
        :return:
        """
        new_target = Node(id=4, nom="Station D", terminus=False, numligne="Ligne 2")
        self.edge.set_cible(new_target)  # Modification du noeud cible
        self.assertEqual(self.edge.get_cible(), new_target)  # Vérification de la modification

    def test_set_temps(self):
        """
        Test de la méthode set_temps
        :return:
        """
        new_temps = 8  # Nouveau temps
        self.edge.set_temps(new_temps)  # Modification du temps
        self.assertEqual(self.edge.get_temps(), new_temps)

    def test_str(self):
        """
        Test de la méthode __str__
        :return:
        """
        expected_output = "[source=Station { id: 1, nom: Station A, terminus: False, ligne: Ligne 1 }, cible=Station " \
                          "{ id: 2, nom: Station B, terminus: False, ligne: Ligne 1 }, temps=5]"
        self.assertEqual(str(self.edge), expected_output)  # Vérification de la sortie


class TestGraph(unittest.TestCase):
    """
    Classe de test pour la classe Graph
    """

    def setUp(self):
        """
        Création d'un objet Graph pour les tests
        :return:
        """
        self.graph = Graph(direction=False)

    def test_add_node(self):
        """
        Test de la méthode add_node
        :return:
        """
        node = Node(1, "Station 1", False, "Ligne 1")  # Création d'un noeud
        self.graph.add_node(node)  # Ajout d'un noeud
        self.assertIn(node, self.graph.stations)

    def test_add_edge(self):
        """
        Test de la méthode add_edge
        :return:
        """
        source = Node(1, "Station 1", False, "Ligne 1")  # Création d'un noeud source
        target = Node(2, "Station 2", False, "Ligne 2")  # Création d'un noeud cible
        self.graph.add_node(source)  # Ajout d'un noeud source
        self.graph.add_node(target)  # Ajout d'un noeud cible
        self.graph.add_edge(source.get_id(), target.get_id(), 5)  # Ajout d'un edge
        self.assertEqual(len(self.graph.dictionnaire[source.get_id()]), 1)  # Vérification de l'ajout

    def test_shortest_way(self):
        """
        Test de la méthode shortest_way
        :return:
        """
        node1 = Node(1, "Station 1", False, "Ligne 1")
        node2 = Node(2, "Station 2", False, "Ligne 2")
        node3 = Node(3, "Station 3", False, "Ligne 1")
        self.graph.add_node(node1)
        self.graph.add_node(node2)
        self.graph.add_node(node3)
        self.graph.add_edge(node1.get_id(), node2.get_id(), 5)
        self.graph.add_edge(node2.get_id(), node3.get_id(), 10)
        shortest_way = self.graph.shortest_way(node1.get_id(), node3.get_id())  # Calcul du plus court chemin
        self.assertEqual(shortest_way, [[1, 2, 3], 15])  # Vérification du plus court chemin

    def test_stations_list(self):
        """
        Test de la méthode stations_list
        :return:
        """
        node1 = Node(1, "Station 1", False, "Ligne 1")
        node2 = Node(2, "Station 2", False, "Ligne 1")
        node3 = Node(3, "Station 3", True, "Ligne 2")
        self.graph.add_node(node1)
        self.graph.add_node(node2)
        self.graph.add_node(node3)
        self.assertEqual(self.graph.stations_list("Ligne 1"), [node1, node2])  # Vérification de la liste des stations
        self.assertEqual(self.graph.stations_list("Ligne 2"), [node3])  # Vérification de la liste des stations

    def test_shortest_path_message(self):
        """
        Test de la méthode shortest_path_message
        :return:
        """
        shortest_path = [
            [1, 0, "Station 1", "Ligne 1", False],
            [2, 5, "Station 2", "Ligne 1", False],
            [3, 15, "Station 3", "Ligne 2", True]
        ]  # Plus court chemin
        expected_message = "Station : Station 1 - Ligne : Ligne 1 - Terminus : False - Temps : 0 secondes. \n" \
                           "Station : Station 2 - Ligne : Ligne 1 - Terminus : False - Temps : 5 secondes. \n" \
                           "Station : Station 3 - Ligne : Ligne 2 - Terminus : True - Temps : 15 secondes. \n"
        self.assertEqual(Graph.shortest_path_message(shortest_path), expected_message)  # Vérification du message

    def test_stations_list_message(self):
        """
        Test de la méthode stations_list_message
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        node1 = Node(1, "Station 1", False, "Ligne 1")
        node2 = Node(2, "Station 2", False, "Ligne 1")
        node3 = Node(3, "Station 3", True, "Ligne 2")
        stations_list = [node1, node2, node3]  # Liste des stations
        expected_message = "Station : Station 1 \n" \
                           "Station : Station 2 \n" \
                           "Station : Station 3 \n"
        self.assertEqual(Graph.stations_list_message(stations_list), expected_message)

    def test_find_correspondance(self):
        """
        Test de la méthode find_correspondance
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        node1 = Node(1, "Station 1", False, "Ligne 1")
        node2 = Node(2, "Station 2", False, "Ligne 1")
        node3 = Node(3, "Station 3", True, "Ligne 2")
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        graph.add_edge(node1.get_id(), node2.get_id(), 5)
        graph.add_edge(node2.get_id(), node3.get_id(), 10)

        correspondance = graph.find_correspondance("Ligne 1", "Ligne 2")  # Recherche de la correspondance
        expected_correspondance = {2,3}  # Correspondance attendue
        self.assertEqual(correspondance, expected_correspondance)  # Vérification de la correspondance

    def test_is_neighbor(self):
        """
        Test de la méthode is_neighbor
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        node1 = Node(1, "Station 1", "Ligne 1", "Terminus 1")
        node2 = Node(2, "Station 2", "Ligne 1", "Terminus 1")
        node3 = Node(3, "Station 3", "Ligne 2", "Terminus 2")
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        graph.add_edge(node1.get_id(), node2.get_id(), 5)
        graph.add_edge(node2.get_id(), node3.get_id(), 10)

        self.assertTrue(graph.is_neighbor(node1.get_id(), node2.get_id()))  # Vérification de la correspondance
        self.assertFalse(graph.is_neighbor(node1.get_id(), node3.get_id()))  # Vérification de la correspondance

    def test_is_path_with_correspondence_shorter(self):
        """
        Test de la méthode is_path_with_correspondence_shorter
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 2")
        self.graph.add_node(station1)
        self.graph.add_node(station2)
        self.graph.add_edge(station1.get_id(), station2.get_id(), 5)  # Ajout d'un arc entre les deux stations
        result = self.graph.is_path_with_correspondence_shorter(station1, station2)  # Vérification de la correspondance
        self.assertTrue(result)  # Vérification de la correspondance

    def test_get_correspondence_distance(self):
        """
        Test de la méthode get_correspondence_distance
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 2")
        distance = self.graph.get_correspondence_distance(station1, station2)  # Vérification de la correspondance
        self.assertEqual(distance, 9)

    def test_calculate_total_time(self):
        """
        Test de la méthode calculate_total_time
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        path = [
            [1, 0, "Station 1", "Ligne 1", False],
            [2, 5, "Station 2", "Ligne 1", False],
            [3, 15, "Station 3", "Ligne 2", True]
        ]  # Chemin
        total_time = self.graph.calculate_total_time(path)  # Calcul du temps total
        self.assertEqual(total_time, 9)  # Vérification du temps total

    def test_get_station_id_by_name(self):
        """
        Test de la méthode get_station_id_by_name
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 1")
        station3 = Node(3, "Station 3", True, "Ligne 2")
        stations = [station1, station2, station3]
        station_id = self.graph.get_station_id_by_name(stations, "Station 2")
        self.assertEqual(station_id, 2)

    def test_get_station_by_id(self):
        """
        Test de la méthode get_station_by_id
        :return:
        """
        graph = Graph(direction=False)
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 1")
        station3 = Node(3, "Station 3", True, "Ligne 2")
        self.graph.add_node(station1)
        self.graph.add_node(station2)
        self.graph.add_node(station3)
        retrieved_station = self.graph.get_station_by_id(2)  # Récupération de la station
        self.assertEqual(retrieved_station, station2)  # Vérification de la correspondance

    def test_get_station_line_by_id(self):
        """
        Test de la méthode get_station_line_by_id
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 1")
        station3 = Node(3, "Station 3", True, "Ligne 2")
        self.graph.add_node(station1)
        self.graph.add_node(station2)
        self.graph.add_node(station3)
        line = self.graph.get_station_line_by_id(2)  # Récupération de la ligne
        self.assertEqual(line, "Ligne 1")

    def test_p_distance(self):
        """
        Test de la méthode p_distance
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        self.graph.add_node(Node(1, "Station 1", False, "Ligne 1"))
        self.graph.add_node(Node(2, "Station 2", False, "Ligne 1"))
        self.graph.add_node(Node(3, "Station 3", True, "Ligne 2"))
        self.graph.add_edge(1, 2, 5)
        self.graph.add_edge(2, 3, 10)
        distance = self.graph.p_distance(1, 3, 2)  # Calcul de la distance
        self.assertEqual(distance, True)  # Vérification de la correspondance

    def test_path_message(self):
        """
        Test de la méthode path_message
        :return:
        """
        graph = Graph(direction=False)  # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 2")
        station3 = Node(3, "Station 3", False, "Ligne 1")
        station4 = Node(4, "Station 4", False, "Ligne 2")
        self.graph.add_node(station1)
        self.graph.add_node(station2)
        self.graph.add_node(station3)
        self.graph.add_node(station4)
        path = ([1, 2, 3, 4], 23) # Création d'un chemin
        expected_message = "Station 1 ( Ligne 1 ) -> Station 2 ( Ligne 2 ) -> Station 3 ( Ligne 1 ) -> Station 4 ( Ligne 2 )\nTemps total : 23 secondes" # Message attendu
        message = self.graph.path_message(path)
        self.assertEqual(message, expected_message) # Vérification de la correspondance

    def test_neighbors_stations(self):
        """
        Test de la méthode neighbors_stations
        :return:
        """
        graph = Graph(direction=False) # Création d'un objet Graph
        station1 = Node(1, "Station 1", False, "Ligne 1")
        station2 = Node(2, "Station 2", False, "Ligne 2")
        station3 = Node(3, "Station 3", False, "Ligne 1")
        self.graph.add_node(station1)
        self.graph.add_node(station2)
        self.graph.add_node(station3)
        self.graph.add_edge(station1.get_id(), station2.get_id(), 5)
        self.graph.add_edge(station2.get_id(), station3.get_id(), 10)
        neighbors = self.graph.neighbors_stations(station2.get_id()) # Récupération des voisins de la station 2
        expected_neighbors = [station1.get_id(), station3.get_id()] # Voisins attendus
        self.assertEqual(neighbors, expected_neighbors) # Vérification de la correspondance





if __name__ == '__main__':
    unittest.main()
