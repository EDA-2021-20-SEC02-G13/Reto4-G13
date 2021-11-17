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
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*10)


def printMenu():
    print("\n" + "-"*20 + " Bienvenido al Reto 4 " + "-"*20)
    print("0 - Crear catalogo y cargar su información")
    print("1 - Req 1. Encontrar puntos de interconexion aerea")
    print("2 - Req 2. Encontrar clusteres de trafico aereo")
    print("3 - Req 3. Encontrar la ruta mas corta entre ciudades")
    print("4 - Req 4. Utilizar las millas de viajero")
    print("5 - Req 5. Cuantificar el efecto de un aeropuerto cerrado")
    print("6 - Bono1. Comparar con servicio WEB externo")
    print("7 - Bono2. Visualizar graficamente los requerimientos")
    print("8 - Salir de la aplicación")
    print("-"*62)


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")

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
