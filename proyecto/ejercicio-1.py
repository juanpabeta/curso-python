"""
Proyecto práctico integrador

Aplicación de consola: Sistema de Registro de Estudiantes

Descripción: Crear una aplicación modular que permita:

1. Registrar estudiantes.
2. Mostrar todos los registros.
3. Buscar estudiante por nombre.
4. Calcular promedio general.
5. Validar entradas y salidas.

"""

# lista
estudiantes = []

def registrar_estudiantes():
    print("\n--- Registrar estudiante ---")
    nombre = input("Nombre: ").strip().title()
    edad = int(input("Edad: "))
    nota = float(input("Nota (0 - 5): "))
    
    estudiante = {"nombre": nombre, "edad": edad, "nota": nota}
    estudiantes.append(estudiante)
    print("Estudiante registrado satisfactoriamente")


def mostrar_estudiantes():
    print("\n--- Lista de estudiantes ---")
    if not estudiantes:
        print("No hay estudiantes registrados.")
    else:
        for i, e in enumerate(estudiantes, 1):
            print(f"{i}. {e['nombre']} - {e['edad']} años - Nota:{e['nota']}") # 1. Luis Molero - 50 años - Nota: 5.0


def buscar_estudiante():
    print("\n--- Buscar un estudiante ---")
    nombre = input("Ingrese el nomvbre a buscar: ").strip().lower()
    
    encontrados = [e for e in estudiantes if nombre in e["nombre"].lower()]
    
    if encontrados:
        for e in encontrados:
            print(f"{e['nombre']} - {e['edad']} años - Nota:{e['nota']}") # 1. Luis Molero - 50 años - Nota: 5.0
    else:
        print("No se encontro ningún estudiante registrado.")

def calcular_promedio():
    print("\n--- Promedio General ---")
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    notas = [e ["nota"] for e in estudiantes]
    promedio = sum(notas) / len(notas)
    print(f"Promedio General: {promedio:.1f}")

def menu():
    while True:
        print("\n*** MNEÚ PRINCIPAL ***")
        print("1. Registrar estudiantes.")
        print("2. Mostrar todos los registros.")
        print("3. Buscar estudiante por nombre.")
        print("4. Calcular promedio general.")
        print("5. Salir")
        
        opcion = input("Elija un opción (1-5): ")
        
        if opcion == "1":
            registrar_estudiantes()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            buscar_estudiante()
        elif opcion == "4":
            calcular_promedio()
        elif opcion == "5":
            print("Hasta lueguito.....")
            break
        else:
            print("Opción invalida, intente de nuevo..")


def main():
    menu()

if __name__ == "__main__":
    main()