# archivo donde se definen las clases para el manejo de los datos de las revistas
import os
import hashlib 
#self es una referencia a la instancia actual de la clase.
# __init__ es un método especial en Python que se llama automáticamente cuando se crea una nueva instancia de la clase. Se utiliza para inicializar los atributos de la clase.

class Revista:
    def __init__(self, titulo):
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

    def agregar_area(self, area):
        '''Agrega un área a la revista'''
        # Verifica si el área ya está en la lista antes de agregarla
        if area not in self.areas:
            self.areas.append(area)
    
    def agregar_catalogo(self, catalogo):
        '''Agrega un catálogo a la revista'''
        # Verifica si el catálogo ya está en la lista antes de agregarlo
        if catalogo not in self.catalogos:
            self.catalogos.append(catalogo)
    
    def to_dict(self, parte):
        '''Devuelve un diccionario con la información de la revista'''
        # Si parte es 1, devuelve solo áreas y catálogos
        if parte == 1:
            return {
                "areas": self.areas,
                "catalogos": self.catalogos
            }
        # Si parte es 2, devuelve toda la información necesaria para el sitio web
        elif parte == 2:
            return {
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