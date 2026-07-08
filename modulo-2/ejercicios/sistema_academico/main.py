from conexion import Conexion
from alumno import crear_alumno, eliminar_alumno
from programas import crear_programa
from notas import crear_nota
from consultas import alumnos_por_programa

def menu():
    while True:
        print("="*50)
        print("\n SISTEMA ACADÉMICO")
        print("="*50)
        print("1. Crear programa")
        print("2. Crear alumno")
        print("3. Eliminar alumno")
        print("4. Ver alumno")
        print("5. Crear nota")
        print("6. Salir")
        
        opcion = input("Escoja una opción: ")
        
        match (opcion):
            case ("1"):
                nombre = input("Ingrese el nombre del programa: ")  
                crear_programa(nombre)
            case ("2"):
                nombre = input("Ingrese el nombre del alumno: ")
                email = input("Ingrese el email del alumno: ")
                programa_id = input("Ingrese el ID del programa: ")
                crear_alumno(nombre,email,programa_id)  
            case ("3"):
                id_alumno = input("Ingrese el ID del alumno a eliminar: ")
                eliminar_alumno(id_alumno)
            case ("4"):
                programa_id = input("Ingrese el ID del programa para ver sus alumnos: ")
                alumnos_por_programa(programa_id)
            case ("5"):
                id_alumno = input("Ingrese el ID del alumno para asignar la nota: ")
                nota = float(input("Ingrese la nota (0-5): "))
                crear_nota(id_alumno,nota)
            case ("6"):   
                print("Saliendo del sistema...")
                break     
            case _:
                print("Opción no válida, por favor intente de nuevo.")
                
if __name__ == "__main__":
    menu()