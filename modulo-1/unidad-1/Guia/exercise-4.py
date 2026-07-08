
def puede_votar()-> str:
    edad = int(input("Ingrese la edad: "))    
    if edad >= 18:
        print("Puedes votar 🗳️")
    elif edad >= 7 and edad < 18:
        print("Presenta tu tarjeta de identidad 🪪")
    else:
        print("No tienes edad suficiente edad para tener un documento")

puede_votar()