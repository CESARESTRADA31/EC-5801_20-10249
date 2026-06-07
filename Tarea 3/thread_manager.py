#Cesar Estrada 2010249
import threading
import logging
from typing import Callable, Any, Dict, Optional

#Configuracion basica de logging para el gestor
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("ThreadManager")

class ThreadManager: #Gestor de hilos con limite de concurrencia, registro de hilos y callbacks
    def __init__(self, max_concurrent: int): #Inicializa el gestor con un numero maximos de hilos concurrentes
        #max_concurrent:Numero maximo de hilos que pueden ejecutarse a la vez
        self.max_concurrent = max_concurrent #Guarda el numero maximo de hilos que pueden ejecutarse simultaneamente
        self._semaphore = threading.Semaphore(max_concurrent)  #"Semaphore":es un mecanismo de sincronizacion que mantiene un contador interno.Control de concurrencia
        self._threads: Dict[str, dict] = {}  #un diccionario donde la clave es el nombre asignado al hilo (por el usuario) y el valor es otro diccionario con la informacion de ese hilo
        self._lock = threading.Lock()        #El diccionario self._threads puede ser accedido y modificado por multiples hilos.Sin un lock, se producirian condiciones de carrera que podrian corromper el diccionario (como en la clase)

    def Thread_Allocate(self, name: str, target: Callable, *args, **kwargs) -> None: #Registra un hilo con un nombre y la funcion a ejecutar
        #name:Identificador unico del hilo.
        #target:Funcion que ejecutara el hilo.
        #args:Argumentos posicionales para target.
        #kwargs:Argumentos nominales para target.
        
        with self._lock: #self._lock es un threading.Lock creado en el constructor;protege el acceso al diccionario self._threads para que no sea modificado por dos hilos a la vez
            if name in self._threads: #Comprueba si ya existe una entrada con el mismo name en el diccionario
                raise ValueError(f"Ya existe un hilo registrado con el nombre '{name}'")
            self._threads[name] = { #Creacion de la entrada en el diccionario
                "target": target,
                "args": args,
                "kwargs": kwargs,
                "callbacks": {"start": None, "end": None},
                "thread": None
            }
            logger.info(f"Hilo '{name}' registrado correctamente") #Emite un mensaje de nivel INFO confirmando que el registro fue exitoso

    def Thread_Callback_Register(self, name: str, callback_start: Optional[Callable] = None, #Asocia funciones callback a un hilo ya registrado(no ejecutado aun)
                                 callback_end: Optional[Callable] = None) -> None:
        #name: Nombre del hilo.
        #callback_start: Función a llamar justo antes de iniciar el hilo.
        #callback_end: Función a llamar justo después de finalizar el hilo.
        with self._lock: #Excluye el acceso concurrente al diccionario self._threads
            if name not in self._threads:
                raise KeyError(f"El hilo '{name}' no está registrado")
            if callback_start: #Asignacion de los callbacks
                self._threads[name]["callbacks"]["start"] = callback_start
            if callback_end:
                self._threads[name]["callbacks"]["end"] = callback_end
            logger.info(f"Callbacks asignados al hilo '{name}'") #Emite un mensaje de nivel INFO confirmando la asignacion

    def Thread_Start(self, name: str) -> None: #Inicia la ejecucion del hilo registrado, respetando el limite de concurrencia
        with self._lock:
            if name not in self._threads:
                raise KeyError(f"El hilo '{name}' no está registrado")
            if self._threads[name]["thread"] is not None and self._threads[name]["thread"].is_alive():
                raise RuntimeError(f"El hilo '{name}' ya está en ejecución")

        # Función que ejecutará el hilo real, gestionando semáforo y callbacks
        def run_wrapper():
            try: #Contiene el codigo principal que debe ejecutarse.Si ocurre cualquier excepcion se pasa al bloque except.
                self._semaphore.acquire()
                cb_start = self._threads[name]["callbacks"]["start"] #Callback de inicio
                if cb_start:
                    cb_start(name)
                logger.info(f"Hilo '{name}' comenzó su ejecución")
                target = self._threads[name]["target"] #Ejecutar la funcion objetivo
                args = self._threads[name]["args"]
                kwargs = self._threads[name]["kwargs"]
                target(*args, **kwargs)
            except Exception as e: #Captura cualquier excepcion derivada de Exception
                logger.error(f"Error en hilo '{name}': {e}")
            finally:
                #Callback de fin
                cb_end = self._threads[name]["callbacks"]["end"]
                if cb_end:
                    cb_end(name)
                logger.info(f"Hilo '{name}' finalizó")
                self._semaphore.release()  #Liberar semaphore para el siguiente hilo

        #Crear y guardar el hilo
        thread = threading.Thread(target=run_wrapper, name=name) #Funcion que ejecutara el hilo cuando se llame a start(). run_wrapper es la funcion interna que definimos antes, la cual contiene el control de semaphore, callbacks y la funcion objetivo del usuario 
        with self._lock:
            self._threads[name]["thread"] = thread
        thread.start()
        logger.info(f"Hilo '{name}' lanzado (activos: {self._semaphore._value})")  #Se muestra el numero actual de permisos disponibles en el semaphore.El semaphore interno de Python (threading.Semaphore) tiene un atributo _value que guarda el contador

#Ejemplo de uso
if __name__ == "__main__":
    def tarea_larga(nombre: str, segundos: int):
        import time
        logger.info(f"[{nombre}] Trabajando por {segundos} segundos...")
        time.sleep(segundos)
        logger.info(f"[{nombre}] Terminó")

    #Callbacks de ejemplo
    def on_start(nombre):
        logger.info(f"[Callback] El hilo '{nombre}' está arrancando")

    def on_end(nombre):
        logger.info(f"[Callback] El hilo '{nombre}' terminó su labor")


    #Crear gestor con maximo 2 hilos concurrentes
    manager = ThreadManager(max_concurrent=2)

    #Registrar hilos
    manager.Thread_Allocate("A", tarea_larga, "A", 3)
    manager.Thread_Allocate("B", tarea_larga, "B", 2)
    manager.Thread_Allocate("C", tarea_larga, "C", 1)

    #Asignar callbacks
    manager.Thread_Callback_Register("A", callback_start=on_start, callback_end=on_end)
    manager.Thread_Callback_Register("B", callback_start=on_start)

    #Iniciar hilos (el tercero esperará hasta que termine alguno de los primeros dos)
    manager.Thread_Start("A")
    manager.Thread_Start("B")
    manager.Thread_Start("C")