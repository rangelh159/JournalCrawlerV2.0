# 📚 Catálogo de Revistas Académicas SCImago

Este proyecto permite automatizar la recopilación, organización y visualización de información sobre revistas académicas indexadas en SCImago. El sistema consta de tres partes: procesamiento de archivos CSV, extracción de datos desde SCImago mediante web scraping y una interfaz gráfica que permite explorar la información por diferentes criterios.

---

## 🔧 Instrucciones para ejecutar el programa

### 1. Preprocesamiento de datos

El archivo ***csv_to_json.py*** sirve para organizar información de revistas contenida en archivos CSV y guardarla en un solo archivo JSON. Utiliza dos carpetas: una con archivos que indican a qué áreas pertenece cada revista, y otra con archivos que muestran en qué catálogos está incluida. A partir de esta información, el archivo agrupa las revistas y registra sus áreas y catálogos, guardando todo en un formato más fácil de manejar y consultar.

**Para generar un archivo JSON:**
1. Abre una terminal y navega hasta la carpeta *funciones* donde se encuentra *csv_to_json.py*
2. Ejecuta el archivo con Python: python *csv_to_json.py*

O bien, pruebe corriendo el archivo *csv_to_json.py* ubicado en la carpeta *funciones*.

Al finalizar, se generará un archivo llamado revistas.json en la ruta: ../datos/json/revistas.json

### 2. Web Scraping de SCImago

El archivo ***scrapper.py*** se encarga de buscar información detallada sobre cada revista en el sitio web *scimagojr.com*, usando el archivo *revistas.json* generado en el paso anterior. Para cada revista, extrae datos como el H-index, sitio web, ISSN, widget, área temática de cada revista, entre otros.

Este proceso automatizado permite actualizar la información sin necesidad de hacerlo manualmente, y guarda los resultados en un nuevo archivo JSON más completo.

**Para ejecutar el scraper:**
1. Abre una terminal y ubícate en la carpeta donde está *scrapper.py*
2. Ejecuta: python scrapper.py -a "ruta_al_archivo_revistas.json" -p (primer titulo en número) -u (último titulo en número) -o "ruta_al_archivo_de_salida.json"
       Significado de los parámetros:
        -a: Archivo de entrada → Ruta al archivo *revistas.json* que contiene la información base sobre las revistas (generado por el csv_to_json.py).
        -p: Primer archivo → Índice (entero) desde donde comenzar el scraping. Por ejemplo, -p 0 inicia desde el principio.
        -u: Último archivo → Índice (entero) desde donde terminar el scraping.
        -o: Archivo de salida → Ruta donde se guardará el nuevo archivo JSON con la información obtenida desde SCImago, ejemplo para este caso: salida.json.
4. Se generará un archivo llamado "salida.json" en la ruta especificada, listo para ser usado por la página web.

Nota: Es necesario tener buena conexión a internet.

### 3. Interfaz gráfica

La parte visual del sistema está desarrollada con Flask y Bootstrap. Esta interfaz permite navegar fácilmente por la información de las revistas ya procesadas. Se pueden explorar revistas por:
1. catálogo,
2. área temática,
3. nombre.

**Para ejecutar la app:**
1. Abre una terminal en la carpeta principal del proyecto
2. Ejecuta: python app.py
3. Abre un navegador y ve a [http://localhost:5000].

Dentro de la interfaz navegue por las funcionalidades de la barra de navegación.

## 👩‍💻 Colaboradoras

* MEREDES MARIANA PERALTA HURTADO
* HILARY DEL CARMEN RANGEL ZAMBRANO
* SOFIA PAOLA SHOUP MORALES

---

## 💡 Nota sobre el uso de inteligencia artificial

Durante el desarrollo del presente proyecto, se utilizó el apoyo de un asistente virtual basado en inteligencia artificial (ChatGPT de OpenAI) para generar sugerencias de nombres, redactar textos explicativos, aclarar dudas sobre la estructura del programa y  optimizar fragmentos de código (también Copilot para estos dos últimos).
