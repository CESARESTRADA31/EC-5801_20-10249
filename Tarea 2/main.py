from pathlib import Path
from yaml_manager import YamlManager
from schema_validator import schema_validator

#Esquema que deben cumplir los datos (claves exactas del YAML)
ESQUEMA_PERSONAJE = {
    "nombre": str,
    "altura": float,
    "peso": float,
    "edad": int,
    "lista_habilidades": [str],   #Lsta de strings
    "descripcion": str
}

@schema_validator(ESQUEMA_PERSONAJE)
def validar_personaje(datos: dict) -> dict: #Funcion identidad que valida la salida contra el esquema
    return datos

def cargar_y_validar_todo(manager: YamlManager, nombre: str, archivo: str): #Carga el YAML, valida cada personaje y retorna el diccionario completo si todos son validos
    manager.cargar(nombre, archivo)
    todos = manager.obtener(nombre)
    
    for clave, datos_personaje in todos.items():
        if validar_personaje(datos_personaje) is None:
            raise ValueError(f"Error de validación en '{clave}'. Los datos no cumplen el esquema.")
        print(f"✓ {clave} validado correctamente.")
    return todos

def main():
    print("Sistema de validación y gestión de YAML\n")
    
    #Ruta al archivo config.yaml (misma carpeta que este script)
    script_dir = Path(__file__).parent
    archivo_yaml = script_dir / "config.yaml"
    
    if not archivo_yaml.exists():
        print(f"Error: No se encontró {archivo_yaml}")
        return
    
    manager = YamlManager()
    nombre_almacen = "mi_config"
    
    #Cargar y validar el personaje
    try:
        datos_completos = cargar_y_validar_todo(manager, nombre_almacen, str(archivo_yaml))
        print("\nTodos los datos cumplen el esquema.\n")
    except Exception as e:
        print(f"Error durante la carga/validación: {e}")
        return
    
    #Modificar TODOS los datos del personaje
    personaje = next(iter(datos_completos)) 
    print(f"Modificando todos los datos de '{personaje}'...")
    
    #Nuevos datos completos
    nuevos_datos = {
        "nombre": "Cesar Estrada",
        "altura": 1.75,
        "peso": 67.0,
        "edad": 23,
        "lista_habilidades": ["Python Basico", "Simulacion en Proteus"],
        "descripcion": "Trabajo mejor bajo presion"
    }
    
    #Reemplazar el diccionario del personaje
    datos_completos[personaje] = nuevos_datos
    
    #Validar el personaje modificado
    if validar_personaje(datos_completos[personaje]) is None:
        print("La modificación no cumple el esquema. No se guardarán cambios.")
        return
    
    #Actualizar el almacenamiento y guardar a disco
    manager.modificar(nombre_almacen, datos_completos)
    manager.guardar(nombre_almacen)
    
    print(f"Datos guardados exitosamente en '{archivo_yaml}'.")
    print("\nContenido final del archivo YAML:")
    print(manager.leer(str(archivo_yaml), modo_binario=False))

if __name__ == "__main__":
    main()
