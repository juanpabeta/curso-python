while True:
    try:
        velocidad = float(input("Ingrese la velocidad del vehiculo(km/h): "))
        
        if velocidad < 0:
            print("\n\nLa velocidad no puede ser negativa. Intente de nuevo. \n\n")
            continue
        if velocidad > 300:
            print("\n\n La velocida esta fuera de rango. ingres una velocidad valida \n\n")
            continue
        break
    
    except ValueError:
        print("Entrada no valida Intente de nuevo \n\n")       

if velocidad == 0:
    print("El vehiculo esta detenido")
elif velocidad > 0 and velocidad <= 60:
    print("La velocidad es normal")
elif velocidad > 60 and velocidad <= 120:
    print("La velocidad es rapida")
else:
    print("Exceso de velocidad")