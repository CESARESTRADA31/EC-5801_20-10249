from pathlib import Path #"pathlib",permite manipular rutas de archivos de forma orientada a objetos
from typing import Union #"typing", se usa para indicar que un parametro puede ser de dos tipos (str o Path).

class FileManager: #Clase base para operaciones de lectura/escritura de archivos
    @classmethod #Descorador
    def leer(cls, ruta: Union[str, Path], modo_binario: bool = False) -> Union[str, bytes]: #Lee el contenido de un archivo.Retorna el contenido como string(texto) o bytes (binario)
        #Modo_binario=False: lectura como texto ('r')
        #Modo_binario=True: lectura como binario ('rb')
        archivo = Path(ruta) #Convierte el argumento ruta (sea str o Path) en un objeto Path de pathlib
        if not archivo.is_file():
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        
        modo = 'rb' if modo_binario else 'r' #Determina el modo de apertura (string "r" o binario "rb")
        with open(archivo, modo) as f: #Garantiza que el archivo se cierre automaticamente al salir del bloque,incluso si ocurre una excepcion
            return f.read() #Inmediatamente despues de leer el archivo, el metodo retorna ese contenido
    
    @classmethod #Decorador
    def escribir(cls, ruta: Union[str, Path], contenido: Union[str, bytes], modo_binario: bool = False) -> None: #Escribe el contenido en un archivo.
        #Modo_binario=False: escritura como texto ("w")
        #Modo_binario=True: escritura como binario ("wb")

        destino = Path(ruta) #Conversion a Path y validacion del directorio padre
        if not destino.parent.exists(): #Verificar que el directorio padre exista
            raise FileNotFoundError(f"El directorio {destino.parent} no existe.")
        
        modo = 'wb' if modo_binario else 'w' #Determinacion del modo de escritura
        with open(destino, modo) as f: #Abre el archivo y garantiza que se cierre automaticamente al salir del bloque, incluso si ocurre una excepcion durante la escritura
            f.write(contenido) #Escribe todo el contenido en el archivo.

