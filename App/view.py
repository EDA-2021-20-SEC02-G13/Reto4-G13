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


def printInterconnections(interconnections):
    """
    Imprime los datos requeridos para el requerimiento 1.
    """
    tbCon = PrettyTable(["Name", "City", "Country", "IATA", "connections",
                         "inbound", "outbound"])
    total = lt.size(interconnections)
    if total != 0:
        u = 1
        for pos in range(1, 6):
            ap = lt.getElement(interconnections, pos)
            tbCon.add_row([ap["Name"], ap["City"], ap["Country"], ap["IATA"],
                          ap["connections"], ap["inbound"], ap["outbound"]])
            u += 1
            if u > total:
                break
    tbCon.max_width = 40
    tbCon.hrules = ALL
    print("\n" + "-"*23 + " Req 1. Answer " + "-"*24)
    print("Connected airports inside network:", str(total))
    print("TOP 5 most connected airports...")
    print(tbCon)


def printSCC(analyzer, aeropuerto1, aeropuerto2, conectados, relacion):
    """
    Imprime los datos requeridos para el requerimiento 2.
    """
    a1 = controller.getAirportInfo(analyzer, aeropuerto1)
    a2 = controller.getAirportInfo(analyzer, aeropuerto2)
    tbA1 = PrettyTable(["IATA", "Name", "City", "Country"])
    tbA1.add_row([a1["IATA"], a1["Name"], a1["City"], a1["Country"]])
    tbA1.max_width = 40
    tbA1.hrules = ALL
    tbA2 = PrettyTable(["IATA", "Name", "City", "Country"])
    tbA2.add_row([a2["IATA"], a2["Name"], a2["City"], a2["Country"]])
    tbA2.max_width = 40
    tbA2.hrules = ALL
    print("\n" + "-"*23 + " Req 2. Answer " + "-"*24)
    print("+++ Airport1 IATA Code:", str(aeropuerto1), "+++")
    print(tbA1)
    print("+++ Airport2 IATA Code:", str(aeropuerto2), "+++")
    print(tbA2)
    print("")
    print("- Number of SCC in Airport-Route Network:", str(conectados))
    print("- Does the", a1["Name"], "and the", a2["Name"], "belong together?")
    print("- ANS:", str(relacion))


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


def printTraveler(aeropuertos, total, total_ruta, ltAu, millas_falta, iata,
                  m_km):
    """
    Imprime los datos requeridos para el requerimiento 4.
    """
    p1 = controller.getAirportInfo(analyzer, iata)
    tbp1 = PrettyTable(["IATA", "Name", "City", "Country"])
    tbp1.add_row([p1["IATA"], p1["Name"], p1["City"], p1["Country"]])
    tbp1.max_width = 40
    tbp1.hrules = ALL
    tbPath = PrettyTable(["Departure", "Destination", "distance_km"])
    nodo1 = lt.getElement(ltAu, 1)
    verticeA = nodo1["vertexA"]
    if verticeA == iata:
        for nodo in lt.iterator(ltAu):
            tbPath.add_row([nodo["vertexA"], nodo["vertexB"], nodo["weight"]])
    else:
        for nodo in lt.iterator(ltAu):
            tbPath.add_row([nodo["vertexB"], nodo["vertexA"], nodo["weight"]])
    tbPath.max_width = 40
    tbPath.hrules = ALL
    print("\n" + "-"*23 + " Req 4. Answer " + "-"*24)
    print("+++ Departure airport for IATA code:", str(iata), "+++")
    print(tbp1)
    print("")
    print("- Number of possible airports:", str(aeropuertos))
    print("- Traveling distance sum between airports:", str(total), "(km).")
    print("- Passenger available travelling miles:", str(m_km), "(km).")
    print("")
    print("+++ Longest possible route with airport", str(iata), "+++")
    print("- Longest possible path distance:", str(total_ruta), "(km).")
    print("- Longest possible path details:")
    print(tbPath)
    print("---")
    if millas_falta >= 0:
        print("The passanger needs", str(millas_falta), "miles to complete",
              "the trip.")
    else:
        print("The passanger has", str(abs(millas_falta)), "left to use.")
    print("---")


def printAffectedAirports(airportsTpl, edgesTpl, adjacents2, iata, analyzer):
    """
    Imprime los datos requeridos para el requerimiento 5.
    """
    air1Before, air1After, air2Before, air2After = airportsTpl
    edge1Before, edge1After, edge2Before, edge2After = edgesTpl
    tbAir = PrettyTable(["IATA", "Name", "City", "Country"])
    total = lt.size(adjacents2)
    if total != 0:
        u = 1
        for pos in range(1, 4):
            airport = lt.getElement(adjacents2, pos)
            ap = controller.getAirportInfo(analyzer, airport)
            tbAir.add_row([ap["IATA"], ap["Name"], ap["City"], ap["Country"]])
            u += 1
            if u > total:
                break
    if total == 4:
        airport = lt.getElement(adjacents2, total)
        ap = controller.getAirportInfo(analyzer, airport)
        tbAir.add_row([ap["IATA"], ap["Name"], ap["City"], ap["Country"]])
    elif total == 5:
        for pos in range(total-1, total+1):
            airport = lt.getElement(adjacents2, pos)
            ap = controller.getAirportInfo(analyzer, airport)
            tbAir.add_row([ap["IATA"], ap["Name"], ap["City"], ap["Country"]])
    elif total > 5:
        for pos in range(total-2, total+1):
            airport = lt.getElement(adjacents2, pos)
            ap = controller.getAirportInfo(analyzer, airport)
            tbAir.add_row([ap["IATA"], ap["Name"], ap["City"], ap["Country"]])
    tbAir.max_width = 40
    tbAir.hrules = ALL
    print("\n" + "-"*23 + " Req 5. Answer " + "-"*24)
    print("Closing the airport with IATA code:", str(iata))
    print("")
    print("--- Airports-Routes DiGraph ---")
    print("Original number of Airports:", str(air2Before), "and Routes:",
          str(edge2Before))
    print("--- Airports-Routes bothWayGraph ---")
    print("Original number of Airports:", str(air1Before), "and Routes:",
          str(edge1Before))
    print("")
    print("+++ Removing airport with IATA:", str(iata), "+++")
    print("")
    print("--- Airports-Routes DiGraph ---")
    print("Resulting number of Airports:", str(air2After), "and Routes:",
          str(edge2After))
    print("--- Airports-Routes bothWayGraph ---")
    print("Resulting number of Airports:", str(air1After), "and Routes:",
          str(edge1After))
    print("")
    print("There are", str(lt.size(adjacents2)), "airports affected by",
          "the removal of", str(iata))
    print("The first 3 and last 3 airports affected are:")
    print(tbAir)


def printDijkstraAirport(analyzer, path, airport1, airport2,
                         distance):
    """
    Imprime los datos requeridos para el requerimiento 6.
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
    print("\n" + "-"*23 + " Req 6. Answer " + "-"*24)
    print("+++ The departure airport ", "is +++")
    print(tbAir1)
    print("")
    print("+++ The departure airport ", "is +++")
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
        print("\n" + "-"*23 + " Req 1. Inputs " + "-"*24)
        print("Most connected airports in network (TOP 5)")
        numDiGraph = controller.totalVertices(analyzer["diGraph"])
        print("Number of airports in network:", str(numDiGraph))
        start_time = time.process_time()
        #
        interconnections = controller.interconnection(analyzer)
        #
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time), 2)
        print("Tiempo:", elapsed_time_mseg, "seg")
        printInterconnections(interconnections)

    elif int(inputs[0]) == 2:
        print("\n" + "-"*23 + " Req 2. Inputs " + "-"*24)
        aeropuerto1 = input("Indique el codigo IATA del primer aeropuerto: ")
        aeropuerto2 = input("Indique el codigo IATA del segundo aeropuerto: ")
        start_time = time.process_time()
        #
        scc = controller.findSCC(analyzer, aeropuerto1, aeropuerto2)
        conectados = scc[0]
        relacion = scc[1]
        #
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time), 2)
        print("Tiempo:", elapsed_time_mseg, "seg")
        printSCC(analyzer, aeropuerto1, aeropuerto2, conectados, relacion)

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
        tpl = controller.travelerMST(analyzer, ciudad1M["id"], millas)
        aeropuertos, total, total_ruta, ltAu, millas_falta, iata, m_km = tpl
        #
        stop_time2 = time.process_time()
        elapsed_time_mseg2 = round((stop_time2 - start_time2), 2)
        print("")
        print("Tiempo:", elapsed_time_mseg1 + elapsed_time_mseg2, "seg")
        printTraveler(aeropuertos, total, total_ruta, ltAu, millas_falta, iata,
                      m_km)

    elif int(inputs[0]) == 5:
        print("\n" + "-"*23 + " Req 5. Inputs " + "-"*24)
        iata = str(input("Indique el codigo IATA del aeropuerto a buscar: "))
        start_time = time.process_time()
        #
        tpl = controller.affectedAirports(analyzer, iata)
        airportsTpl = tpl[0]
        edgesTpl = tpl[1]
        adjacents2 = tpl[2]
        #
        stop_time = time.process_time()
        elapsed_time_mseg = round((stop_time - start_time), 2)
        print("Tiempo:", elapsed_time_mseg, "seg")
        printAffectedAirports(airportsTpl, edgesTpl, adjacents2, iata,
                              analyzer)

    elif int(inputs[0]) == 6:
        print("\n" + "-"*23 + " Req 6. Inputs " + "-"*24)
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
        c1cr = ciudad1['lat'], ciudad1['lng']
        c2cr = ciudad2['lat'], ciudad2['lng']
        ap = controller.nearairportapi(c1cr[0], c1cr[1], c2cr[0], c2cr[1])
        tpl = controller.dijkstraAirport(analyzer, ap[0], ap[1], ap[2], ap[3])
        path = tpl[0]
        airport1 = tpl[1]
        airport2 = tpl[2]
        distance = tpl[3]
        #
        stop_time2 = time.process_time()
        elapsed_time_mseg2 = round((stop_time2 - start_time2), 2)
        print("")
        print("Tiempo:", elapsed_time_mseg1 + elapsed_time_mseg2, "seg")
        printDijkstraAirport(analyzer, path, airport1, airport2,
                             distance)

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
