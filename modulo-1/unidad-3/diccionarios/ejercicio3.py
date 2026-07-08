from typing import Dict,Any

biblioteca: Dict[str, Dict[str, Any]] = {
    "L001": {
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "año": 1967,
        "disponible": True
    },
    "L002": {
        "titulo": "1984",
        "autor": "George Orwell",
        "año": 1949,
        "disponible": False
    },
    "L003": {
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "año": 1605,
        "disponible": True
    }
}

DISPONIBLE = "Disponible"
NO_DISPONIBLE = "No disponible"

#Funciones auxiliares
def _obtener_libro(codigo:str) -> Dict[str,Any]:
    if codigo not in biblioteca:
        raise KeyError(f"El libro de código {codigo} no se encuentra")
    return biblioteca[codigo]

def _estado_legible(disponible:bool) -> str:
    return DISPONIBLE if disponible else NO_DISPONIBLE

def mostrar_libro(codigo: str) -> None:
    try:
        libro = _obtener_libro(codigo)
        print(f"\nCódigo: {codigo}")
        print(f"Título: {libro['titulo']}")
        print(f"Autor: {libro['autor']}")
        print(f"Año: {libro['año']}")
        print(f"Estado: {_estado_legible(libro['disponible'])}")
    except KeyError as error:
        print(f"\n{error}")
        
def cambiar_disponibilidad(codigo:str)->None:
    try:
        libro = _obtener_libro(codigo)
        libro["disponible"] = not libro["disponible"]
        print(
            f"\nEstado actualizado del libro {codigo}"
            f"{_estado_legible(libro['disponible'])}"
        )
    except KeyError as error:
        print(f"No se puede cambiar la disponilidad. {error}")
        
def main()->None:
    
    cambiar_disponibilidad("L002")
    cambiar_disponibilidad("L003")
    mostrar_libro("L003")
    mostrar_libro("L002")
    mostrar_libro("L230")
    
if __name__ == "__main__":
    main()