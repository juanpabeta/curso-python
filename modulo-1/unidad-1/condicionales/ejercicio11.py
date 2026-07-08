"""
Ejercicio:

1. Número positivo, negativo o cero

Descripción: Solicitar un número e indicar si es positivo, negativo o cero."""

numero = int(input("Ingresa un número: "))
if numero == 0:
    print(f"EL numero es: {numero}")
elif numero > 0:
    print("El numero es positivo")
elif numero <0:
    print("El numero es negativo")
