"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import time
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

sys.setrecursionlimit(2**20)


# Funciones para la impresión de resultados

def printCargaArchivos(verticesDiGraph, routesDiGraph, verticesbwGraph,
                       routesbwGraph, verticesCityGraph, routesCityGraph,
                       numCities, airportDiGraph, airportbwGraph, lastCity):
    """
    Imprime los datos requeridos para la carga de archivos
    """
    print("-"*62)
    print("Aeropuertos diGraph: " + str(verticesDiGraph))
    print("Rutas aereas diGraph: " + str(routesDiGraph))
    print("1er Aeropuerto: " + str(airportDiGraph)[1:-1])
    print("")
    print("Aeropuertos bothWayGraph: " + str(verticesbwGraph))
    print("Rutas aereas bothWayGraph: " + str(routesbwGraph))
    print("1er Aeropuerto: " + str(airportbwGraph)[1:-1])
    print("")
    print("Aeropuertos y ciudades en citiesGraph: " + str(verticesCityGraph))
    print("Rutas aeropuerto-ciudad en citiesGraph: " + str(routesCityGraph))
    print("")
    print("Total de ciudades: " + str(numCities))
    print("Ultima ciudad: " + str(lastCity)[1:-1])
    print("-"*62)


# Menu de opciones

def printMenu():
    print("\n" + "-"*20 + " Bienvenido al Reto 4 " + "-"*20)
    print("0 - Crear analizador y cargar su información")
    print("1 - Req 1. Encontrar puntos de interconexion aerea")
    print("2 - Req 2. Encontrar clusteres de trafico aereo")
    print("3 - Req 3. Encontrar la ruta mas corta entre ciudades")
    print("4 - Req 4. Utilizar las millas de viajero")
    print("5 - Req 5. Cuantificar el efecto de un aeropuerto cerrado")
    print("6 - Bono1. Comparar con servicio WEB externo")
    print("7 - Bono2. Visualizar graficamente los requerimientos")
    print("8 - Salir de la aplicación")
    print("-"*62)


# Menu principal

analyzer = None
airportsFile = "Skylines/airports_full.csv"
citiesFile = "Skylines/worldcities.csv"
routesFile = "Skylines/routes_full.csv"


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar: ")
    if int(inputs[0]) == 0:
        print("-"*62)
        print("Inicializando, cargando información de los archivos ....")
        start_time = time.process_time()
        #
        analyzer = controller.initAnalyzer()
        controller.loadData(analyzer, airportsFile, citiesFile, routesFile)
        verticesDiGraph = controller.totalVertices(analyzer["diGraph"])
        routesDiGraph = controller.totalRoutes(analyzer["diGraph"])
        airportDiGraph = controller.firstAirport(analyzer["diGraph"],
                                                 analyzer["airports"])
        verticesbwGraph = controller.totalVertices(analyzer["bothWayGraph"])
        routesbwGraph = controller.totalRoutes(analyzer["bothWayGraph"])
        airportbwGraph = controller.firstAirport(analyzer["bothWayGraph"],
                                                 analyzer["airports"])
        verticesCityGraph = controller.totalVertices(analyzer["citiesGraph"])
        routesCityGraph = controller.totalRoutes(analyzer["citiesGraph"])
        numCities = controller.totalCities(analyzer["cities"])
        lastCity = controller.lastCity(analyzer["cities"])
        #
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time), 2)
        print("Tiempo:", elapsed_time_mseg, "seg")
        printCargaArchivos(verticesDiGraph, routesDiGraph, verticesbwGraph,
                           routesbwGraph, verticesCityGraph, routesCityGraph,
                           numCities, airportDiGraph, airportbwGraph, lastCity)

    elif int(inputs[0]) == 1:
        pass

    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
