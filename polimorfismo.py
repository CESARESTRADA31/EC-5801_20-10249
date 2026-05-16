#Cesar Estrada 2010249
#Clases:
class DiscoDuro:
    def __init__(self, tamaño):
    #Def __init__: es el metodo constructor de la clase
    #Self: es una referencia al objeto que se creo; permite acceder a sus atributos y metodos
    #Tamaño: indica cuantas posiciones (memoria) tendra el arreglo interno. El parametro lo proporciona el usuario
        self.tamaño = tamaño #Crea un atributo de instancia "tamaño" (variable que le pertenece a un objeto especifico), y le asigna el valor dado por el usuario
        self.memoria = [0] * tamaño #Crea un arreglo de longitud "tamaño" e inicia todas sus posiciones en 0 (emulando la memoria interna de un disco duro)
        
        self.retraso_lectura = 10      #10 ms
        self.retraso_escritura = 10    
        #Retraso en milisegundos (el más lento)

    def leer(self, posicion): #Definicion del metodo "leer". "posicion" es el parametro que indica la direccion de memoria que se quiere leer

        if posicion < 0 or posicion >= self.tamaño: #Condificion que verifica que la posicion no este fuera de rango. No se permiten numeros negativos y si la posicion es mayor o igual al tamaño del arreglo, no existe
            raise IndexError("Posición fuera de rango en Disco Duro")
        print(f"  [Disco Duro] Leyendo posición {posicion} -> retraso de {self.retraso_lectura} ms") #Informa al usuario que se está realizando una operación de lectura, indicando cuanto tiempo se "demora" la lectura
        return self.memoria[posicion]

    def escribir(self, posicion, valor): #Definicion el metodo "escribir". "valor" es el dato que se desea almacenar (en nuestro caso, un entero)

        if posicion < 0 or posicion >= self.tamaño: #Misma condicion de error que el metodo "leer"
            raise IndexError("Posición fuera de rango en Disco Duro")
        print(f"  [Disco Duro] Escribiendo '{valor}' en posición {posicion} -> retraso de {self.retraso_escritura} ms") #Informa al usuario que se está realizando una operación de escritura, indicando cuanto tiempo se "demora" la escritura
        self.memoria[posicion] = valor

class MemoriaRam: #Se construye de la misma forma que la clase DiscoDuro
    def __init__(self, tamaño):
     
        self.tamaño = tamaño
        self.memoria = [0] * tamaño
        self.retraso_lectura = 100    #100 ns
        self.retraso_escritura = 100

    def leer(self, posicion):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango en RAM")
        print(f"  [RAM] Leyendo posición {posicion} -> retraso de {self.retraso_lectura} ns")
        return self.memoria[posicion]

    def escribir(self, posicion, valor):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango en RAM")
        print(f"  [RAM] Escribiendo '{valor}' en posición {posicion} -> retraso de {self.retraso_escritura} ns")
        self.memoria[posicion] = valor

class MemoriaSram: #Se construye de la misma forma que las clases anteriores
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.memoria = [0] * tamaño
        self.retraso_lectura = 10     #10 ns
        self.retraso_escritura = 10

    def leer(self, posicion):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango en SRAM")
        print(f"  [SRAM] Leyendo posición {posicion} -> retraso de {self.retraso_lectura} ns")
        return self.memoria[posicion]

    def escribir(self, posicion, valor):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango en SRAM")
        print(f"  [SRAM] Escribiendo '{valor}' en posición {posicion} -> retraso de {self.retraso_escritura} ns")
        self.memoria[posicion] = valor

#Funciones polimorficas (actuan como un bus de memoria)
def bus_leer(dispositivo, posicion): #Definicion de la funcion "bus_leer", que simula una operacion de lectura en un bus de memoria. "dispositivo" representa cualquier objeto que tenga un metodo leer()
#"posicion" es el parametro del indice de memoria donde se quiere leer
    print(f"\n[Bus] Solicitando lectura en posición {posicion}") #Imprime mensaje indicando que el bus esta iniciando una operacion de lectura
    valor = dispositivo.leer(posicion) #Polimorfismo: la funcion invoca "dispostivo.leer(posicion)" sin saber que tipo de objeto es "dispositivo" (Puede ser DiscoDuro,MemoriaRam o MemoriaSram)
    print(f"[Bus] Lectura completada: valor = {valor}")  #Mensaje que indica que la operacion termino y muestra el valor obtenido
    return valor #Devuelve el valor leído para que el código que llamó a "bus_leer" pueda usarlo

def bus_escribir(dispositivo, posicion, valor): #Definicion de la funcion "bus_escribir", que simula una operacion de escritura del bus de memoria
#"valor" es el dato que queremos almacenar, "dispositivo" un objeto que implemente el metodo "escribir", "posicion" entero que indica la direccion de memoria donde se va a guardar el dato
    print(f"\n[Bus] Solicitando escritura del valor '{valor}' en posición {posicion}")
    dispositivo.escribir(posicion, valor) #Polimorfismo: El bus no sabe que es el "dispositivo", confia en que el objeto tiene el metodo "escribir" y lo invoca con sus argumentos
    print(f"[Bus] Escritura completada")

#Ejemplo
if __name__ == "__main__":
    print("DEMOSTRACIÓN DE POLIMORFISMO")
    print("Se crean 3 dispositivos con tamaño 5 cada uno.")
    
    #Crear instancias de cada tipo de memoria
    disco = DiscoDuro(5)
    ram = MemoriaRam(5)
    sram = MemoriaSram(5)
    
    #Lista de dispositivos (todos son diferentes, pero compatibles polimorficamente)
    dispositivos = [disco, ram, sram]
    
    #Escribir un valor en la posicion 2 de cada dispositivo usando la funcion polimorfica
    for dispositivo in dispositivos:
        bus_escribir(dispositivo, 2, 42)
    
    #Leer desde la misma posicion de cada dispositivo
    for dispositivo in dispositivos:
        bus_leer(dispositivo, 2)
    
    print("\nFin de la demostracion")
    print("Se ha utilizado el mismo bus (mismas funciones) para tres tipos de memoria")
    print("con comportamientos (retrasos) completamente diferentes")
