#Archivo con las funciones necesarias para convertir un archivo CSV a JSON
import csv
import json
import os

def leer_csv(directorio_areas, directorio_catalogos) -> dict:
    revistas = {}

    # Leer archivos de áreas
    for archivo in os.listdir(directorio_areas): # Listar archivos en el directorio de áreas
        if archivo.endswith(".csv"): 
            area = archivo.split()[0] #Por cada archivo que termine en .csv, el nombre del archivo es dividido y puesto en una lista de 2 elementos, donde el area es el primer elemento, el cual se toma como valor de la variable área 
            path = os.path.join(directorio_areas, archivo) # Se obtiene la ruta completa del archivo
            with open(path, 'r', encoding='latin1') as f: # Se abre el archivo CSV con encodificación latin1 para evitar problemas con caracteres especiales
                reader = csv.DictReader(f)  # Se abre el archivo CSV y se lee como un diccionario
                for fila in reader:
                    titulo = fila.get("TITULO:") #fila es un diccionario, se obtiene el valor de la clave TITULO:
                    if titulo:
                        titulo = titulo.strip().lower() # Se eliminan espacios en blanco y se convierte a minúsculas
                        if titulo not in revistas: # Si el título no está en el diccionario, se agrega
                            revistas[titulo] = {"areas": [], "catalogos": []}
                        if area not in revistas[titulo]["areas"]: # Si el área no está en la lista de áreas, se agrega
                            revistas[titulo]["areas"].append(area)

    # Leer archivos de catálogos
    for archivo in os.listdir(directorio_catalogos):
        if archivo.endswith(".csv"):
            catalogo = archivo.split("_")[0] #Se divide el nombre del archivo por "_" y se toma el primer elemento como el catálogo
            path = os.path.join(directorio_catalogos, archivo)
            with open(path, 'r', encoding='latin1') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    titulo = fila.get("TITULO:") or fila.get("TITULO")
                    if titulo:
                        titulo = titulo.strip().lower()
                        if titulo not in revistas:
                            revistas[titulo] = {"areas": [], "catalogos": []}
                        if catalogo not in revistas[titulo]["catalogos"]:
                            revistas[titulo]["catalogos"].append(catalogo)
    return revistas