#Archivo con las funciones necesarias para convertir un archivo CSV a JSON
import csv
import json
import os
from journal_classes import Revista

def leer_csv(directorio_areas, directorio_catalogos) -> dict:
    revistas = {}

    # Leer archivos de áreas
    for archivo in os.listdir(directorio_areas): # Listar archivos en el directorio de áreas
        if archivo.endswith(".csv"): 
            area = archivo.split()[0].upper() #Por cada archivo que termine en .csv, el nombre del archivo es dividido y puesto en una lista de 2 elementos, donde el area es el primer elemento, el cual se toma como valor de la variable área 
            path = os.path.join(directorio_areas, archivo) # Se obtiene la ruta completa del archivo
            with open(path, 'r', encoding='latin1') as f: # Se abre el archivo CSV con encodificación latin1 para evitar problemas con caracteres especiales
                reader = csv.DictReader(f)  # Se abre el archivo CSV y se lee como un diccionario
                for fila in reader:
                    titulo = fila.get("TITULO:") #fila es un diccionario, se obtiene el valor de la clave TITULO:
                    if titulo:
                        titulo = titulo.strip().lower() # Se eliminan espacios en blanco y se convierte a minúsculas
                        if titulo not in revistas: # Si el título no está en el diccionario, se agrega
                            revistas[titulo] = Revista(titulo) # Se crea una nueva instancia de la clase Revista
                        revistas[titulo].agregar_area(area) # Se agrega el área a la revista

    # Leer archivos de catálogos
    for archivo in os.listdir(directorio_catalogos):
        if archivo.endswith(".csv"):
            catalogo = archivo.split("_")[0].upper() #Se divide el nombre del archivo por "_" y se toma el primer elemento como el catálogo
            path = os.path.join(directorio_catalogos, archivo)
            with open(path, 'r', encoding='latin1') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    titulo = fila.get("TITULO:")
                    if titulo:
                        titulo = titulo.strip().lower()
                        if titulo not in revistas:
                            revistas[titulo] = Revista(titulo)
                        revistas[titulo].agregar_catalogo(catalogo)
    return revistas

def guardar_json(diccionario_revistas, ruta_salida):
    # Convierte cada objeto Revs¿ista a un diccionario simple con .to_dict(parte=1)
    dict_final = { titulo: revista.to_dict(parte=1) for titulo, revista in diccionario_revistas.items() }
    
    with open(ruta_salida, "w", encoding='utf-8') as f:
        json.dump(dict_final, f, indent=4, ensure_ascii=False)
    print(f"JSON guardado en: {ruta_salida} ({len(dict_final)} revistas)")

if __name__ == "__main__":
    # Definir los directorios de entrada y salida
    directorio_areas = "../datos/csv/areas"
    directorio_catalogos = "../datos/csv/catalogos"
    ruta_salida = "../datos/json/revistas.json"

    # Leer el CSV y convertirlo a JSON
    revistas = leer_csv(directorio_areas, directorio_catalogos)
    guardar_json(revistas, ruta_salida)