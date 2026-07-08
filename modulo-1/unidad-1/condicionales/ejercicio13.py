"""3. Clasificador de edad

Descripción: Pedir la edad del usuario y clasificarla en rangos.

| Rango | Mensaje      |
| ----- | ------------ |
| 0–12  | Niño         |
| 13–17 | Adolescente  |
| 18–59 | Adulto       |
| 60+   | Adulto mayor |
"""

edad = int(input("Ingresa la edad: "))
if edad >= 0 and edad <= 12:
    print("Eres un niño")
elif edad >= 13 and edad <= 17:
    print("Eres un adolescente")
elif edad >= 18 and edad <= 59:
    print("Eres un adulto")
elif edad >= 60:
    print("Eres un un adulto mayor")