"""
EJERCICIOS

Ejercicio 1: Verificar mayoría de edad
1. Enunciado:
Pide la edad de una persona y muestra un mensaje si es mayor de edad (18 años o más).

2. Ejercicio 2: Determinar si un número es positivo
Enunciado:
Pide un número y muestra un mensaje si el número es positivo.

3. Ejercicio 3: Verificar rango de valores

Enunciado:
Pide un número y muestra un mensaje solo si está entre 10 y 50 (inclusive).
"""

edad = int(input("Ingresa tu edad: "))
numero = int(input("Ingresa un número: "))


if edad >= 18:
    print("Eres adulto") 
    
if numero > 0:
    print("El número es positivo")   


if numero >= 10 and numero <= 50:
    print("El número está entre 10 y 50")
else:
    print("El número no está entre 10 y 50")