precios = [50,75,46,22,80,65,8]
mayor = precios[0]
menor = precios[0]

for precio in precios:
    if precio > mayor:
        mayor = precio
    if precio < menor:
        menor = precio
        
print(f"El precio mayor es: {mayor}")
print(f"El precio menor es: {menor}")
        