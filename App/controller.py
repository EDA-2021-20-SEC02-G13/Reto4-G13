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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del analizador de vuelos

def initAnalyzer():
    """
    Inicializa el analizador de vuelos del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer, airportsFile, citiesFile, routesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    """
    fileA = cf.data_dir + airportsFile
    input_file_A = csv.DictReader(open(fileA, encoding="utf-8"), delimiter=",")
    for airport in input_file_A:
        model.addAirport(analyzer, airport)
        model.updateLongitudeIndex(analyzer, airport)
        model.addAirportGraph(analyzer, airport)

    fileC = cf.data_dir + citiesFile
    input_file_C = csv.DictReader(open(fileC, encoding="utf-8"), delimiter=",")
    for city in input_file_C:
        model.addCity(analyzer, city)
        model.addCities(analyzer, city)
        model.addCityAirport(analyzer, city)

    fileR = cf.data_dir + routesFile
    input_file_R = csv.DictReader(open(fileR, encoding="utf-8"), delimiter=",")
    for route in input_file_R:
        model.addOneWayRoute(analyzer, route)
        model.addBothWayRoute(analyzer, route)


# Funciones de consulta sobre el catálogo

def totalVertices(graph):
    """
    Obtiene el total de vertices de un grafo.
    """
    return model.totalVertices(graph)


def totalRoutes(graph):
    """
    Obtiene el total de arcos de un grafo.
    """
    return model.totalRoutes(graph)


def firstAirport(graph, map):
    """
    Obtiene el primer aeropuerto en el grafo.
    """
    return model.firstAirport(graph, map)


def totalCities(citiesIndex):
    """
    Obtiene el total de ciudades de la Tabla de Hash.
    """
    return model.totalCities(citiesIndex)


def lastCity(map):
    """
    Obtiene la ultima ciudad en el mapa.
    """
    return model.lastCity(map)


def interconnection(analyzer):
    """
    Encuentra los aeropuertos que sirven como punto de interconexion.
    """
    return model.interconnection(analyzer)


def findSCC(analyzer, aeropuerto1, aeropuerto2):
    """
    Encuentra los componentes fuertemente conectados de un grafo.
    """
    return model.findSCC(analyzer, aeropuerto1, aeropuerto2)


def homonymous(repeatedCities, city):
    """
    Retorna una lista de ciudades con el mismo nombre.
    """
    return model.homonymous(repeatedCities, city)


def dijkstraCity(analyzer, ciudad1, ciudad2):
    """
    Encuentra la ruta minima en distancia para viajar entre dos ciudades, por
    medio del algoritmo de Dijkstra.
    """
    return model.dijkstraCity(analyzer, ciudad1, ciudad2)


def getAirportInfo(analyzer, iata):
    """
    Obtiene la informacion del aeropuerto.
    """
    return model.getAirportInfo(analyzer, iata)


def travelerMST(analyzer, ciudad1M, millas):
    """
    Identifica el arbol de expansion minima para poder cubrir la mayor
    cantidad de ciudades posibles en un unico viaje.
    """
    return model.travelerMST(analyzer, ciudad1M, millas)


def dijkstraAirport(analyzer, airport1, airport2, d1, d2):
    return model.dijkstraAirport(analyzer, airport1, airport2, d1, d2)


def affectedAirports(analyzer, airport):
    """
    Identifica cuales serian los aeropuertos que afectados si uno sale
    del funcionamiento.
    """
    return model.affectedAirports(analyzer, airport)


def nearairportapi(lat1, lng1, lat2, lng2):
    return model.nearairportapi(lat1, lng1, lat2, lng2)
