from flask import Flask, request, url_for, render_template, redirect, flash, session
import os
import random
import funciones.journal_classes as jc

import json

app = Flask(__name__)
sistema = jc.SistemaGestor() 
json_completo= 'datos/json/salida_b_actualizado.json' 
revistas_scrapped = sistema.leer_json(json_completo) 


@app.route('/') 
def index():
    '''Páfona principal de la aplicación'''
    return render_template('index.html') 

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').lower()
    resultados = []

    if query:
        for revista_id, revista in sistema.revistas.items():
            if query in revista.titulo.lower() or \
               any(query in area.lower() for area in revista.areas) or \
               any(query in catalogo.lower() for catalogo in revista.catalogos):
                resultados.append(revista.to_dict(2))  # Convierte el objeto a diccionario

    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/revista/<int:revista_id>')
def detalle_revista(revista_id):
    '''Muestra los detalles de una revista específica'''
    revista = sistema.obtener_revista_por_id(revista_id)
    if not revista:
        return "Revista no encontrada", 404
    return render_template('detalle.html', revista=revista.to_dict(2))

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