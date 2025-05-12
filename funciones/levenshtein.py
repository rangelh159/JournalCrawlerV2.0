import Levenshtein

def levenshtein_distance(cadena1, cadena2):
    """
    Calcula la distancia de Levenshtein entre dos cadenas.
    """
    if len(cadena1) < len(cadena2):
        return levenshtein_distance(cadena2, cadena1)

    # Si una de las cadenas está vacía
    if len(cadena2) == 0:
        return len(cadena1)

    # Crear la matriz de distancias
    previous_row = range(len(cadena2) + 1)
    for i, c1 in enumerate(cadena1):
        current_row = [i + 1]
        for j, c2 in enumerate(cadena2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

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