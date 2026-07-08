suma = 0
numero = int(input("Ingrese un numero (0 para salir") )
while numero != 0:
    suma += numero
    numero = int(input("Ingrese otro numero (0 para salir): ") )
            
print (f"La suma total es => {suma}")