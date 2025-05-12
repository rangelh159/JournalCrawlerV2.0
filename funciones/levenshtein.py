import Levenshtein

def distancia_levenshtein(cadena1, cadena2):
    """
    Calcula la distancia de Levenshtein entre dos cadenas.
    """
    if len(cadena1) < len(cadena2):
        return distancia_levenshtein(cadena2, cadena1)

    # Si una de las cadenas está vacía
    if len(cadena2) == 0:
        return len(cadena1)

    # Crear la matriz de distancias
    fila_anterior = range(len(cadena2) + 1)
    for i, c1 in enumerate(cadena1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(cadena2):
            inserciones = fila_anterior[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_anterior[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_anterior = fila_actual

    return fila_anterior[-1]

def es_similar_levenshtein(titulo1, titulo2, umbral=0.8):
    """
    Compara dos títulos usando la distancia de Levenshtein.
    Devuelve True si la similitud es mayor o igual al umbral.
    """
    distancia = Levenshtein.distance(titulo1, titulo2)
    longitud_maxima = max(len(titulo1), len(titulo2))
    similitud = 1 - (distancia / longitud_maxima)
    return similitud >= umbral

if __name__ == "__main__":
    print(levenshtein_distance("journal", "r journal"))  # Debería devolver un valor pequeño
    print(levenshtein_distance("journal", "journal of science"))  # Debería devolver un valor pequeño
    print(levenshtein_distance("journal", "random text"))  # Debería devolver un valor grande