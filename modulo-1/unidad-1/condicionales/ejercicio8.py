numero = int(input("Ingrese un número entero: "))
numero2 = int(input("Ingrese otro número entero: "))

operador = input("Dime un operador (+, -, *, /): ")

match operador:
    case "+":
        print(f"La suma es: {numero + numero2}")
    case "-":
        print(f"La resta es: {numero - numero2}")
    case "*":
        print(f"La multiplicación es: {numero * numero2}")
    case "/":
        if numero2 != 0:
            print(f"La división es: {numero / numero2}")
        else:
            print("Error: División por cero no permitida.")