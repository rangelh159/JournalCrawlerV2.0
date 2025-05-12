# archivo donde se definen las clases para el manejo de los datos de las revistas
import os
import hashlib 
import json
#self es una referencia a la instancia actual de la clase.
# __init__ es un método especial en Python que se llama automáticamente cuando se crea una nueva instancia de la clase. Se utiliza para inicializar los atributos de la clase.

class Revista:
    id_counter = 1  # Variable de clase para llevar el conteo de IDs

    def __init__(self, titulo):
        '''Clase para manejar la información de una revista'''
        self.id = Revista.id_counter  # Asigna el ID actual
        Revista.id_counter += 1  # Incrementa el contador para el próximo ID
        self.titulo = titulo
        self.areas = []
        self.catalogos = []
        self.sitio_web = None
        self.h_index = None
        self.subject_area = None
        self.publisher = None
        self.issn = None
        self.widget = None
        self.publication_type = None

    
    def to_dict(self, parte):
        '''Devuelve un diccionario con la información de la revista'''
        # Si parte es 1, devuelve solo áreas y catálogos
        if parte == 1:
            return {
                "id": self.id,
                "areas": self.areas,
                "catalogos": self.catalogos
            }
        # Si parte es 2, devuelve toda la información necesaria para el sitio web
        elif parte == 2:
            return {
                "id": self.id,
                "titulo": self.titulo,
                "areas": self.areas,
                "catalogos": self.catalogos,
                "sitio_web": self.sitio_web,
                "h_index": self.h_index,
                "subject_area": self.subject_area,
                "publisher": self.publisher,
                "issn": self.issn,
                "widget": self.widget,
                "publication_type": self.publication_type
            }
        
    def agregar_area(self, area):
        '''Agrega un área a la lista de áreas si no está ya presente'''
        if area not in self.areas:
            self.areas.append(area)

    def agregar_catalogo(self, catalogo):
        '''Agrega un catálogo a la lista de catálogos si no está ya presente'''
        if catalogo not in self.catalogos:
            self.catalogos.append(catalogo)

class Usuario:
    '''Clase para manejar la información de un usuario del sistema'''
    def __init__(self, username, nombre_completo, email, password):
        self.username = username
        self.nombre_completo = nombre_completo
        self.email = email
        self.password = self.hash_string(password) 
        self.guardadas = []

    def to_dict(self):
        '''Devuelve un diccionario con la información de las relaciones'''
        return {
            'username':self.username,
            'nombre_completo':self.nombre_completo, 
            'email':self.email,
            'password': self.password,
            'guardadas': [revista.titulo for revista in self.guardadas]
        }
    
    def guardar_revista(self, revista):
        '''Guarda la revista en el archivo de usuario'''
        # Verifica si la revista ya está en la lista antes de agregarla
        if revista not in self.guardadas:
            self.guardadas.append(revista)

    def ver_revistas(self):
        '''Devuelve la lista de revistas del usuario'''
        return self.guardadas
    
    def eliminar_guardada(self, revista):
        '''Elimina la revista guardada del archivo de usuario'''
        # Verifica si la revista está en la lista antes de eliminarla
        if revista in self.guardadas:
            self.guardadas.remove(revista)
    
    def hash_string(self, string):
        '''Devuelve el shas de una string'''
        return hashlib.sha256(string.encode()).hexdigest()
    

class SistemaGestor:
    '''Clase para manejar el sistema de gestión de revistas'''
    def __init__(self):
        self.revistas = {}
        self.usuarios = {}
        self.usuario_actual = None
        self.idx_revista = 0

    def leer_json(self, archivo_json):
        '''Carga un archivo JSON y convierte los datos en objetos Revista'''
        if not os.path.exists(archivo_json):
            raise FileNotFoundError(f"El archivo {archivo_json} no existe.")
        
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo) 
            #print(datos)  # Verifica que los datos se carguen correctamente
            for titulo, revista_data in datos.items():
                #print(titulo)   # Itera sobre las claves y valores
                revista = Revista(titulo)  # Usa la clave como título
                revista.id = revista_data.get('id', None)
                revista.areas = revista_data.get('areas', [])
                revista.catalogos = revista_data.get('catalogos', [])
                revista.sitio_web = revista_data.get('sitio_web', None)
                revista.h_index = revista_data.get('h_index', None)
                revista.subject_area = revista_data.get('subject_area', None)
                revista.publisher = revista_data.get('publisher', None)
                revista.issn = revista_data.get('issn', None)
                revista.widget = revista_data.get('widget', None)
                revista.publication_type = revista_data.get('publication_type', None)
                
                self.revistas[revista.id] = revista  # Usa el ID como clave en el diccionario
        self.idx_revista = max(self.revistas.keys()) if self.revistas else 0

    def guardar_json(self, ruta_salida):
        '''Guarda las revistas en un archivo JSON'''
        dict_final = {
            revista.id: revista.to_dict(2)
            for revista in self.revistas.values()
        }
        
        with open(ruta_salida, "w", encoding="utf-8") as f:
            json.dump(dict_final, f, indent=4, ensure_ascii=False)
        print(f"JSON guardado en: {ruta_salida} ({len(dict_final)} revistas)")

    def agregar_revista(self, revista):
        '''Agrega una nueva revista al sistema'''
        self.idx_revista += 1
        revista.id = self.idx_revista
        self.revistas[revista.id] = revista

    def obtener_revistas(self):
        '''Devuelve la lista de revistas en formato de diccionario'''
        return [revista.to_dict(2) for revista in self.revistas.values()]

    def obtener_revista_por_id(self, id_revista):
        '''Devuelve una revista específica por su ID'''
        return self.revistas.get(id_revista)