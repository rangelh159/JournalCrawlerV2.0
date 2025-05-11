#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import time
import random
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrapea información de revistas desde scimagojr.com "
                    "a partir de un JSON de entrada (con títulos, áreas y catálogos) "
                    "y escribe un JSON de salida con toda la metadata extraída."
    )
    parser.add_argument(
        '-a', '--archivo-entrada', required=True,
        help="JSON de entrada generado en la Parte 1 (diccionario título→{areas,catalogos})"
    )
    parser.add_argument(
        '-p', '--primero', type=int, required=True,
        help="Índice (incluyente) del primer registro a procesar"
    )
    parser.add_argument(
        '-u', '--ultimo', type=int, required=True,
        help="Índice (excluyente) del último registro a procesar"
    )
    parser.add_argument(
        '-o', '--archivo-salida', required=True,
        help="JSON de salida donde se guardarán los registros enriquecidos"
    )
    return parser.parse_args()

def load_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_output(data, path):
    # Creamos la carpeta si no existe
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[+] Escritos {len(data)} registros en {path}")

def buscar_detalle(title):
    """
    1) Hace la búsqueda por título y recorre los resultados.
    2) Extrae los campos pedidos de la página de detalle si encuentra una coincidencia exacta
       o si hay un único resultado en la búsqueda.
    """
    base = 'https://www.scimagojr.com/'
    # 1) Página de búsqueda
    qs = urllib.parse.quote_plus(title)
    search_url = f'{base}journalsearch.php?q={qs}'
    r = requests.get(search_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    # Recorrer todos los resultados de la búsqueda
    resultados = soup.find_all('a', href=re.compile(r'tip=sid'))
    if len(resultados) == 1:
        # Si hay un único resultado, asumir que es el correcto
        a = resultados[0]
        detail_url = urllib.parse.urljoin(base, a['href'])
        r2 = requests.get(detail_url, headers=HEADERS, timeout=30)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, 'html.parser')
        return extraer_detalles(s2)

    for a in resultados:
        # Buscar el título dentro del enlace usando la clase "jrnlname"
        jrnlname_span = a.find('span', class_='jrnlname')
        if jrnlname_span:
            print(f"Resultado encontrado: {jrnlname_span.get_text(strip=True)}")
        if not jrnlname_span:
            continue

        resultado_titulo = jrnlname_span.get_text(strip=True).lower()
        if resultado_titulo == title.lower():
            # Si el título coincide, ir a la página de detalle
            detail_url = urllib.parse.urljoin(base, a['href'])
            r2 = requests.get(detail_url, headers=HEADERS, timeout=15)
            r2.raise_for_status()
            s2 = BeautifulSoup(r2.text, 'html.parser')
            return extraer_detalles(s2)

    # Si no se encuentra una coincidencia exacta
    print(f"No se encontró una coincidencia exacta para «{title}»")
    return {
        "sitio_web": None,
        "h_index": None,
        "subject_area": None,
        "publisher": None,
        "issn": None,
        "widget": None,
        "publication_type": None
    }

def extraer_detalles(s2):
    """
    Extrae los detalles de la página de la revista.
    """
     # Subject Area and Category → diccionario jerárquico
    areas = {}
    subject_area_div = s2.find('h2', string=re.compile(r'^Subject Area and Category$', re.I))
    if subject_area_div:
        # Buscar el <p> contenedor que sigue al <h2>
        subject_area_container = subject_area_div.find_next_sibling('p')
        if subject_area_container:
            # Cada UL directo dentro del <p> representa un área principal
            for ul in subject_area_container.find_all('ul', recursive=False):
                # Tomamos el primer <li> de ese UL
                area_li = ul.find('li', recursive=False)
                if not area_li:
                    continue
                # Nombre del área principal
                area_link = area_li.find('a', href=True)
                if not area_link:
                    continue
                area_name = area_link.get_text(strip=True)

                # Recopilar subcategorías (si existen)
                categories = []
                subcategory_ul = area_li.find('ul', class_='treecategory')
                if subcategory_ul:
                    for sub_li in subcategory_ul.find_all('li'):
                        sub_a = sub_li.find('a', href=True)
                        if sub_a:
                            categories.append(sub_a.get_text(strip=True))

                areas[area_name] = categories

    # Publisher
    pub_tag = s2.find('h2', string=re.compile(r'^Publisher$', re.I))
    publisher = pub_tag.find_next_sibling().get_text(strip=True) if pub_tag else None

    # H-Index
    h_index = None
    h2_hindex = s2.find('h2', string=re.compile(r'^H-Index$', re.I))
    if h2_hindex:
        p_hindex = h2_hindex.find_next_sibling('p', class_='hindexnumber')
        if p_hindex:
            h_index = p_hindex.get_text(strip=True)

    # ISSN
    issn_tag = s2.find('h2', string=re.compile(r'^ISSN$', re.I))
    issn = issn_tag.find_next_sibling().get_text(strip=True) if issn_tag else None

    # Publication type
    pt_tag = s2.find('h2', string=re.compile(r'^Publication type$', re.I))
    publication_type = pt_tag.find_next_sibling().get_text(strip=True) if pt_tag else None

    # Sitio web
    info_h2 = s2.find('h2', string=re.compile(r'^Information$', re.I))
    sitio_web = None
    if info_h2:
        info_div = info_h2.find_parent()
        a_home = info_div.find('a', string=re.compile(r'Homepage', re.I))
        if a_home and a_home['href'].startswith('http'):
            sitio_web = a_home['href']

    # Widget
    widget = None
    embed_input = s2.find('input', id='embed_code')
    if embed_input and embed_input.has_attr('value'):
        widget = embed_input['value']

    return {
        "sitio_web": sitio_web,
        "h_index": h_index,
        "subject_area": areas,
        "publisher": publisher,
        "issn": issn,
        "widget": widget,
        "publication_type": publication_type
    }

def main():
    args = parse_args()
    entrada = load_input(args.archivo_entrada)
    títulos = list(entrada.keys())[args.primero:args.ultimo]

    # 1) Cargar datos previos (si existe el archivo de salida)
    if os.path.exists(args.archivo_salida):
        try:
            with open(args.archivo_salida, 'r', encoding='utf-8') as f:
                salida = json.load(f)
            print(f"[i] Cargados {len(salida)} revistas ya procesadas desde {args.archivo_salida}")
        except json.JSONDecodeError:
            print(f"[!] El archivo de salida {args.archivo_salida} está corrupto/vacío. Se inicializará vacío.")
            salida = {}
    else:
        salida = {}

    # 2) Iterar solo los que faltan
    for idx, titulo in enumerate(títulos, start=args.primero):
        if titulo in salida:
            print(f"[{idx}] «{titulo}» ya procesado, saltando.")
            continue

        print(f"[{idx}] Procesando «{titulo}»…", end=' ')
        try:
            detalles = buscar_detalle(titulo)
            salida[titulo] = {
                "id": idx +1,
                "areas": entrada[titulo]["areas"],
                "catalogos": entrada[titulo]["catalogos"],
                **detalles
            }
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")

        # 3) Guardar incrementalmente (opcional, para no perder avances)
        save_output(salida, args.archivo_salida)

        # 4) Esperar para no sobrecargar el servidor
        time.sleep(random.uniform(3.0, 5.0))

    # 5) Guardado final (por si quedó algo sin guardar en el incremental)
    save_output(salida, args.archivo_salida)

if __name__ == "__main__":
    main()
