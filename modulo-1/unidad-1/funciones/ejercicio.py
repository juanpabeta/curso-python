def suma(n1:int, n2:int)-> int:
    resultado = n1 + n2
    return f"El resultado de la suma de los numeros {n1} + {n2} = {resultado}"

print(suma(5,4))

estudiantes = []

def agregar_estudiante(nombre:str):
    estudiantes.append(nombre)
    print(f" \n Estudiantes agregados \n:{estudiantes} ")
    
agregar_estudiante("Juan Pablo")
agregar_estudiante("Cristian")
agregar_estudiante("Antonio")