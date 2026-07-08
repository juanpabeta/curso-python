def mayor():
    n1 = int(input("Ingresa un numero: "))
    n2 = int(input("Ingresa otro numero: "))
    n3 = int(input("Ingresa otro numero: "))
    
    if n1 > n2 and n1 > n3:
        print("El numero 1 es el mayor")
    elif n2 > n1 and n2 > n3:
        print("El numero 2 es el mayor")
    else:
        print("El numero 3 es el mayor")
        
mayor()