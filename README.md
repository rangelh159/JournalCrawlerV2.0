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

[Insertar aquÍ]

### 3. Interfaz gráfica

[Insertar aquÍ]

## 👩‍💻 Colaboradoras

* MEREDES MARIANA PERALTA HURTADO
* HILARY DEL CARMEN RANGEL ZAMBRANO
* SOFIA PAOLA SHOUP MORALES

---

## 💡 Nota sobre el uso de inteligencia artificial

Durante el desarrollo del presente proyecto, se utilizó el apoyo de un asistente virtual basado en inteligencia artificial (ChatGPT de OpenAI) para generar sugerencias de nombres, optimizar fragmentos de código, redactar textos explicativos y aclarar dudas sobre la estructura del programa. Las decisiones finales de implementación y validación fueron tomadas por las integrantes del equipo.
