

nombre = input("Dime tu nombre: ")
asignaturas = ["Química","Física","Matemáticas","Sociales","Español"]
repetidas = []

for asignatura in asignaturas:
        nota = float(input(f"Ingrese la nota que obtuvo en la materia {asignatura}: "))
        if nota < 3:
            repetidas.append(asignatura)
            
print(f"\n -------- Las asignaturas a repetir por el estudiante {nombre} -------- ")
for i in repetidas:
    print(i)