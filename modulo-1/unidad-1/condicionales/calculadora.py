
numero1 = int(input("Ingresa un numero entero: "))
numero2 = int(input("Ingresa un numero entero: "))

operador = input("Ingresa un operador + - x /: ")
if operador == "+":
    print(f"La suma de los numeros es: {numero1+numero2} ")
elif operador == "-":
    print(f"La resta de los numeros es: {numero1-numero2} ")
elif operador == "x":
    print(f"La multiplicacion de los numeros es: {numero1*numero2} ")
elif operador == "/":
    print(f"La resta de los numeros es: {numero1//numero2} ")
else:
    print("Operador invalido :<")