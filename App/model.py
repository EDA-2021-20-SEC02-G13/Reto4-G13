"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de los mismos.
"""


# Construccion de modelos

def newAnalyzer():
    """
    Inicializa el analizador de vuelos.

    Se crean tres grafos:
      - Un digrafo con todos los aeropuertos y rutas de vuelo.
      - Un grafo no dirigido con aquellos que comparten una ruta.
      - Un grafo que relaciona ciudades y aeropuertos.

    Adicionalmente se utilizan otras estructuras: Dos tablas de hash
    para guardar la informacion relevante de cada ciudad y aeropuerto.
    """
    analyzer = {"diGraph": None,
                "bothWayGraph": None,
                "citiesGraph": None,
                "airports": None,
                "cities": None}

    analyzer["diGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=4000,
                                      comparefunction=compareAirportsIds)

    analyzer["bothWayGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                           directed=False,
                                           size=3500,
                                           comparefunction=compareAirportsIds)

    analyzer["citiesGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=True,
                                          size=10000,
                                          comparefunction=compareCitiesIds)

    analyzer["airports"] = mp.newMap(10710,
                                     maptype="PROBING",
                                     loadfactor=0.5,
                                     comparefunction=compareAirports)

    analyzer["cities"] = mp.newMap(41010,
                                   maptype="PROBING",
                                   loadfactor=0.5,
                                   comparefunction=compareCities)

    return analyzer


# Funciones para agregar informacion al analizador

def addAirport(analyzer, airport):
    """
    Revisa si existe o no el aeropuerto en el mapa. En base a esto, lo
    añade o no a la Tabla de Hash.
    """
    iata = airport["IATA"]
    entry = mp.get(analyzer["airports"], iata)
    if entry is None:
        mp.put(analyzer["airports"], iata, airport)
    else:
        pass


def addCity(analyzer, city):
    """
    Revisa si existe o no la ciudad en el mapa. En base a esto, la
    añade o no a la Tabla de Hash.
    """
    nameCity = city["city"]
    entry = mp.get(analyzer["cities"], nameCity)
    if entry is None:
        mp.put(analyzer["cities"], nameCity, city)
    else:
        pass


def addOneWayRoute(analyzer, route):
    """
    Adiciona al grafo "diGraph" los aeropuertos como vertices y las rutas entre
    aeropuertos adyacentes como arcos.
    """
    departure = route["Departure"]
    destination = route["Destination"]
    distance = route["distance_km"]
    diGraph = analyzer["diGraph"]
    addVertex(diGraph, departure)
    addVertex(diGraph, destination)
    addRoute(diGraph, departure, destination, distance)


def addBothWayRoute(analyzer, route):
    """
    Adiciona al grafo "bothWayGraph" unicamente los aeropuertos y rutas que
    tienen una conexion tanto de ida como de vuelta.
    """
    departure = route["Departure"]
    destination = route["Destination"]
    distance = route["distance_km"]
    diGraph = analyzer["diGraph"]
    bothWayGraph = analyzer["bothWayGraph"]
    edge1 = gr.getEdge(diGraph, departure, destination)
    edge2 = gr.getEdge(diGraph, destination, departure)
    if edge1 is not None and edge2 is not None:
        addVertex(bothWayGraph, departure)
        addVertex(bothWayGraph, destination)
        addRoute(bothWayGraph, departure, destination, distance)


def addVertex(graph, vertex):
    """
    Adiciona un aeropuerto o ciudad como un vertice del grafo.
    """
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)


def addRoute(graph, departure, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos o aeropuerto-ciudad.
    """
    edge = gr.getEdge(graph, departure, destination)
    if edge is None:
        gr.addEdge(graph, departure, destination, distance)


# Funciones para creacion de datos

# Funciones de consulta

def totalVertices(graph):
    """
    Obtiene el total de vertices de un grafo.
    """
    return gr.numVertices(graph)


def totalRoutes(graph):
    """
    Obtiene el total de arcos de un grafo.
    """
    return gr.numEdges(graph)


def totalCities(citiesIndex):
    """
    Obtiene el total de ciudades de la Tabla de Hash.
    """
    return mp.size(citiesIndex)


# Funciones de ordenamiento

# Funciones de comparacion

def compareAirportsIds(airport, keyairpot):
    """
    Compara dos aeropuertos.
    """
    airportcode = keyairpot['key']
    if (airport == airportcode):
        return 0
    elif (airport > airportcode):
        return 1
    else:
        return -1


def compareCitiesIds(cities, keycity):
    """
    Compara dos ciudades.
    """
    citycode = keycity['key']
    if (cities == citycode):
        return 0
    elif (cities > citycode):
        return 1
    else:
        return -1


def compareAirports(keyname, airport):
    """
    Compara dos aeropuertos. El primero es una cadena de caracteres
    y el segundo un entry de un map.
    """
    apEntry = me.getKey(airport)
    if (keyname == apEntry):
        return 0
    elif (keyname > apEntry):
        return 1
    else:
        return -1


def compareCities(keyname, city):
    """
    Compara dos ciudades. La primera es una cadena de caracteres
    y el segundo un entry de un map.
    """
    cityEntry = me.getKey(city)
    if (keyname == cityEntry):
        return 0
    elif (keyname > cityEntry):
        return 1
    else:
        return -1
