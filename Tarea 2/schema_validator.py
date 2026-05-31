from typing import Any, Callable, Optional
#"Any": indica que un valor puede ser de cualquier tipo (para data y schema en el validador)
#"Callable": para tipar la función que se va a decorar
#"Optional":  el decorador puede retornar None (cuando falla la validación) o cualquier otro valor

def __validate(data: Any, schema: Any) -> bool: #Valida recursivamente que "data" cumpla con "schema".Retorna True si es valido, False en caso contrario
    if isinstance(schema, dict): #Comprueba si schema es una instancia de dict.Si es True, se entra en el bloque de validacion para diccionarios
        if not isinstance(data, dict): #Si data no es un diccionario, la validacion falla inmediatamente (return false)
            return False
        for key, subschema in schema.items(): 
            if key not in data: #Si la clave no existe, falla la validacion
                return False
            if not __validate(data[key], subschema):
                return False
        return True
    
    #Esquema tipo lista generica: list -> data debe ser lista sin restriccion de tipos
    if schema is list:
        return isinstance(data, list)
    
    #Esquema tipo lista con especificacion de tipo
    if isinstance(schema, list):
        if not isinstance(data, list):
            return False
        if len(schema) == 0:
            return True  #Lista vacia como esquema acepta cualquier lista (vacia)
        if len(schema) != 1:
            #El validador solo acepta un tipo por elemento
            return False
        tipo_elemento = schema[0]
        #Todos los elementos deben cumplir el tipo
        return all(__validate(item, tipo_elemento) for item in data)
    
    #Esquema tipo basico (int, str, float)
    if isinstance(schema, type):
        return isinstance(data, schema)
    
    #Esquema literal
    return data == schema  #Caso base por defecto que se ejecuta cuando ninguna de las condiciones anteriores se cumplio


def schema_validator(schema: dict): #Fabrica de decoradores. Recibe un esquema y retorna un decorador que valida el resultado de la funcion decorada contra el esquema.
    #Si la validacion falla, retorna None
    def decorator(func: Callable) -> Callable: #Recibe la funcion original (func) que sera decorada. Se encarga de construir la funcion wrapper
        def wrapper(*args, **kwargs) -> Optional[Any]: #Es la funcion que ejecutara cuando se llame a la funcion decorada. Toma cualquier cantidad de argumentos posicionales (*args) y nominales (**kwargs) y los pasa íntegramente a la funcion original (func)
            result = func(*args, **kwargs) ##Valida result contra el schema (capturado del primer nivel) usando __validate(result, schema)
            if not __validate(result, schema):
                return None
            return result
        return wrapper
    return decorator

