#Matrices con polimorfismo Cesar Estrada 2010249
class Matriz:
    #Clase para representar una matriz de tamaño M x N (M filas, N columnas).

    def __init__(self, filas, columnas, datos=None):
        #Construccion de la matriz
        self.filas = filas
        self.columnas = columnas
        if datos is not None:
            if len(datos) != filas or any(len(fila) != columnas for fila in datos):
                raise ValueError("Los datos no tienen la forma especificada (filas x columnas)")
            self.datos = [fila[:] for fila in datos]
        else:
            self.datos = [[0] * columnas for _ in range(filas)]

    def __getitem__(self, indice):
        if isinstance(indice, tuple):
            i, j = indice
            return self.datos[i][j]
        else:
            return self.datos[indice]

    def __setitem__(self, indice, valor):
        if isinstance(indice, tuple):
            i, j = indice
            self.datos[i][j] = valor
        else:
            self.datos[indice] = valor

    def __str__(self):
        return "\n".join(["\t".join(map(str, fila)) for fila in self.datos])

    def __repr__(self):
        return f"Matriz({self.filas}, {self.columnas}, {self.datos})"

    #Operaciones con polimorfismo:
    def __add__(self, otra): #Suma de matrices
        if not isinstance(otra, Matriz):
            raise TypeError("Solo se puede sumar otra Matriz")
        if self.filas != otra.filas or self.columnas != otra.columnas:
            raise ValueError("Las dimensiones deben coincidir para la suma")
        resultado = Matriz(self.filas, self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                resultado[i, j] = self.datos[i][j] + otra.datos[i][j]
        return resultado

    def __sub__(self, otra): #Resta de matrices
        if not isinstance(otra, Matriz):
            raise TypeError("Solo se puede restar otra Matriz")
        if self.filas != otra.filas or self.columnas != otra.columnas:
            raise ValueError("Las dimensiones deben coincidir para la resta")
        resultado = Matriz(self.filas, self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                resultado[i, j] = self.datos[i][j] - otra.datos[i][j]
        return resultado

    def __mul__(self, otro): #Multiplicacion de matrices. El parametro "otro" puede ser un flotante o una matriz (si es este ultimo, se hace el producto matricial)
        if isinstance(otro, (int, float)):
            #Multiplicacion escalar del lado derecho Matriz * (flotante) (devuelve nueva matriz)
            resultado = Matriz(self.filas, self.columnas)
            for i in range(self.filas):
                for j in range(self.columnas):
                    resultado[i, j] = self.datos[i][j] * otro
            return resultado
        elif isinstance(otro, Matriz):
            #Producto matricial
            if self.columnas != otro.filas:
                raise ValueError("Número de columnas de la primera debe coincidir con filas de la segunda")
            resultado = Matriz(self.filas, otro.columnas)
            for i in range(self.filas):
                for j in range(otro.columnas):
                    suma = 0
                    for k in range(self.columnas):
                        suma += self.datos[i][k] * otro.datos[k][j]
                    resultado[i, j] = suma
            return resultado
        else:
            raise TypeError("Multiplicación no soportada con tipo {}".format(type(otro)))

    def __rmul__(self, otro): #Misma multiplicacion de matrices por escalar(flotante) pero por el lado izquierdo; el usuario escribe el escalar primero, es decir, (flotante) * Matriz en vez de Matriz * (flotante) como en el caso anterior
        #Simplemente se reutiliza__mul__ 
        #Este metodo se hace para evitar errores con el orden que el usuario coloca/hace la multiplicacion escalar. No es necesario para el producto matricial porque siempre sera Matriz x Matriz
        if isinstance(otro, (int, float)):
            return self.__mul__(otro)
        else:
            raise TypeError("Multiplicación escalar no soportada con tipo {}".format(type(otro)))

    def __truediv__(self, otro): #Division real deshabilitada
        raise NotImplementedError("La división de matrices no está definida")

    def __floordiv__(self, otro): #Division entera deshabilitada
        raise NotImplementedError("La división de matrices no está definida")

    #Caracteristicas generales de las matrices
    def dimension(self):
        return (self.filas, self.columnas)

    def es_cuadrada(self):
        return self.filas == self.columnas

    def copiar(self):
        return Matriz(self.filas, self.columnas, self.datos)

    def trasponer(self):
        traspuesta = Matriz(self.columnas, self.filas)
        for i in range(self.filas):
            for j in range(self.columnas):
                traspuesta[j, i] = self.datos[i][j]
        return traspuesta

    def escalar(self, escalar):
        
        for i in range(self.filas):
            for j in range(self.columnas):
                self.datos[i][j] *= escalar
        return self
    
    #Matriz identidad
    @staticmethod
    def identidad(n):
        ident = Matriz(n, n)
        for i in range(n):
            ident[i, i] = 1
        return ident

    #Metodos de instancia para delegar en los operadores +, - y * los métodos especiales definidos anteriormente (___add___, __sub__ y ___mul__)
    def suma(self, otra):
        return self + otra

    def resta(self, otra):
        return self - otra

    def producto(self, otra):
        return self * otra
    
#Ejemplo
if __name__ == "__main__":
    #Espacio para crear lo datos de la matriz
    datos2 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9 ]
    ]
    datos1 = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    #Espacio para nombrar/hacer la matriz.La escala de tamaño debe coincidir con los datos creados anteriormente

    A = Matriz(3, 3, datos2)
    B = Matriz(3, 3, datos1)   

    #Espacio para hacer las operaciones que se desee, usando "prints"
    print("Matriz A:")
    print(A)

    print("\nSuma A + A:")
    print(A + B)

    print("\nResta A - A (matriz cero):")
    print(A - B)

    print("\nMultiplicación escalar 3 * A:")
    print(3 * A)

    print("\nProducto matricial B * A:")
    print(B * A)

    #Prueba de division (deshabilitada)
    try:
        print(A / A)
    except NotImplementedError as e:
        print("\nDivisión capturada:", e)
