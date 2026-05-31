import yaml #Libreria PyYAML para convertir entre YAML y diccionarios/objetos Python
from pathlib import Path #Clase pathlib para manejo de rutas de archivos 
from file_manager import FileManager #Clase base que proporciona leer() y escribir() para archivos de texto/binario

class YamlManager(FileManager): #YamlManager es una subclase de FileManager;hereda los metodos publicos leer() y escribir()
    def __init__(self):
        super().__init__() #Llama el constructor de la clase padre
        self.__almacen = {}   #Diccionario privado con la estructura pedida
    
    def cargar(self, nombre: str, ruta: str) -> None: #Metodo "cargar", lee un archivo YAML del disco,lo convierte en un diccionario de Python y lo almacena internamente
        #"nombre:str"; identificador que usara el programador para referirse a este conjunto de datos mas adelante
        #"ruta:str"; ubicación del archivo YAML
        contenido_texto = self.leer(ruta, modo_binario=False) #Lee el contenido textual usando el metodo heredado del FileManager "self.leer".
        datos = yaml.safe_load(contenido_texto) #Conversion de YAML a diccionario
        #yaml.safe_load es una funcion de la libreria PyYAML que analiza y desglosa una cadena con formato YAML y construye objetos Python equivalentes(diccionarios, listas,entre otros)
        if datos is None:
            datos = {}   #Archivo vacio se convierte en diccionario vacio (para evitar problemas en las iteracciones)
        
        
        self.__almacen[nombre] = { #Guarda en el almacen privado
            "path": str(Path(ruta).absolute()),   
            "data": datos
        }
    
    def obtener(self, nombre: str) -> dict: #Metodo "obtener" es un getter publico que permite acceder a los datos internos (ya cargados y desglosados) asociados a un nombre logico
        # "-> dict"; el metodo retorna un diccionario de Python(el contenido del YAML)
        if nombre not in self.__almacen:
            raise KeyError(f"No existe ningún YAML cargado con el nombre '{nombre}'")
        return self.__almacen[nombre]["data"] #Se retorna el diccionario "data";"data" es el diccionario Python que resulto de analizar y deglosar el archivo YAML (o un diccionario vacio si el archivo estaba vacio)
    
    def modificar(self, nombre: str, nuevos_datos: dict) -> None: #Reemplaza los datos del diccionario asociado a "nombre"
        #"nuevos_datos: dict"; el nuevo diccionario Python que reemplazara al antiguo contenido "data"
        if nombre not in self.__almacen: 
            raise KeyError(f"No se puede modificar: el nombre '{nombre}' no existe")
        self.__almacen[nombre]["data"] = nuevos_datos #Reemplazo del diccionario interno. Se accede a la entrada "nombre", cuya entrada es un diccionario con dos claves: "path" y "data"(contenido del archivo YAML);la asignacion ""= nuevos_datos" reemplaza la referencia anterior
    
    def guardar(self, nombre: str) -> None: #Vuelve el diccionario actual (modificado) al archivo YAML original

        if nombre not in self.__almacen:
            raise KeyError(f"No hay datos guardados con el nombre '{nombre}'")
        ruta = self.__almacen[nombre]["path"] #"ruta" es la ruta del archivo YAML, guardada en el momento de la carga
        datos = self.__almacen[nombre]["data"] #"data" es la referencia al diccionario Python que representa el contenido actual
        texto_yaml = yaml.safe_dump(datos, sort_keys=False, allow_unicode=True) #Convertir a texto YAML (sin ordenar llaves para mantener el orden original)
        self.escribir(ruta, texto_yaml, modo_binario=False)  #Escribir usando el metodo heredado
    


