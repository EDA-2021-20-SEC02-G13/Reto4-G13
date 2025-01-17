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

from amadeus import Client, ResponseError
import os
import folium
import config as cf
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from math import radians, cos, sin, asin, sqrt
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

    Adicionalmente se utilizan otras estructuras: Tres tablas de hash
    para guardar la informacion relevante de cada ciudad y aeropuerto.

    Asimismo, se emplea un arbol RBT para la construccion del tercer grafo.
    El arbol, junto a la funcion addCityAirport, se utiliza para encontrar los
    aeropuertos mas cercanos a una ciudad en especificio.
    """
    analyzer = {"diGraph": None,
                "bothWayGraph": None,
                "citiesGraph": None,
                "airports": None,
                "cities": None,
                "repeatedCities": None,
                "rbtAuxiliar": None}

    analyzer["diGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=9100,
                                      comparefunction=compareAirportsIds)

    analyzer["bothWayGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                           directed=False,
                                           size=9100,
                                           comparefunction=compareAirportsIds)

    analyzer["citiesGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=False,
                                          size=41010,
                                          comparefunction=compareCitiesIds)

    analyzer["airports"] = mp.newMap(9100,
                                     maptype="PROBING",
                                     loadfactor=0.5,
                                     comparefunction=compareAirports)

    analyzer["cities"] = mp.newMap(41010,
                                   maptype="PROBING",
                                   loadfactor=0.5,
                                   comparefunction=compareCities)

    analyzer["repeatedCities"] = mp.newMap(38000,
                                           maptype="PROBING",
                                           loadfactor=0.5,
                                           comparefunction=compareCities)

    analyzer["rbtAuxiliar"] = om.newMap(omaptype="RBT",
                                        comparefunction=compareLongitude)

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


def addAirportGraph(analyzer, airport):
    """
    Agrega el aeropuerto a los grafos requeridos.
    """
    diGraph = analyzer["diGraph"]
    bothWayGraph = analyzer["bothWayGraph"]
    iata = airport["IATA"]
    addVertex(diGraph, iata)
    addVertex(bothWayGraph, iata)


def addCity(analyzer, city):
    """
    Revisa si existe o no la ciudad en el mapa. En base a esto, la
    añade o no a la Tabla de Hash.
    """
    idCity = city["id"]
    entry = mp.get(analyzer["cities"], idCity)
    if entry is None:
        mp.put(analyzer["cities"], idCity, city)
    else:
        pass


def addCities(analyzer, city):
    """
    Revisa si existe o no la ciudad en el mapa. En base a esto, la
    añade o no a la Tabla de Hash, y a una lista de ciudades repetidas.
    """
    ciudad = city["city"]
    entry = mp.get(analyzer["repeatedCities"], ciudad)
    if entry is None:
        cityEntry = lt.newList("ARRAY_LIST")
        mp.put(analyzer["repeatedCities"], ciudad, cityEntry)
    else:
        cityEntry = me.getValue(entry)
    lt.addLast(cityEntry, city)


def addOneWayRoute(analyzer, route):
    """
    Adiciona al grafo "diGraph" los aeropuertos como vertices y las rutas entre
    aeropuertos adyacentes como arcos.
    """
    departure = route["Departure"]
    destination = route["Destination"]
    distance = float(route["distance_km"])
    diGraph = analyzer["diGraph"]
    addRoute(diGraph, departure, destination, distance)


def addBothWayRoute(analyzer, route):
    """
    Adiciona al grafo "bothWayGraph" unicamente los aeropuertos y rutas que
    tienen una conexion tanto de ida como de vuelta.
    """
    departure = route["Departure"]
    destination = route["Destination"]
    distance = float(route["distance_km"])
    diGraph = analyzer["diGraph"]
    bothWayGraph = analyzer["bothWayGraph"]
    edge1 = gr.getEdge(diGraph, departure, destination)
    edge2 = gr.getEdge(diGraph, destination, departure)
    if edge1 is not None and edge2 is not None:
        addRoute(bothWayGraph, departure, destination, distance)


def updateLongitudeIndex(analyzer, airport):
    """
    Revisa si existe o no la longitud en el arbol. En base a esto, crea una
    nueva estructura para modelarla, o la adiciona a la lista de aeropuertos.
    """
    longitudeIndex = analyzer["rbtAuxiliar"]
    longitude = round(float(airport["Longitude"]), 2)
    entry = om.get(longitudeIndex, longitude)
    if entry is None:
        latitudentry = newLatitude()
        om.put(longitudeIndex, longitude, latitudentry)
    else:
        latitudentry = me.getValue(entry)
    updateLatitudeIndex(latitudentry["latitudeIndex"], airport)


def updateLatitudeIndex(latitudeIndex, airport):
    """
    Revisa si existe o no la latitud en el arbol. En base a esto, crea una
    nueva estructura para modelarla, o la adiciona a la lista de aeropuertos.
    """
    latitude = round(float(airport["Latitude"]), 2)
    entry = om.get(latitudeIndex, latitude)
    if entry is None:
        latentry = newLatitudelist()
        om.put(latitudeIndex, latitude, latentry)
    else:
        latentry = me.getValue(entry)
    lt.addLast(latentry["ltLatitude"], airport)


def addCityAirport(analyzer, city):
    """
    Genera un arco entre una ciudad y su aeropuerto mas cercano. Para ello,
    calcula la distancia ciudad-aeropuerto de un rango delimitado por un arbol.
    """
    log1 = float(city["lng"])
    lat1 = float(city["lat"])
    log2 = log1 + 0.5
    lat2 = lat1 + 0.5
    mapLongitudes = analyzer["rbtAuxiliar"]
    mapAeropuertos = analyzer["airports"]
    ltTotal = adjAirports(mapLongitudes, log1-0.5, lat1-0.5, log2, lat2)
    minimo = 10000000000
    aeropuertoMin = ""
    for airport in lt.iterator(ltTotal):
        iata = airport["IATA"]
        dicAuxiliar = mp.get(mapAeropuertos, iata)
        dicAirport = dicAuxiliar["value"]
        log2 = float(dicAirport["Longitude"])
        lat2 = float(dicAirport["Latitude"])
        distance = haversine(log1, lat1, log2, lat2)
        if distance < minimo:
            minimo = distance
            aeropuertoMin = iata
    ciudad = city["id"]
    grafoCiudades = analyzer["citiesGraph"]
    addVertex(grafoCiudades, ciudad)
    addVertex(grafoCiudades, aeropuertoMin)
    addRoute(grafoCiudades, ciudad, aeropuertoMin, minimo)


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

def newLatitude():
    """
    Crea una nueva estructura para modelar los aeropuertos de una latitud.
    """
    latitudentry = {"latitudeIndex": None}
    latitudentry["latitudeIndex"] = om.newMap(omaptype="RBT",
                                              comparefunction=compareLatitude)
    return latitudentry


def newLatitudelist():
    """
    Crea una nueva estructura para modelar los aeropuertos de una latitud.
    """
    latentry = {"ltLatitude": None}
    latentry["ltLatitude"] = lt.newList("ARRAY_LIST")
    return latentry


def adjAirports(mapLong, log1, lat1, log2, lat2):
    """
    Retorna los aeropuertos mas cercanos a una ciudad, delimitado por una
    zona geografica. Si no encuentra, vuelve a llamar a la funcion con un
    area de mayor tamaño.
    """
    ltLongitudes = om.values(mapLong, log1, log2)
    ltTotal = lt.newList("ARRAY_LIST")
    for mapLatitudes in lt.iterator(ltLongitudes):
        ltLatitudes = om.values(mapLatitudes["latitudeIndex"], lat1, lat2)
        for latitude in lt.iterator(ltLatitudes):
            for airport in lt.iterator(latitude["ltLatitude"]):
                lt.addLast(ltTotal, airport)
    if lt.size(ltTotal) != 0:
        return ltTotal
    else:
        return adjAirports(mapLong, log1-0.5, lat1-0.5, log2+0.5, lat2+0.5)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia en km entre dos latitudes y longitudes.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


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


def firstAirport(graph, map):
    """
    Obtiene el primer aeropuerto en el grafo.
    """
    vertices = gr.vertices(graph)
    iata = lt.getElement(vertices, 1)
    entry = mp.get(map, iata)
    ap = me.getValue(entry)
    tp = ap["Name"], ap["City"], ap["Country"], ap["Latitude"], ap["Longitude"]
    return tp


def totalCities(citiesIndex):
    """
    Obtiene el total de ciudades de la Tabla de Hash.
    """
    return mp.size(citiesIndex)


def lastCity(map):
    """
    Obtiene la ultima ciudad en el mapa.
    """
    cities = mp.keySet(map)
    idCity = lt.getElement(cities, lt.size(cities))
    entry = mp.get(map, idCity)
    city = me.getValue(entry)
    tp = city["city"], city["population"], city["lat"], city["lng"]
    return tp


def interconnection(analyzer):
    """
    Encuentra los aeropuertos que sirven como punto de interconexion.
    """
    diGraph = analyzer["diGraph"]
    vertices = gr.vertices(diGraph)
    ltAuxiliar = lt.newList("ARRAY_LIST")
    for airport in lt.iterator(vertices):
        outdegree = gr.outdegree(diGraph, airport)
        indegree = gr.indegree(diGraph, airport)
        if outdegree > 0 or indegree > 0:
            connections = outdegree + indegree
            airInfo = getAirportInfo(analyzer, airport)
            airInfo["connections"] = connections
            airInfo["inbound"] = indegree
            airInfo["outbound"] = outdegree
            lt.addLast(ltAuxiliar, airInfo)
    
    return sortAirports(ltAuxiliar, lt.size(ltAuxiliar))


def findSCC(analyzer, aeropuerto1, aeropuerto2):
    """
    Encuentra los componentes fuertemente conectados de un grafo.
    """
    scccluster = scc.KosarajuSCC(analyzer["diGraph"])
    relacion = scc.stronglyConnected(scccluster, aeropuerto1, aeropuerto2)
    conectados = scccluster['components']   
    return conectados, relacion


def homonymous(repeatedCities, city):
    """
    Retorna una lista de ciudades con el mismo nombre.
    """
    entry = mp.get(repeatedCities, city)
    ciudades = me.getValue(entry)
    return ciudades


def dijkstraCity(analyzer, ciudad1, ciudad2):
    """
    Encuentra la ruta minima en distancia para viajar entre dos ciudades, por
    medio del algoritmo de Dijkstra.
    """
    citiesGraph = analyzer["citiesGraph"]
    adjacents1 = gr.adjacents(citiesGraph, ciudad1)
    adjacents2 = gr.adjacents(citiesGraph, ciudad2)
    airport1 = lt.getElement(adjacents1, 1)
    airport2 = lt.getElement(adjacents2, 1)
    search = djk.Dijkstra(analyzer["diGraph"], airport1)
    path = djk.pathTo(search, airport2)
    distance = 0
    d1 = gr.getEdge(citiesGraph, ciudad1, airport1)
    d2 = gr.getEdge(citiesGraph, ciudad2, airport2)
    distance += d1["weight"]
    distance += d2["weight"]
    return path, airport1, airport2, distance


def dijkstraAirport(analyzer, airport1, airport2, distance1, distance2):
    """
    Encuentra la ruta minima en distancia para viajar entre dos ciudades, por
    medio del algoritmo de Dijkstra.
    """
    search = djk.Dijkstra(analyzer["diGraph"], airport1)
    path = djk.pathTo(search, airport2)
    distance = 0
    d1 = distance1
    d2 = distance2
    distance += d1
    distance += d2
    return path, airport1, airport2, distance


def getAirportInfo(analyzer, iata):
    """
    Obtiene la informacion del aeropuerto.
    """
    airports = analyzer["airports"]
    entry = mp.get(airports, iata)
    return me.getValue(entry)


def travelerMST(analyzer, ciudad1M, millas):
    """
    Identifica el arbol de expansion minima para poder cubrir la mayor
    cantidad de ciudades posibles en un unico viaje.
    """
    citiesGraph = analyzer["citiesGraph"]
    bothWayGraph = analyzer["bothWayGraph"]
    adjacents = gr.adjacents(citiesGraph, ciudad1M)
    iata = lt.getElement(adjacents, 1)
    search = prim.PrimMST(bothWayGraph)
    total = round(prim.weightMST(bothWayGraph, search), 3)
    recorrido = dfs.DepthFirstSearch(bothWayGraph, iata)
    mayor = 0
    ruta = ""
    for vertex in lt.iterator(mp.keySet(recorrido["visited"])):
        pila = dfs.pathTo(recorrido, vertex)
        size = lt.size(pila)
        if size > mayor:
            mayor = size
            ruta = pila
    mapEdges = search["edgeTo"]
    ltAu = lt.newList("ARRAY_LIST")
    total_ruta = 0
    for airport in lt.iterator(ruta):
        entry = mp.get(mapEdges, airport)
        if entry is not None:
            nodo = me.getValue(entry)
            total_ruta += nodo["weight"]
            lt.addLast(ltAu, nodo)
    m_km = round(float(millas) * 1.6, 3)
    total_ruta = round(total_ruta, 3)
    km_falta = total_ruta - m_km
    millas_falta = round(km_falta/1.6, 3)
    mpAu = mp.newMap(4000,
                     maptype="PROBING",
                     loadfactor=0.5,
                     comparefunction=compareAirports)
    aeropuertos = 0
    for nodo in lt.iterator(search["mst"]):
        vertexA = nodo["vertexA"]
        vertexB = nodo["vertexB"]
        entry1 = mp.get(mpAu, vertexA)
        entry2 = mp.get(mpAu, vertexB)
        if entry1 is None:
            aeropuertos += 1
            mp.put(mpAu, vertexA, vertexA)
        if entry2 is None:
            aeropuertos += 1
            mp.put(mpAu, vertexB, vertexB)
    return aeropuertos, total, total_ruta, ltAu, millas_falta, iata, m_km


def affectedAirports(analyzer, airport):
    """
    Identifica cuales serian los aeropuertos que afectados si uno sale
    del funcionamiento.
    """
    bothWayGraph = analyzer["bothWayGraph"]
    diGraph = analyzer["diGraph"]
    air1Before = totalVertices(bothWayGraph)
    air2Before = totalVertices(diGraph)
    air1After = air1Before - 1
    air2After = air2Before - 1
    edge1Before = totalRoutes(bothWayGraph)
    edge2Before = totalRoutes(diGraph)
    adjacents1 = gr.adjacents(bothWayGraph, airport)
    adjacents2 = gr.adjacents(diGraph, airport)
    edge1After = edge1Before - lt.size(adjacents1)
    edge2After = edge2Before - lt.size(adjacents2)
    airportsTpl = air1Before, air1After, air2Before, air2After
    edgesTpl = edge1Before, edge1After, edge2Before, edge2After
    return airportsTpl, edgesTpl, adjacents2


def nearairportapi(lat1, lng1, lat2, lng2):
    amadeus = Client(
        client_id=os.getenv('AMADEUS_CLIENT_ID'),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )
    '''
    What relevant airports are there around a specific location?
    '''
    l1 = float(lng1)
    la1 = float(lat1)
    l2 = float(lng2)
    la2 = float(lat2)
    response1 = amadeus.reference_data.locations.airports.get(longitude = l1, latitude = la1)
    response2 = amadeus.reference_data.locations.airports.get(longitude = l2, latitude = la2)
    data1 = response1.data
    data2 = response2.data
    distancia1 = data1[0]['distance']
    d1 = float(distancia1['value'])
    distancia2 = data2[0]['distance']
    d2 = float(distancia2['value'])
    airport1 = data1[0]['iataCode']
    airport2 = data2[0]['iataCode']
    return airport1, airport2, d1, d2

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


def compareLongitude(log1, log2):
    """
    Compara dos coordenadas de longitud.
    """
    if (log1 == log2):
        return 0
    elif (log1 > log2):
        return 1
    else:
        return -1


def compareLatitude(lat1, lat2):
    """
    Compara dos coordenadas de latitud.
    """
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
        return 1
    else:
        return -1


def cmpAirportByCon(air1, air2):
    """
    Devuelve verdadero (True) si el numero de conexiones de air1 es mayor
    que el de air2.
    """
    return air1["connections"] > air2["connections"]


# Funciones de ordenamiento

def sortAirports(airports, sizeAirports):
    """
    Ordena los aeropuertos por numero de conexiones.
    """
    sub_list = lt.subList(airports, 1, sizeAirports)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpAirportByCon)
    return sorted_list
