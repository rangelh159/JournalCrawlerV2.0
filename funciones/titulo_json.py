import json

def agregar_titulo_a_json(json_data):
    """
    Añade el atributo 'titulo' a cada objeto en el JSON,
    utilizando la clave como valor del atributo.
    """
    for titulo, datos in json_data.items():
        # Normalizar el título: eliminar espacios adicionales y capitalizar
        titulo_normalizado = titulo.strip().title()  # Capitaliza cada palabra
        datos["titulo"] = titulo_normalizado  # Añade el título normalizado como atributo
    return json_data


if __name__ == "__main__":
    # Cargar el JSON existente
    nombre_archivo = "salida_b"  # Nombre del archivo JSON a cargar
    with open(f"../datos/json/{nombre_archivo}.json", "r", encoding="utf-8") as archivo_actualizado:
        json_data = json.load(archivo_actualizado)

    # Añadir el atributo 'titulo' a cada entrada
    json_actualizado = agregar_titulo_a_json(json_data)

    # Guardar el JSON actualizado
    with open(f"../datos/json/{nombre_archivo}_actualizado.json", "w", encoding="utf-8") as archivo:
        json.dump(json_actualizado, archivo, indent=4, ensure_ascii=False)

    print(f"JSON actualizado guardado en '../datos/json/{nombre_archivo}_actualizado.json'")