#Herencia Cesar Estrada 2010249
#Clase padre: Punto en 3 dimensiones (X, Y, Z)
class Punto: #Se crea la clase "Punto", el cual representa un punto en el espacio 3D con coordenadas privadas.
    def __init__(self, x: float, y: float, z: float): #__init__ es el metodo constructor de la clase. Los parametros x,y,z son valores para crear el punto (se espera que sean flotantes, por eso el ":float")
        self.__x = x  #Coordenada X privada
        self.__y = y  #Coordenada Y privada
        self.__z = z  #Coordenada Z privada

    #"Gets" para acceder a las coordenadas privadas desde la clase hija
    def get_x(self) -> float: #Devuelve el valor de la coord X
        return self.__x

    def get_y(self) -> float: #Devuelve el valor de la Coord Y
        return self.__y

    def get_z(self) -> float: #Devuelve el valor de la coord Z
        return self.__z

    #Operaciones públicas
    def sumar_escalar(self, escalar: float) -> None: #Suma un mismo escalar a cada una de las tres coordenadas, modifica directamente el punto
        self.__x += escalar
        self.__y += escalar
        self.__z += escalar

    def multiplicar_escalar(self, escalar: float, ejes: list = None) -> None: #Multiplica un escalar por uno o varios ejes del punto (operacion publica)
        #"ejes" lista con los ejes a modificar (x,y,z)
        if ejes is None:
            ejes = ['x', 'y', 'z']

        if 'x' in ejes:
            self.__x *= escalar
        if 'y' in ejes:
            self.__y *= escalar
        if 'z' in ejes:
            self.__z *= escalar
    
    def obtener_coordenadas(self) -> tuple: #Devuelve una tupla con las coordenadas actuales (solo lectura)
        return (self.__x, self.__y, self.__z)

#Clase hija: Vector (hereda de Punto)
class Vector(Punto): #Se crea una clase "vector()" que hereda la clase "(punto)", por lo cual tiene todos los atributos y metodos de este ultimo.
    def __init__(self, x: float, y: float, z: float): #Constructor de la clase, se recibe los 3 componentes del vector. El origen implicito del vector es (0,0,0).
        super().__init__(x, y, z) #Llamada a la clase padre (Punto)."super()" devuelve un objeto que permite acceder a métodos de la clase padre

    def magnitud(self) -> float: #Se crea el metodo "magnitud", el cual calcula y devuelve la longitud del vector. Se usa la formula clasica de la raiz cuadrada de la suma de los componentes al cuadrado
        x = self.get_x()
        y = self.get_y()
        z = self.get_z()
        #"get()" para acceder a las coords privadas
        return (x ** 2 + y ** 2 + z ** 2) ** 0.5 #Calculo de la raiz cuadrada mediante el operador ** 0.5

#Ejemplo
if __name__ == "__main__":
    #Crear un punto y mostrar sus coordenadas
    p = Punto(3, 4, 5)
    print("Prueba de la clase Punto")
    print(f"Punto inicial: {p.obtener_coordenadas()}")

    #Multiplicar solo los ejes X e Y por 3
    p.multiplicar_escalar(3, ejes=['x', 'y'])
    print(f"Multiplicar X e Y por 3: {p.obtener_coordenadas()}") 

    #Crear un vector (hereda de Punto)
    v = Vector(3, 4, 5)
    print("\nPrueba de la clase Vector")
    print(f"Vector: componentes = ({v.get_x()}, {v.get_y()}, {v.get_z()})")
    print(f"Magnitud del vector: {v.magnitud():.2f}")  

    #Verificar que el vector puede usar las operaciones heredadas
    v.sumar_escalar(1)
    print(f"Vector tras sumar 1: ({v.get_x()}, {v.get_y()}, {v.get_z()})")
    print(f"Nueva magnitud: {v.magnitud():.2f}") 