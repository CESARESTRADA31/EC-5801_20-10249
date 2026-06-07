#Cesar Estrada 2010249
import threading
import logging
from typing import Callable, Any, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("ThreadManagerEvent")

class ThreadManagerEvent: #ersión mejorada del gestor de hilos que incluye eventos de terminacion.para cada hilo, permitiendo detenerlos de forma controlada
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self._semaphore = threading.Semaphore(max_concurrent)
        self._threads: Dict[str, dict] = {}
        self._lock = threading.Lock()

    def Thread_Allocate(self, name: str, target: Callable, *args, **kwargs) -> None: #Registra un hilo y crea su evento de terminacion
        with self._lock:
            if name in self._threads:
                raise ValueError(f"Ya existe un hilo con nombre '{name}'")
            stop_event = threading.Event() #Evento de terminacion para este hilo (inicialmente no señalado)
            self._threads[name] = {
                "target": target,
                "args": args,
                "kwargs": kwargs,
                "callbacks": {"start": None, "end": None},
                "thread": None,
                "stop_event": stop_event
            }
            logger.info(f"Hilo '{name}' registrado con evento de terminación")

    def Thread_Callback_Register(self, name: str, callback_start: Optional[Callable] = None, #Asocia callbacks a un hilo registrado
                                 callback_end: Optional[Callable] = None) -> None:
        with self._lock:
            if name not in self._threads:
                raise KeyError(f"Hilo '{name}' no registrado")
            if callback_start:
                self._threads[name]["callbacks"]["start"] = callback_start
            if callback_end:
                self._threads[name]["callbacks"]["end"] = callback_end
            logger.info(f"Callbacks asignados a '{name}'")

    def Thread_Start(self, name: str) -> None: #Inicia el hilo, pasandole su evento de terminacion como argumento adicional
        with self._lock:
            if name not in self._threads:
                raise KeyError(f"Hilo '{name}' no registrado")
            if self._threads[name]["thread"] and self._threads[name]["thread"].is_alive():
                raise RuntimeError(f"Hilo '{name}' ya está ejecutándose")

        def run_wrapper(): #Funcion wrapper que inyecta el evento de terminacion a la funcion objetivo
            try:
                self._semaphore.acquire()
                cb_start = self._threads[name]["callbacks"]["start"]
                if cb_start:
                    cb_start(name)
                logger.info(f"Hilo '{name}' iniciado")

                target = self._threads[name]["target"] #Obtener la funcion objetivo y sus argumentos originales
                args = self._threads[name]["args"]
                kwargs = self._threads[name]["kwargs"]
                stop_event = self._threads[name]["stop_event"]

                #Ejecutar la funcion pasandole el evento de terminacion como primer argumento
                target(stop_event, *args, **kwargs)
            except Exception as e:
                logger.error(f"Excepción en hilo '{name}': {e}")
            finally:
                cb_end = self._threads[name]["callbacks"]["end"]
                if cb_end:
                    cb_end(name)
                logger.info(f"Hilo '{name}' finalizado")
                self._semaphore.release()

        thread = threading.Thread(target=run_wrapper, name=name)
        with self._lock:
            self._threads[name]["thread"] = thread
        thread.start()
        logger.info(f"Hilo '{name}' lanzado (concurrencia actual: {self.max_concurrent - self._semaphore._value})")

    def Thread_End(self, name: str) -> None: #Solicita la terminacion controlada del hilo mediante su evento de terminacion. Luego espera a que el hilo termine (join)
        with self._lock:
            if name not in self._threads:
                raise KeyError(f"Hilo '{name}' no registrado")
            stop_event = self._threads[name]["stop_event"]
            thread = self._threads[name]["thread"]
            if thread is None or not thread.is_alive():
                logger.warning(f"Hilo '{name}' no está activo, no se puede detener")
                return
            #Señalar el evento para que el hilo termine su trabajo
            stop_event.set()
            logger.info(f"Señal de terminación enviada al hilo '{name}'")

        #Esperar a que el hilo finalice (join) para hacer la terminacion sincrona
        thread.join()
        logger.info(f"Hilo '{name}' ha terminado completamente (join realizado)")

#Ejemplo: función que verifica periodicamente el evento de terminacion
def trabajo_largo(stop_event: threading.Event, nombre: str, duracion_max: int): #Funcion que simula un proceso largo. En cada iteracion comprueba si debe detenerse
    #stop_event: Evento que indica si se debe terminar.
    #nombre: Nombre identificador (solo para logs).
    #duracion_max: Número máximo de iteraciones (simula trabajo).
    import time
    i = 0
    while not stop_event.is_set() and i < duracion_max:
        logger.info(f"[{nombre}] Iteración {i+1}/{duracion_max} - trabajando...")
        time.sleep(1)
        i += 1
    if stop_event.is_set():
        logger.info(f"[{nombre}] Detenido prematuramente por evento de terminación")
    else:
        logger.info(f"[{nombre}] Completó su trabajo normalmente")

#Callbacks de ejemplo
def on_start(nombre):
    logger.info(f"[Callback] Hilo '{nombre}' arrancando")

def on_end(nombre):
    logger.info(f"[Callback] Hilo '{nombre}' finalizó")

if __name__ == "__main__":
    #Crear gestor con limite de 2 hilos concurrentes
    manager = ThreadManagerEvent(max_concurrent=2)

    #Registrar hilos
    manager.Thread_Allocate("Worker1", trabajo_largo, "Worker1", 5)  
    manager.Thread_Allocate("Worker2", trabajo_largo, "Worker2", 10)  
    manager.Thread_Allocate("Worker3", trabajo_largo, "Worker3", 8)   

    #Asignar callbacks
    manager.Thread_Callback_Register("Worker1", callback_start=on_start, callback_end=on_end)
    manager.Thread_Callback_Register("Worker2", callback_start=on_start)

    #Iniciar los tres (solo dos se ejecutaran concurrentemente)
    manager.Thread_Start("Worker1")
    manager.Thread_Start("Worker2")
    manager.Thread_Start("Worker3")

    #Esperar un poco y luego detener Worker2 antes de que termine naturalmente
    import time
    time.sleep(2)
    print("\n--- Solicitando terminación de Worker2 ---")
    manager.Thread_End("Worker2")  # Esto detendra Worker2 de forma controlada
