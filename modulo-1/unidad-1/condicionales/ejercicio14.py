"""5. Verificar hora del día

Descripción: Pedir la hora (0 a 23) e indicar si es mañana, tarde o noche."""

while True:
    entrada = input("Ingrese la hora (0-23): ")
    if entrada.isdigit():
        hora_dia = int(entrada)
        if hora_dia >=0 and hora_dia <= 23:
            break
        else:
            print("Error: La hora es invalida")


if hora_dia >=0 and hora_dia <=12:
    print("Es de mañana 🌄")
elif hora_dia > 12 and hora_dia <= 18:
    print("Es de tarde ☀️ 😎 ")
elif hora_dia>18:
    print("Es de noche 🌚")
else:
    print("Ingrese una hora valida")
    