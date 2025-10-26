""" 
OPERADORES RELACIONALES

Enunciado:
Crea un programa en Python que pida al usuario ingresar dos números y muestre en pantalla el resultado de las siguientes comparaciones:

Si el primer número es mayor que el segundo.

Si el primer número es menor que el segundo.

Si ambos números son iguales.

"""
n1 = int(input("Ingresa el primer número: "))
n2 = int(input("Ingresa el segundo número: "))

if n1 >n2:
    print(f"El primer número ({n1}) es mayor que el segundo número ({n2}).")
if n1 < n2:
    print(f"El primer número ({n1}) es menor que el segundo número ({n2}).")
if n1 == n2:
    print(f"Ambos números son iguales: {n1} = {n2}.")