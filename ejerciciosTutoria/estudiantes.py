
def registrar_estudiante():
    
    nombre = input("ingrese el nombre del estudiante: ")
    while True:
        try:
            edad = int(input("ingrese la edad del estudiante: "))
            if edad <= 0:
                print("el estudiante debe tener una edad mayor que cero")
            else:
                print("Edad agregada correctamente")
                break
        except:
            raise ValueError("Error, ingresa un número")
        
    while True:
        try:
            n1 = float(input("Ingrese la primera nota: "))
            
            if n1 < 0 or n1 >= 5 :
                print("La nota debe ser mayor que cero y menor que 5")
            else:
                print("Nota agregada correctamente")
                break
        except ValueError:
            print("Error, la nota debe ser un flotante")

    while True:
        try:
            n2 = float(input("Ingrese la segunda nota: "))
            
            if n2 < 0 or n2 >= 5 :
                print("La nota debe ser mayor que cero y menor que 5")
            else:
                print("Nota agregada correctamente")
                break
        except ValueError:
            print("Error, la nota debe ser un flotante")
        
    while True:
        try:
            n3 = float(input("Ingrese la tercera nota: "))
            
            if n3 < 0 or n3 >= 5 :
                print("La nota debe ser mayor que cero y menor que 5")
            else:
                print("Nota agregada correctamente")
                break
        except ValueError:
            print("Error, la nota debe ser un flotante")
        
    return nombre,edad,n1,n2,n3

def calcular_promedio(n1,n2,n3):
    promedio = (n1+n2+n3) / 3
    return promedio

def evaluar_estado(promedio):
    if promedio >= 0 and promedio < 3:
        return "Desaprobado"
    elif promedio >= 3 and promedio <= 5:
        return "Aprobado"
    
contador = 0
prom = 0
   
while True:   
    print("=== SISTEMA DE ESTUDIANTES ===")
    print("1. Registrar estudiantes")
    print("2. salir")
    opcion = input("Ingresa una opción: ")
    
    if opcion == "1":
        nombre,edad,n1,n2,n3 = registrar_estudiante()
        promedio = calcular_promedio(n1,n2,n3)
        evaluar_estado(promedio)
        contador+= 1
        prom += promedio
        
    if opcion == "2":
        print(f"Total de estudiantes registrados: {contador}")
        if contador > 0:
            print(f"Promedio general del grupo: {prom/contador}")
        else:
            print("no ha sido agregado ningun estudiante")
        
        break

    else:
        print("Ingresa una opción válida")
        
        
        
    
    