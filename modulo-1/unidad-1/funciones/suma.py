def suma()-> int:    
    n1 = int(input("Ingresa un numero: "))
    n2 = int(input("Ingresa otro numero: "))
    suma = n1 + n2
    return suma

print(f"La suma de los numeros es: {suma()}")