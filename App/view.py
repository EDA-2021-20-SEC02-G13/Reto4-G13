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
from prettytable import PrettyTable, ALL
from DISClib.ADT import stack
from DISClib.ADT import list as lt
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


def printDijkstraCity(analyzer, path, airport1, airport2, city1, city2,
                      distance):
    """
    Imprime los datos requeridos para el requerimiento 3.
    """
    a1 = controller.getAirportInfo(analyzer, airport1)
    a2 = controller.getAirportInfo(analyzer, airport2)
    tbAir1 = PrettyTable(["IATA", "Name", "City", "Country"])
    tbAir1.add_row([a1["IATA"], a1["Name"], a1["City"], a1["Country"]])
    tbAir1.max_width = 40
    tbAir1.hrules = ALL
    tbAir2 = PrettyTable(["IATA", "Name", "City", "Country"])
    tbAir2.add_row([a2["IATA"], a2["Name"], a2["City"], a2["Country"]])
    tbAir2.max_width = 40
    tbAir2.hrules = ALL
    tbDistance = PrettyTable(["Departure", "Destination", "distance_km"])
    tbStops = PrettyTable(["IATA", "Name", "City", "Country"])
    dictAuxiliar = {}
    if path is not None:
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            distance += stop["weight"]
            tbDistance.add_row([stop["vertexA"], stop["vertexB"],
                                stop["weight"]])
            dictAuxiliar[stop["vertexA"]] = 1
            dictAuxiliar[stop["vertexB"]] = 1
    else:
        print('No hay camino')
    for key in dictAuxiliar.keys():
        air1 = controller.getAirportInfo(analyzer, key)
        tbStops.add_row([air1["IATA"], air1["Name"], air1["City"],
                         air1["Country"]])
    tbDistance.max_width = 40
    tbDistance.hrules = ALL
    tbStops.max_width = 40
    tbStops.hrules = ALL
    print("\n" + "-"*23 + " Req 3. Answer " + "-"*24)
    print("+++ The departure airport in", str(city1), "is +++")
    print(tbAir1)
    print("")
    print("+++ The departure airport in", str(city2), "is +++")
    print(tbAir2)
    print("\n" + "+++ Dijkstra's Trip Details +++")
    print("- Total distance:", str(round(distance, 3)), "(km)")
    print("- Trip Path:")
    print(tbDistance)
    print("- Trip Stops:")
    print(tbStops)


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
airportsFile = "Skylines/airports-utf8-small.csv"
citiesFile = "Skylines/worldcities-utf8.csv"
routesFile = "Skylines/routes-utf8-small.csv"


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
        print("\n" + "-"*23 + " Req 2. Inputs " + "-"*24)
        aeropuerto1 = input('Indique el aeropuerto que desea : ')
        aeropuerto2 = input('Indique el aeropuerto que desea : ')
        scc = controller.findSCC(analyzer, aeropuerto1, aeropuerto2)
        print(scc[0], scc[1])

    elif int(inputs[0]) == 3:
        print("\n" + "-"*23 + " Req 3. Inputs " + "-"*24)
        city1 = input("Indique el nombre de la primera ciudad a buscar: ")
        city2 = input("Indique el nombre de la segunda ciudad a buscar: ")
        start_time1 = time.process_time()
        #
        cities = controller.homonymous(analyzer["repeatedCities"], str(city1))
        print("\n" + "Listado de ciudades hononimas de la primera ciudad:")
        tbCity = PrettyTable(["#", "Ciudad", "Pais", "Subregion", "Latitud",
                              "Longitud)", "id"])
        num = 1
        for city in lt.iterator(cities):
            tbCity.add_row([str(num), city["city"], city["country"],
                            city["admin_name"], city["lat"], city["lng"],
                            city["id"]])
            num += 1
        tbCity.max_width = 40
        tbCity.hrules = ALL
        print(tbCity)
        #
        cities2 = controller.homonymous(analyzer["repeatedCities"], str(city2))
        print("\n" + "Listado de ciudades hononimas de la segunda ciudad:")
        tbCity2 = PrettyTable(["#", "Ciudad", "Pais", "Subregion", "Latitud",
                              "Longitud)", "id"])
        num = 1
        for city in lt.iterator(cities2):
            tbCity2.add_row([str(num), city["city"], city["country"],
                            city["admin_name"], city["lat"], city["lng"],
                            city["id"]])
            num += 1
        tbCity2.max_width = 40
        tbCity2.hrules = ALL
        print(tbCity2)
        #
        stop_time1 = time.process_time()
        elapsed_time_mseg1 = round((stop_time1 - start_time1), 2)
        numCiudad1 = input("\n" + "Seleccione de la lista de ciudades, el "
                           "numero de la primera que desea buscar: ")
        numCiudad2 = input("Seleccione de la lista de ciudades, el "
                           "numero de la segunda que desea buscar: ")
        start_time2 = time.process_time()
        #
        ciudad1 = lt.getElement(cities, int(numCiudad1))
        ciudad2 = lt.getElement(cities2, int(numCiudad2))
        tpl = controller.dijkstraCity(analyzer, ciudad1["id"], ciudad2["id"])
        path = tpl[0]
        airport1 = tpl[1]
        airport2 = tpl[2]
        distance = tpl[3]
        #
        stop_time2 = time.process_time()
        elapsed_time_mseg2 = round((stop_time2 - start_time2), 2)
        print("")
        print("Tiempo:", elapsed_time_mseg1 + elapsed_time_mseg2, "seg")
        printDijkstraCity(analyzer, path, airport1, airport2, city1, city2,
                          distance)

    elif int(inputs[0]) == 4:
        print("\n" + "-"*23 + " Req 4. Inputs " + "-"*24)
        millas = input("Indique la cantidad de millas del viajero: ")
        p1 = input("Indique el nombre de la ciudad de partida: ")
        start_time1 = time.process_time()
        #
        citiesM = controller.homonymous(analyzer["repeatedCities"], str(p1))
        print("\n" + "Listado de ciudades hononimas de la primera ciudad:")
        tbCityM = PrettyTable(["#", "Ciudad", "Pais", "Subregion", "Latitud",
                              "Longitud)", "id"])
        num = 1
        for city in lt.iterator(citiesM):
            tbCityM.add_row([str(num), city["city"], city["country"],
                            city["admin_name"], city["lat"], city["lng"],
                            city["id"]])
            num += 1
        tbCityM.max_width = 40
        tbCityM.hrules = ALL
        print(tbCityM)
        #
        stop_time1 = time.process_time()
        elapsed_time_mseg1 = round((stop_time1 - start_time1), 2)
        numCiudad1M = input("\n" + "Seleccione de la lista de ciudades, el "
                            "numero de la que desea partir: ")
        start_time2 = time.process_time()
        #
        ciudad1M = lt.getElement(citiesM, int(numCiudad1M))
        controller.travelerMST(analyzer, ciudad1M["id"], millas)

        #
        stop_time2 = time.process_time()
        elapsed_time_mseg2 = round((stop_time2 - start_time2), 2)
        print("")
        print("Tiempo:", elapsed_time_mseg1 + elapsed_time_mseg2, "seg")

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
