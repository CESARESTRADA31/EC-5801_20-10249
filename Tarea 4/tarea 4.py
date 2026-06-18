#Cesar Estrada 2010249
import logging
import threading
from queue import Queue
from typing import Any, Callable, Dict, Optional

#Configuracion basica del logging
logging.basicConfig( #"basicConfig()"": funcion del modulo logging que establece la configuracion global para el sistema de logging
    level=logging.INFO, #Define el umbral minimo de severidad para que un mensaje sea procesado.Con INFO, se mostraran mensajes de nivel INFO,WARNING,ERROR y CRITICAL
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s' #Especifica la estructura de cada linea de log = Fecha y hora (por defecto formato americano), nivel de severidad, nombre del logger (MassagesManager) y mensaje enviado por el usuario
)
logger = logging.getLogger("MessagesManager") #"logging.getLogger(name)" obtiene (o crea si no existe) un objeto Logger con el nombre "MessagesManager"


class Messages_Manager: #Gestor de colas para comunicacion entre hilos. Crea y elimina colas y envia/recibe mensajes, realizando pollings automaticos
    def __init__(self): #Metodo _init_ constructor de la clase
        self._queues: Dict[str, Queue] = {} #Almacena todas las colas creadas e indexadas por su nombre."Dict[str, Queue]":diccionario cuyas claves son str (el nombre de la cola) y cuyos valores son objetos Queue
        self._callbacks: Dict[str, Callable] = {} #Almacena las funciones callback asociadas a cada cola, tambien indexadas por nombre.Usa diccionario cuya claves son str (nombre de la cola) y valores Callable (una funcion que se ejecutara al recibir un mensaje)
        self._lock = threading.Lock() #Crear un objeto Lock para garantizar mutex en el acceso a los diccionarios

    #Gestion de colas
    def create(self, name: str, maxsize: int = 0, callback: Optional[Callable] = None) -> None: #Metodo create encargado de crear una nueva cola en el gestor,asociarla a un nombre unico y asignarle una funcion callback que se ejecutara automaticamente al recibir mensajes
        with self._lock: #Evita la condicion de carrera, protegiendo el acceso a los diccionarios _queues y _callbacks; adquiere el lock al entrar al bloque y lo libera al salir
            if name in self._queues: #Comprueba si el nombre ya existe en el diccionario de colas
                raise ValueError(f"Ya existe una cola con el nombre '{name}'")
            self._queues[name] = Queue(maxsize=maxsize) #Se crea una instancia de queue.Queue con el tamaño maximo especificado.
            if callback is not None: #Si se proporciona un callback (no es None),se guarda en el diccionario _callbacks con la misma clave name
                self._callbacks[name] = callback 
            logger.info(f"Cola '{name}' creada (maxsize={maxsize}, callback={'asignado' if callback else 'ninguno'})") #Emite un mensaje de nivel INFO indicando que la cola fue creada.Muestra el tamaño maximo y si se asigno o no un callback

    def delete(self, name: str) -> None: #Metodo publico que recibe el nombre de la cola a eliminar y no retorna valor
        with self._lock:
            if name not in self._queues: #Comprueba si el nombre existe en el diccionario de colas
                raise KeyError(f"No existe la cola '{name}'")
            del self._queues[name] #Elimina la entrada del diccionario _queues con la clave name.A partir de este momento,cualquier intento de usar la cola fallara porque name ya no estara en _queues
            if name in self._callbacks: #Verifica si existe un callback asociado a esta cola; si existe, lo elimina
                del self._callbacks[name]
            logger.info(f"Cola '{name}' eliminada correctamente")

    #Intercambio de mensajes
    def send(self, name: str, message: Any, timeout: Optional[float] = None) -> None: #El metodo send es el encargado de depositar un mensaje en una cola especifica
        with self._lock: #"with self._lock": adquiere el lock al entrar y lo libera al salir
            if name not in self._queues:
                raise KeyError(f"No existe la cola '{name}'")
            q = self._queues[name] #Obtiene una referencia local al objeto Queue asociado al nombre proporcionado, para luego poder operar con el
        try:
            q.put(message, block=True, timeout=timeout) #"block=True":la operacion es bloqueante.Si la cola esta llena, el hilo se detiene hasta que haya espacio disponible (o hasta que se cumpla el timeout).
            logger.info(f"Mensaje enviado a cola '{name}': {message}")
        except Exception as e:
            logger.error(f"Error al enviar mensaje a '{name}': {e}")
            raise #Si ocurre cualquier excepcion (ejmplo: queue.Full por timeout),se registra como ERROR y luego se relanza (raise) para que el llamador pueda manejarla

    def receive(self, name: str) -> Optional[Any]: #El metodo receive se encarga de extraer un mensaje de una cola especifica de forma no bloqueante
        with self._lock: #Adquiere el lock al entrar al bloque y lo libera al salir
            if name not in self._queues:
                raise KeyError(f"No existe la cola '{name}'")
            q = self._queues[name]
        try:
            mensaje = q.get_nowait() #"get_nowait()":es un metodo de queue.Queue que intenta extraer un elemento de la cola sin bloquear
            logger.info(f"Mensaje recibido de cola '{name}': {mensaje}")
            return mensaje
        except Exception: #Manejo de cola vacia sin errores
            logger.debug(f"Intento de receive en cola '{name}' vacía")
            return None

    #Polling automatico
    def poll(self) -> None: #Obtiene una lista de todas las colas activas y una copia de los callbacks asociados,todo bajo proteccion de mutex
        with self._lock:
            nombres = list(self._queues.keys())
            callbacks_instantanea = self._callbacks.copy() #Crea una copia superficial del diccionario de callbacks

        for name in nombres: #"nombres":es la lista estatica de nombres de colas que se obtuvo al inicio de poll,capturando el estado en ese momento
            mensaje = self.receive(name) #Recepcion de mensajes no bloqueante 
            if mensaje is not None: #Si mensaje es None,significa que la cola estaba vacia; en ese caso,simplemente se salta al siguiente nombre de la lista
                ci = callbacks_instantanea.get(name) #Obtencion del callback asociado
                if ci is not None: #Solo se ejecuta si existe un callback asociado a la cola
                    try:
                        ci(mensaje) #Invoca la funcion callback pasandole el mensaje extraido como argumento
                        logger.debug(f"Callback ejecutado para cola '{name}'")
                    except Exception as e:
                        logger.error(f"Error en callback de cola '{name}': {e}")
