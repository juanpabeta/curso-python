edad = input("Por favor, ingresa tu edad: ")


if edad.isdigit():
    edad = int(edad)
    print(f"La edad ingresada es válida: {edad}")
else:
    print("La edad ingresada no es válida. Por favor, ingresa un número entero positivo.")