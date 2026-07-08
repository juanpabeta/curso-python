compra = float(input("Ingrese el valor de su compra: "))


if compra >= 50000:
    descuento = 0.20
elif compra >= 20000 and compra < 50000:
    descuento = 0.10 
else:
    descuento = 0.10
    
valor_final = compra *(1-descuento)

print(f"El descuento aplicado es {descuento * 100:.0f}%")
print(f"Total a pagar: ${valor_final:,.2f}")