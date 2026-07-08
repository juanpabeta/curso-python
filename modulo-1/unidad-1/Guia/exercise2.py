#Programa que determina el valor de una compra con el 10% de descuento

valor_Compra = int(input("Ingrese el valor de la compra: $"))

total_Pagar = valor_Compra
descuento = 0

if total_Pagar >= 100000:
    descuento = total_Pagar*10/100
    valor_Compra -= descuento
    
    print(f"Valor total de la compra con el descuento del 10% es de: {valor_Compra} ")   
    
    
else:
    print(f"El valor de total de la compra sin el descuento del 10% es de: {valor_Compra}")