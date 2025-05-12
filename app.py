from flask import Flask, request, url_for, render_template, redirect, flash, session
import os
import random
import funciones.journal_classes as jc
import funciones.levenshtein as lev

# Diccionario para mapear códigos de áreas a nombres legibles
AREA_MAP = {
    "CIENCIAS_BIO": "Ciencias Biológicas",
    "CIENCIAS_ECO": "Ciencias Económicas",
    "CIENCIAS_EXA": "Ciencias Exactas",
    "CIENCIAS_SOC": "Ciencias Sociales",
    "HUMAN_Y_ART": "Humanidades y Arte",
    "ING": "Ingeniería",
    "MULTI": "Multidisciplinario"
}


#Archivo principal de la aplicación Flask
app = Flask(__name__)
sistema = jc.SistemaGestor() #Instancia de la clase Sistema, que es la encargada de gestionar el sistema de revistas científicas. Esta clase se encarga de cargar los datos de las revistas desde un archivo JSON y de gestionar las operaciones relacionadas con las revistas, como la búsqueda y el inicio de sesión.
json_completo= 'datos/json/salida_b_actualizado.json' #Ruta del archivo JSON que contiene la información de las revistas científicas. Este archivo se encuentra en la carpeta datos/json/revistas.json.
revistas_scrapped = sistema.leer_json(json_completo) #Carga el archivo JSON que contiene la información de las revistas científicas. Este archivo se encuentra en la carpeta datos/json/revistas.json. La función leer_json() es un método de la clase Sistema que se encarga de cargar los datos desde el archivo JSON y almacenarlos en la instancia del sistema.


@app.route('/') #decorador que indica que esta función se ejecuta cuando se accede a la ruta raíz de la aplicación. Esto significa que cuando el usuario accede a la URL base de la aplicación, se ejecuta esta función.
def index():
    '''Páfona principal de la aplicación'''
    return render_template('index.html') ##render_template es una función de Flask que se utiliza para renderizar una plantilla HTML y devolverla al navegador. Esta función toma como argumento el nombre de la plantilla HTML que se va a renderizar y los datos que se van a pasar a la plantilla. En este caso, se está renderizando la plantilla index.html y no se están pasando datos a la plantilla.

@app.route('/area')
def area():
    # Obtener el área seleccionada de los parámetros de la URL
    selected_area = request.args.get('area', None)

    # Crear un diccionario con las revistas agrupadas por área
    revistas_por_area = {}
    for revista_id, revista in sistema.revistas.items():
        for area in revista.areas:
            if area not in revistas_por_area:
                revistas_por_area[area] = []
            revistas_por_area[area].append({
                "id": revista.id,
                "titulo": revista.titulo,
                "h_index": revista.h_index
            })

    # Obtener las revistas del área seleccionada
    revistas = revistas_por_area.get(selected_area, []) if selected_area else None

    # Pasar los datos al template
    return render_template(
        'area.html',
        AREA_MAP=AREA_MAP, revistas=revistas, selected_area=selected_area)

@app.route('/catalogos')
def catalogos():
    # Obtener el catálogo seleccionado de los parámetros de la URL
    selected_catalogo = request.args.get('catalogo', None)

    # Crear un diccionario con las revistas agrupadas por catálogo
    revistas_por_catalogo = {}
    for revista_id, revista in sistema.revistas.items():
        for catalogo in revista.catalogos:
            if catalogo not in revistas_por_catalogo:
                revistas_por_catalogo[catalogo] = []
            revistas_por_catalogo[catalogo].append({
                "id": revista.id,
                "titulo": revista.titulo,
                "h_index": revista.h_index
            })

    # Obtener las revistas del catálogo seleccionado
    revistas = revistas_por_catalogo.get(selected_catalogo, []) if selected_catalogo else None

    # Obtener la lista de catálogos disponibles
    catalogos_disponibles = list(revistas_por_catalogo.keys())

    # Pasar los datos al template
    return render_template(
        'catalogos.html',
        catalogos_disponibles=catalogos_disponibles,
        revistas=revistas,
        selected_catalogo=selected_catalogo
    )

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').lower()
    orden = request.args.get('orden', 'desc')  # Por defecto, descendente
    resultados = []

    if query:
        for revista_id, revista in sistema.revistas.items():
            titulo = revista.titulo.lower()

            # Coincidencia exacta de palabras clave
            if query in titulo:
                relevancia = 1  # Máxima relevancia para coincidencia exacta
            # Coincidencia aproximada usando Levenshtein
            elif lev.es_similar_levenshtein(query, titulo, umbral=0.8):
                relevancia = 2  # Relevancia media para coincidencia aproximada
            else:
                continue  # Ignorar resultados irrelevantes

            # Traducir las áreas
            areas_traducidas = [AREA_MAP.get(area, area) for area in revista.areas]

            # Agregar resultado con relevancia
            resultados.append({
                "revista": revista.to_dict(2),
                "relevancia": relevancia,
                "titulo": revista.titulo,
                "areas_traducidas": areas_traducidas
            })

        # Ordenar los resultados por relevancia
        resultados.sort(key=lambda x: x["relevancia"])

        # Ordenar por H-Index según el orden seleccionado
        def parse_h_index(value):
            try:
                return int(value)  # Intenta convertir a entero
            except (ValueError, TypeError):
                return 0  # Si falla, devuelve 0 como valor predeterminado

        if orden == 'asc':
            resultados.sort(key=lambda x: parse_h_index(x["revista"].get("h_index", 0)))
        else:  # Orden descendente por defecto
            resultados.sort(key=lambda x: parse_h_index(x["revista"].get("h_index", 0)), reverse=True)

    return render_template('buscar.html', resultados=resultados, query=query, orden=orden)

@app.route('/revista/<int:revista_id>')
def detalle_revista(revista_id):
    '''Muestra los detalles de una revista específica'''
    revista = sistema.obtener_revista_por_id(revista_id)
    if not revista:
        return "Revista no encontrada", 404
    #verificar si datos scrappeados es none
    campos_scrappeados = ['h_index', 'subject_area', 'sitio_web', 'publisher', 'issn', 'widget', 'publication_type']
    campos_null = [campo for campo in campos_scrappeados if getattr(revista, campo, None) is None] #getattr(revista, campo, None) devuelve el valor del atributo campo de la revista. Si el atributo no existe, devuelve None. Los parametros de getattr son el objeto del que se quiere obtener el atributo, el nombre del atributo y un valor por defecto que se devuelve si el atributo no existe.

    mensaje = None
    if campos_null:
        mensaje = "Algunos datos de esta revista no están disponibles en Scimago."

    areas_traducidas = [AREA_MAP.get(area, area) for area in revista.areas]

    return render_template('detalle.html', revista=revista.to_dict(2), mensaje=mensaje, areas_traducidas=areas_traducidas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        exito = sistema.login(username, password)
        if exito: 
            session['logged_in'] = True
            session['username'] = sistema.usuario_actual.nombre_completo
            return redirect(url_for('index'))
        else: 
            error = 'Usuario o contraseña incorrectos'
            return render_template('login.html')
    return render_template('login.html')

@app.route('/creditos')
def equipo():
    return render_template('creditos.html')

@app.route('/explorar')
def explorar():
    # Obtener la letra seleccionada de los parámetros de la URL
    letra = request.args.get('letra', '').upper()

    # Filtrar las revistas que comienzan con la letra seleccionada
    revistas = []
    if letra:
        for revista_id, revista in sistema.revistas.items():
            if revista.titulo.upper().startswith(letra):
                revistas.append({
                    "id": revista.id,
                    "titulo": revista.titulo,
                    "catalogos": revista.catalogos,
                    "areas": revista.areas,
                    "h_index": revista.h_index
                })

    # Pasar los datos al template
    return render_template('explorar.html', revistas=revistas, letra=letra)

if __name__ == '__main__':
    app.run(debug= True)