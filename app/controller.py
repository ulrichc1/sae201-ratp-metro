# Authors: Ulrich COUDIN, Hugo MOLINIER
# Groupe : Ulrich COUDIN, Hugo MOLINIER, Mélissa COQUERELLE, Noé LAMARQUE
# Date: 23-06-2023
# SAÉ : SAÉ 2.01 - Développement Orienté Objets
from flask import Flask, render_template, request, send_from_directory
from model import Csv, Graph, Node, Edge
import networkx as nx
import json
import urllib.request
import os

app = Flask(__name__)


# Chargement des données (IDs des stations double version : fichier 'data/id_correspondences.json')
def load_ids() -> dict:
    """
    Charge les IDs des stations depuis un fichier JSON
        :return: Dictionnaire des IDs des stations
        :rtype: dict
    """
    dictionary = {}  # Dictionnaire vide
    try:  # On essaie d'ouvrir le fichier JSON
        with open('data/id_correspondences.json.', 'r') as file:  # Ouverture du fichier en lecture
            dictionary = json.load(file)  # Chargement du fichier JSON dans le dictionnaire
    except FileNotFoundError:  # Si le fichier n'est pas trouvé
        print("Le fichier JSON n'a pas été trouvé.")
    except json.JSONDecodeError:  # Si le fichier JSON est mal formaté
        print("Le fichier JSON est mal formaté.")
    return dictionary  # On retourne le dictionnaire


try:  # Chargement des données
    station_csv = Csv("stations.csv")
    relation_csv = Csv("relations.csv")
    stations = station_csv.lecture_csv_station()  # Chargement des stations
    relations = relation_csv.lecture_csv_relation()  # Chargement des relations
    station_ids = load_ids()  # Chargement des IDs des stations
    print(station_ids)  # Affichage des IDs des stations
    # Construction du graphe
    graphe_ratp = Graph(False)  # Graphe non orienté
    for station in stations:  # Ajout des stations au graphe
        graphe_ratp.add_node(station)
    for relation in relations:  # Ajout des relations au graphe
        graphe_ratp.add_edge(relation.source, relation.cible, relation.temps)
except Exception as e:  # Si une erreur est levée
    print("Erreur : " + str(e))
finally:  # Dans tous les cas
    print("OK")

# Tests
try:
    print(f"\n Chemins les plus courts : \n")
    print(graphe_ratp.find_shortest_path_with_intermediate(0, 6, 250))
    print(graphe_ratp.find_shortest_path_with_intermediate(71, 17, 363))
    print(graphe_ratp.find_shortest_path_with_intermediate(71, 18, 363))
    print(f"\n Stations voisines (Châtelet) : \n")
    print(graphe_ratp.neighbors_stations(71))
    print(f"\n Liste de stations (ligne 1) : \n")
    print(graphe_ratp.stations_list('1'))
    print(f"\n Chemin le plus court avec le moins de correspondences : \n")
    min_cor_chat_bast = graphe_ratp.dijkstra_min_correspondences(71, 18)
    print(graphe_ratp.path_message(min_cor_chat_bast))
    print(f"\n Correspondances entre deux lignes (ligne 1 et 7): \n")
    print(graphe_ratp.find_correspondance("1", "7"))
    print(f"\n Station à proximité d'un terminus (comparaison) \n")
    print(graphe_ratp.compare_terminus_proximity(364,365))
    print(f"\n Station accessible (comparaison plus proche d'une correspondance) \n")
    print(graphe_ratp.compare_accessibility(148, 161))
    print(f"\n Station la plus centrale (stations) (comparaison plus de correspondances à p-distance (3 stations) ) \n")
    print(graphe_ratp.compare_centralization_stations(71, 18, 3))
    print(f"\n Station la plus centrale (temps) (comparaison plus de correspondances à n-secondes (300) \n")
    print(graphe_ratp.compare_centralization_temps(71, 18, 300))

except Exception as e:
    print("Erreur : " + str(e))


# Images
@app.route('/images/<path:filename>')
def serve_image(filename: str) -> str:
    """
    Renvoie lien vers image
        :param filename:  nom de l'image
        :type filename: str
        :return:  lien vers image
        :rtype: str
    """
    return send_from_directory('static/images', filename)


def load_id_correspondences() -> dict:
    """
    Charge les correspondances entre les IDs des stations et les noms des stations
        :return: Dictionnaire des correspondances
        :rtype: dict
    """
    url = "https://data.ulrichcoudin.com/ids/id_correspondences.json"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        correspondences = json.loads(data)
    return correspondences


# Filtre Jinja pour formater le temps
@app.template_filter('format_time')
def format_time(time) -> str:
    """
    Formate le temps
        :param time: Temps à formater
        :type time: float
        :return:  Temps formaté
        :rtype: str
    """
    minutes = int(time)  # Partie entière pour les minutes
    seconds = int((time - minutes) * 60)  # Partie décimale pour les secondes

    # Formater la chaîne de temps
    time_str = f"{minutes} minutes"
    if seconds > 0:
        time_str += f" {seconds} secondes"

    return time_str


# Page d'accueil
@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """
    Page d'accueil
        :return:  Page d'accueil
        :rtype: str
    """
    return render_template('index.html')


@app.route('/shortest_path_time', methods=['GET', 'POST'])
def shortest_path_time() -> str:
    """
    Page du plus court chemin en temps entre deux stations
        :return:  Page du plus court chemin en temps entre deux stations
        :rtype: str
    """
    total_time = 0
    shortest_path = []
    if request.method == 'POST':
        # Récupérer les noms des stations à partir du formulaire
        station1 = int(request.form['station1'])
        station2 = int(request.form['station2'])

        try:
            # Récupérer les noms des stations à partir de leur ID
            source = graphe_ratp.get_station_name_by_id(station1)
            target = graphe_ratp.get_station_name_by_id(station2)

            # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
            source = source.replace('_', ' ')
            target = target.replace('_', ' ')
            line1 = graphe_ratp.get_station_line_by_id(station1)
            line2 = graphe_ratp.get_station_line_by_id(station2)
            if line1:
                source += f" (Ligne {line1})"
            if line2:
                target += f" (Ligne {line2})"
            # Calcul du chemin le plus court
            shortest_path_result = graphe_ratp.shortest_way(station1, station2)

            shortest_path = shortest_path_result[0]
            # On transforme les IDs en noms de stations avec lignes
            shortest_path_names = []
            # Conversion des ids des stations actuelles avec les vrais ids (station_ids)
            shortest_path_ids = [station_ids[str(station_id)] for station_id in shortest_path]

            for station_id in shortest_path:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                shortest_path_names.append(station_name)
            shortest_path = shortest_path_names
            total_time = shortest_path_result[1] / 60
            # On garde 2 chiffres après la virgule
            total_time = round(total_time, 2)


        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('shortest_path_time.html', error="Erreur : " + str(e))
        # Rendu du template avec les résultats
        return render_template('shortest_path_time.html', source=source, target=target,
                               shortest_path=shortest_path,
                               total_time=total_time, stations=stations, shortest_path_ids=shortest_path_ids)

    return render_template('shortest_path_time.html', stations=stations, shortest_path=shortest_path,
                           total_time=total_time, )


@app.route('/shortest_path_correspondance', methods=['GET', 'POST'])
def shortest_path_correspondance() -> str:
    """
    Page du plus court chemin en nombre de correspondances entre deux stations
        :return: Page du plus court chemin en nombre de correspondances entre deux stations
        :rtype: str
    """
    total_time = 0
    shortest_path = []
    if request.method == 'POST':
        # Récupérer les noms des stations à partir du formulaire
        station1 = int(request.form['station1'])
        station2 = int(request.form['station2'])

        try:
            # Récupérer les noms des stations à partir de leur ID
            source = graphe_ratp.get_station_name_by_id(station1)
            target = graphe_ratp.get_station_name_by_id(station2)

            # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
            source = source.replace('_', ' ')
            target = target.replace('_', ' ')
            line1 = graphe_ratp.get_station_line_by_id(station1)
            line2 = graphe_ratp.get_station_line_by_id(station2)
            if line1:
                source += f" (Ligne {line1})"
            if line2:
                target += f" (Ligne {line2})"
            # Calcul du chemin le plus court
            shortest_path_result = graphe_ratp.dijkstra_min_correspondences(station1, station2)

            shortest_path = shortest_path_result[0]
            # On transforme les IDs en noms de stations avec lignes
            shortest_path_names = []
            # Conversion des ids des stations actuelles avec les vrais ids (station_ids)
            shortest_path_ids = [station_ids[str(station_id)] for station_id in shortest_path]

            for station_id in shortest_path:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                shortest_path_names.append(station_name)
            shortest_path = shortest_path_names
            total_time = shortest_path_result[1] / 60
            # On garde 2 chiffres après la virgule
            total_time = round(total_time, 2)


        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('shortest_path_correspondance.html', error="Erreur : " + str(e))
        # Rendu du template avec les résultats
        return render_template('shortest_path_correspondance.html', source=source, target=target,
                               shortest_path=shortest_path,
                               total_time=total_time, stations=stations, shortest_path_ids=shortest_path_ids)

    return render_template('shortest_path_correspondance.html', stations=stations, shortest_path=shortest_path,
                           total_time=total_time, )


@app.route('/shortest_path_time_intermediate', methods=['GET', 'POST'])
def shortest_path_time_intermediate() -> str:
    """
    Page du plus court chemin en temps entre deux stations avec une station intermédiaire
        :return: Page du plus court chemin en temps entre deux stations avec une station intermédiaire
        :rtype: str
    """
    total_time = 0
    shortest_path = []
    if request.method == 'POST':
        # Récupérer les noms des stations à partir du formulaire
        station1 = int(request.form['station1'])
        intermediate_s = int(request.form['intermediate'])
        station2 = int(request.form['station2'])

        try:
            # Récupérer les noms des stations à partir de leur ID
            source = graphe_ratp.get_station_name_by_id(station1)
            intermediate = graphe_ratp.get_station_name_by_id(intermediate_s)
            target = graphe_ratp.get_station_name_by_id(station2)

            # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
            source = source.replace('_', ' ')
            intermediate = intermediate.replace('_', ' ')
            target = target.replace('_', ' ')
            line1 = graphe_ratp.get_station_line_by_id(station1)
            line_intermediate = graphe_ratp.get_station_line_by_id(intermediate_s)
            line2 = graphe_ratp.get_station_line_by_id(station2)
            if line1:
                source += f" (Ligne {line1})"
            if line2:
                target += f" (Ligne {line2})"
            if line_intermediate:
                intermediate += f" (Ligne {line_intermediate})"
            # Calcul du chemin le plus court
            shortest_path_result = graphe_ratp.find_shortest_path_with_intermediate(station1, intermediate_s, station2)

            shortest_path = shortest_path_result[0]
            # On transforme les IDs en noms de stations avec lignes
            shortest_path_names = []
            # Conversion des ids des stations actuelles avec les vrais ids (station_ids)
            shortest_path_ids = [station_ids[str(station_id)] for station_id in shortest_path]

            for station_id in shortest_path:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                shortest_path_names.append(station_name)
            shortest_path = shortest_path_names
            total_time = shortest_path_result[1] / 60
            # On garde 2 chiffres après la virgule
            total_time = round(total_time, 2)


        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('shortest_path_time_intermediate.html', error="Erreur : " + str(e))
        # Rendu du template avec les résultats
        return render_template('shortest_path_time_intermediate.html', source=source, target=target,
                               intermediate=intermediate, shortest_path=shortest_path,
                               total_time=total_time, stations=stations, shortest_path_ids=shortest_path_ids)
    return render_template('shortest_path_time_intermediate.html', stations=stations,
                           shortest_path=shortest_path,
                           total_time=total_time, )


@app.route('/shortest_path_correspondance_intermediate', methods=['GET', 'POST'])
def shortest_path_correspondance_intermediate() -> str:
    """
    Page du plus court chemin en nombre de correspondances entre deux stations avec une station intermédiaire
        :return: Page du plus court chemin en nombre de correspondances entre deux stations avec une station intermédiaire
        :rtype: str
    """
    total_time = 0  # Temps total du trajet
    shortest_path = []  # Chemin le plus court
    if request.method == 'POST':
        # Récupérer les noms des stations à partir du formulaire
        station1 = int(request.form['station1'])
        intermediate_s = int(request.form['intermediate'])
        station2 = int(request.form['station2'])

        try:
            # Récupérer les noms des stations à partir de leur ID
            source = graphe_ratp.get_station_name_by_id(station1)
            intermediate = graphe_ratp.get_station_name_by_id(intermediate_s)
            target = graphe_ratp.get_station_name_by_id(station2)

            # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
            source = source.replace('_', ' ')
            intermediate = intermediate.replace('_', ' ')
            target = target.replace('_', ' ')
            line1 = graphe_ratp.get_station_line_by_id(station1)
            line_intermediate = graphe_ratp.get_station_line_by_id(intermediate_s)
            line2 = graphe_ratp.get_station_line_by_id(station2)
            if line1:
                source += f" (Ligne {line1})"
            if line2:
                target += f" (Ligne {line2})"
            if line_intermediate:
                intermediate += f" (Ligne {line_intermediate})"
            # Calcul du chemin le plus court
            shortest_path_result = graphe_ratp.find_shortest_path_min_correspondences_with_intermediate(station1,
                                                                                                        intermediate_s,
                                                                                                        station2)

            shortest_path = shortest_path_result[0]
            # On transforme les IDs en noms de stations avec lignes
            shortest_path_names = []
            # Conversion des ids des stations actuelles avec les vrais ids (station_ids)
            shortest_path_ids = [station_ids[str(station_id)] for station_id in shortest_path]

            for station_id in shortest_path:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                shortest_path_names.append(station_name)
            shortest_path = shortest_path_names
            total_time = shortest_path_result[1] / 60
            # On garde 2 chiffres après la virgule
            total_time = round(total_time, 2)

        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('shortest_path_correspondance_intermediate.html', error="Erreur : " + str(e))
        # Rendu du template avec les résultats
        return render_template('shortest_path_correspondance_intermediate.html', source=source, target=target,
                               intermediate=intermediate, shortest_path=shortest_path,
                               total_time=total_time, stations=stations, shortest_path_ids=shortest_path_ids)

    return render_template('shortest_path_correspondance_intermediate.html', stations=stations,
                           shortest_path=shortest_path,
                           total_time=total_time, )


@app.route('/possible_correspondences', methods=['GET', 'POST'])
def possible_correspondences() -> str:
    """
    Page des correspondances possibles
        :return: Page des correspondances possibles
        :rtype: str
    """
    if request.method == 'POST':
        # Récupérer les lignes à partir du formulaire
        line1 = request.form['line_nb1']
        line2 = request.form['line_nb2']
        try:
            # Chercher les correspondances possibles
            correspondences = graphe_ratp.find_correspondance(line1, line2)
            # On transforme les IDs en noms de stations avec lignes
            correspondences_names = []
            for station_id in correspondences:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                correspondences_names.append(station_name)
            # Conversion des ids des stations actuelles avec les vrais ids (station_ids)
            correspondences_ids = [station_ids[str(station_id)] for station_id in correspondences]
        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('possible_correspondences.html', error="Erreur : " + str(e))
        # Rendu du template avec les résultats
        return render_template('possible_correspondences.html', correspondences_name=correspondences_names,
                               correspondences_list=correspondences_ids, line_nb1=line1, line_nb2=line2)
    return render_template('possible_correspondences.html')


@app.route('/list_stations_lines', methods=['GET', 'POST'])
def list_stations_lines() -> str:
    """
    Page de la liste des stations d'une ligne
        :return: Page de la liste des stations d'une ligne
        :rtype: str
    """
    if request.method == 'POST':
        # Récupérer le numéro de la ligne à partir du formulaire
        line_nb = request.form['line']
        try:
            # Récupérer les stations de la ligne
            stations_line = graphe_ratp.stations_list(line_nb)
            # On converti les stations en tableau d'id
            stations_line = [station.get_id() for station in stations_line]
            # On transforme les IDs en noms de stations avec lignes
            stations_line_names = []
            for station_id in stations_line:
                station_name = graphe_ratp.get_station_name_by_id(station_id)
                # Remplacer "_" par des espaces et ajouter la ligne entre parenthèses si disponible
                station_name = station_name.replace('_', ' ')
                line = graphe_ratp.get_station_line_by_id(station_id)
                if line:
                    station_name += f" (Ligne {line})"
                stations_line_names.append(station_name)
            # On converti les ids des stations actuelles avec les vrais ids (station_ids)
            stations_line = [station_ids[str(station_id)] for station_id in stations_line]

            # Rendu du template avec les résultats
            return render_template('list_stations_lines.html', stations_line_names=stations_line_names,
                                   stations_line=stations_line, line_nb=line_nb)
        except Exception as e:
            print("Erreur : " + str(e))
            return render_template('list_stations_lines.html', error="Erreur : " + str(e))
    return render_template('list_stations_lines.html')


def minimum_spanning_tree() -> None:
    """
    Arbre couvrant de poids minimum
        :return:
    """
    min_spanning_tree = graphe_ratp.find_min_spanning_tree()

    # Créez un objet nx.Graph()
    nx_graph = nx.Graph()

    # Ajoutez les nœuds au graphe nx.Graph()
    for node in graphe_ratp.stations:
        nx_graph.add_node(node)
    # Ajoutez les arêtes de l'arbre minimum couvrant au graphe nx.Graph()
    for edge in min_spanning_tree:
        source_id = edge.get_source()
        target_id = edge.get_cible()
        nx_graph.add_edge(source_id, target_id)
    # Affichez le graphe
    pos = nx.spring_layout(nx_graph)  # Calculez la disposition des nœuds
    nx.draw_networkx(nx_graph, pos=pos, with_labels=True)  # Dessinez le graphe
    nx.write_gexf(nx_graph, "graph.gexf")  # Exportez le graphe au format GEXF pour Gephi


# minimum_spanning_tree() # Décommentez pour afficher l'arbre couvrant de poids minimum sous fichier graph.gexf

if __name__ == '__main__':  # On lance le serveur Flask
    app.run(debug=False)
