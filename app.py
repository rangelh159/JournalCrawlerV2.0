from flask import Flask, request, url_for, render_template, redirect, flash, session
import os
import random
import funciones.journal_classes as jc

import json

app = Flask(__name__)
sistema = jc.SistemaGestor() #Instancia de la clase Sistema, que es la encargada de gestionar el sistema de revistas científicas. Esta clase se encarga de cargar los datos de las revistas desde un archivo JSON y de gestionar las operaciones relacionadas con las revistas, como la búsqueda y el inicio de sesión.
json_completo= 'datos/json/salida_b.json' #Ruta del archivo JSON que contiene la información de las revistas científicas. Este archivo se encuentra en la carpeta datos/json/revistas.json.
revistas_scrapped = sistema.leer_json(json_completo) #Carga el archivo JSON que contiene la información de las revistas científicas. Este archivo se encuentra en la carpeta datos/json/revistas.json. La función leer_json() es un método de la clase Sistema que se encarga de cargar los datos desde el archivo JSON y almacenarlos en la instancia del sistema.


@app.route('/') #decorador que indica que esta función se ejecuta cuando se accede a la ruta raíz de la aplicación. Esto significa que cuando el usuario accede a la URL base de la aplicación, se ejecuta esta función.
def index():
    '''Páfona principal de la aplicación'''
    return render_template('index.html') ##render_template es una función de Flask que se utiliza para renderizar una plantilla HTML y devolverla al navegador. Esta función toma como argumento el nombre de la plantilla HTML que se va a renderizar y los datos que se van a pasar a la plantilla. En este caso, se está renderizando la plantilla index.html y no se están pasando datos a la plantilla.

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').lower()
    resultados = {}
    if query:
        for titulo, datos in revistas_scrapped.items():
            if query in titulo.lower() or \
               any(query in area.lower() for area in datos['areas']) or \
               any(query in catalogo.lower() for catalogo in datos['catalogos']):
                resultados[titulo] = datos

    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/revista/<int:revista_id>')
def detalle_revista(revista_id):
    '''Muestra los detalles de una revista específica'''
    for titulo, datos in revistas_scrapped.items():
        if datos['id'] == revista_id:
            return render_template('detalle.html', titulo=titulo, revista=datos)
    return "Revista no encontrada", 404

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

if __name__ == '__main__':
    app.run(debug= True)