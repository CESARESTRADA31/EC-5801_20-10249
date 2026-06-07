#Cesar Estrada 20-10249
import logging

def configurar_logging(): #Configura el sistema de logging con formato y nivel por defecto
    logging.basicConfig( #Funcion de configuracion unica para el sistema de logging raiz. Solo tiene efecto la primera vez que se llama
        level=logging.DEBUG,  #Captura todos los mensajes desde DEBUG en adelante
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', #Define la estructura de cada linea de log
        datefmt='%d-%m-%Y %H:%M:%S' #Especifica cómo se muestra la fecha
    )

def demostrar_niveles(): #Ejecuta ejemplos de los diferentes niveles de severidad
    logger = logging.getLogger(__name__) #El logger hereda la configuracion del logger raiz (la que establecimos con basicConfig), por lo que ya tiene nivel DEBUG y el formato definido

    logger.debug("Mensaje de depuración: detalles internos, normalmente no se muestra en producción") #Emite un mensaje de nivel DEBUG.Este nivel es el mas bajo y se usa para informacion de depuracion muy detallada
    logger.info("Mensaje informativo: el programa ha iniciado correctamente") #Emite un mensaje nivel INFO.Indica eventos normales del programa, como que una operacion se completo con exito
    logger.warning("Advertencia: algo inesperado pero el programa sigue funcionando") #Emite un mensaje nivel WARNING.Señala una situacion inesperada que no impide la ejecucion, pero que puede derivar en problemas
    logger.error("Error: una operación falló, pero el programa puede continuar") #Emite un mensaje nivel ERROR.Indica que una operación especifica fallo

    #Ejemplo:
    print("\n")
    logger.setLevel(logging.WARNING) #Cambio del umbral de severidad del logger especifico (logger, que apunta a __name__) a WARNING.A partir de ese momento, ese logger solo procesara y mostrara mensajes cuyo nivel sea igual o superior a WARNING
    logger.debug("Este DEBUG no se mostrará (nivel WARNING)")
    logger.info("Este INFO no se mostrará")
    logger.warning("Este WARNING sí se muestra")
    logger.error("Este ERROR sí se muestra")

if __name__ == "__main__":
    configurar_logging()
    demostrar_niveles()