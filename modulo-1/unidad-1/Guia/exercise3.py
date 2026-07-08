
valor_Compra = float(input("Ingrese el valor de la compra: "))
def descuento()->float:
    if valor_Compra > 100000:
        descuento = valor_Compra*10//100
        return valor_Compra-descuento

print(descuento())
    

