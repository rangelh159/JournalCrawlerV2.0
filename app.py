from flask import Flask, request, url_for, render_template, redirect, flash, session
import os
import random
#from journal_classes import Revista

app = Flask(__name__)
@app.route('/') #decorador que indica que esta función se ejecuta cuando se accede a la ruta raíz de la aplicación. Esto significa que cuando el usuario accede a la URL base de la aplicación, se ejecuta esta función.
def index():
    '''Páfona principal de la aplicación'''
    return render_template('index.html') ##render_template es una función de Flask que se utiliza para renderizar una plantilla HTML y devolverla al navegador. Esta función toma como argumento el nombre de la plantilla HTML que se va a renderizar y los datos que se van a pasar a la plantilla. En este caso, se está renderizando la plantilla index.html y no se están pasando datos a la plantilla.

@app.route('/buscar', methods=['GET'])
def buscar():
    # Lógica para procesar la búsqueda
    query = request.args.get('q')  # 'q' es el nombre del campo de búsqueda
    # Buscar revistas que coincidan con `query`
    return render_template('resultados.html', resultados=resultados)

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

if __name__ == '__main__':
    app.run(debug= True)