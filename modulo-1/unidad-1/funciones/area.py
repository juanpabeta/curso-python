def area_triangulo()-> float:
    base = float(input("Ingresa la base del triangulo: "))
    altura = float(input("Ingresa la altura del triangulo: "))
    
    area = base * altura// 2
    return area

print(f"El area del triangulo es: {area_triangulo()}")