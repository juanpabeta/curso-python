"""
Préstamo de Libros en una Biblioteca 
Una biblioteca escolar quiere crear un programa en consola en Python para controlar qué estudiantes tienen libros prestados.
El sistema no usará base de datos ni clases.
Solo debe utilizar:
•	Diccionarios (dict)
•	Conjuntos (set)
Situación
La biblioteca tiene varios libros identificados por un código único.
Ejemplo de libros:
•	L1 → El principito
•	L2 → Cien años de soledad
•	L3 → Python básico
Cada libro puede prestarse a un solo estudiante a la vez.
Los estudiantes se identifican por su número de documento.

Cómo debe guardarse la información
1. Catálogo de libros (diccionario)
El diccionario guardará el nombre del libro y si está disponible o prestado.
Ejemplo conceptual:
libros = {
    "L1": True,
    "L2": False,
    "L3": True
}
Donde:
•	True = disponible
•	False = prestado

2. Préstamos por estudiante (diccionario + set)
Cada estudiante tendrá un conjunto (set) con los códigos de los libros que tiene prestados.
prestamos = {
    "1010": {"L1", "L3"},
    "1020": {"L2"}
}
El set evita que el estudiante pueda tener el mismo libro dos veces.

Reglas
1.	No se puede prestar un libro si ya está prestado.
2.	No se puede prestar el mismo libro dos veces al mismo estudiante.
3.	Cuando se devuelve un libro, vuelve a quedar disponible.
4.	Si el estudiante no existe, se crea automáticamente cuando pide su primer libro.
5.	Si intenta devolver un libro que no tiene, debe mostrarse un mensaje de error.

Opciones del programa
El sistema debe mostrar un menú:
1.	Prestar libro
2.	Devolver libro
3.	Ver libros de un estudiante
4.	Ver estado de todos los libros
5.	Salir

"""
from typing import Set,Dict

libros = {
    "L1": True,
    "L2": True,
    "L3" : False,
    "L4" : False,
    "L5" :True
}

prestamos = {
    "1010": {"L1", "L3"},
    "1020": {"L2"},
    "1030": {"L4","L5"}
}

    
def _prestar_libro(libros:Dict[str,bool],prestamos:Dict[str,Set[str]])-> None :
    documento_estudiante = input("Ingresa el documento del estudiante: ").strip()
    id_libro = input("Ingresa el id del libro: ").strip()
    
    if id_libro not in libros:
        print("El libro no existe")
    if documento_estudiante not in prestamos:
        print("El estudiante no existe")
        prestamos[documento_estudiante] = set()
    if not libros[id_libro]:
        print("El libro esta prestado")
        
    