import itertools
import json
from AFND_e import AFND_e

# Generador de IDs de estado únicos
id_gen = (f"s{i}" for i in itertools.count())

#Función para generar nuevos estados
def nuevo_estado():
    return next(id_gen)

# Precondición: los estados de dest y fuente deben tener nombres distintos
def copiar(dest, fuente):
    for estado in fuente.estados:
        dest.agregar_estado(estado)
    for desde in fuente.transiciones:
        for simbolo in fuente.transiciones[desde]:
            for hacia in fuente.transiciones[desde][simbolo]:
                dest.agregar_transicion(desde, simbolo, hacia)

#Función para cargar los afnd-e de los tests
def cargar_afnd_desde_json(ruta):
    with open(ruta, 'r') as archivo:
        data = json.load(archivo)

    afnd = AFND_e()
    afnd.establecer_inicial(data["inicial"])

    for estado_final in data["finales"]:
        afnd.agregar_final(estado_final)

    for desde, trans in data["transiciones"].items():
        for simbolo, destinos in trans.items():
            for hacia in destinos:
                afnd.agregar_transicion(desde, simbolo, hacia)

    return afnd

def afnde_to_json(afnd, ruta):
    if afnd is not None:
        datos = {
            "inicial": afnd.inicial,
            "finales": list(afnd.finales),
            "transiciones": {}
        }

        for desde in afnd.transiciones:
            datos["transiciones"][desde] = {}
            for simbolo in afnd.transiciones[desde]:
                datos["transiciones"][desde][simbolo] = list(afnd.transiciones[desde][simbolo])

        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


