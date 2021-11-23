﻿"""
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
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de los mismos.
"""


# Construccion de modelos

def newAnalyzer():
    """
    Inicializa el analizador de vuelos. Se crean tres grafos:
      - Un digrafo con todos los aeropuertos y rutas de vuelo.
      - Un grafo no dirigido con aquellos que comparten una ruta.
      - Un grafo que relaciona ciudades y aeropuertos.
    """
    analyzer = {"diGraph": None,
                "bothWayGraph": None,
                "citiesGraph": None}

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

    return analyzer


# Funciones para agregar informacion al analizador

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


def addVertex(graph, airport):
    """
    Adiciona un aeropuerto o ciudad como un vertice del grafo.
    """
    if not gr.containsVertex(graph, airport):
        gr.insertVertex(graph, airport)


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
    Obtiene el total de vertices de un grafo
    """
    return gr.numVertices(graph)


def totalRoutes(graph):
    """
    Obtiene el total de arcos de un grafo
    """
    return gr.numEdges(graph)


# Funciones de ordenamiento

# Funciones de comparacion

def compareAirportsIds(airport, keyairpot):
    """
    Compara dos aeropuertos
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
    Compara dos ciudades
    """
    citycode = keycity['key']
    if (cities == citycode):
        return 0
    elif (cities > citycode):
        return 1
    else:
        return -1
