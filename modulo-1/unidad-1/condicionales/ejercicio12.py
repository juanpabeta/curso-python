"""2. Clasificador de notas

Descripción: El usuario ingresa una nota de 0 a 100. Mostrar el nivel académico según el puntaje.

| Rango  | Mensaje   |
| ------ | ----------|
| 90–100 | Excelente |
| 70–89  | Aprobado  |
| 0–69   | Reprobado |
"""

nota = float(input("Ingresa una nota entre 0 y 100: "))

if nota >=0 and nota <= 69:
    print("Reprobaste el curso")
elif nota >= 70 and nota <= 89:
    print("Aprobaste el curso")
elif nota >= 90 and nota <= 100:
    print("felicitaciones, has sacado un excelente en el curso 🎉")
else:
    print("Ingresa un numero valido")