
"""Actividad Final

        -Convertidor de medidas(monedas,distancia,temperatura)
        1.Realizar el convertidor de temperatura
        2.Realizar el convertidor de distancia
        3.Realizar el convertidor de divisas
        4.Realizar un menú principal para seleccionar el tipo de conversor
        5.Imprimir el resultado de la conversión 
        """

#Conversor de temperatura

def convertir_temperatura(valor:float,desde:str,hacia:str)-> float:
        desde = desde.strip().upper()
        hacia = hacia.strip().upper()
            
    #C -> F    
        if desde == 'C' and hacia == 'F':
            return(valor * 1.8)+32         
    #F -> C    
        if desde == 'F' and hacia == 'C':
            return(valor -32)/1.8            
    #C -> K    
        if desde == 'C' and hacia == 'K':
            return valor + 273.15            
    #K -> C    
        if desde == 'K' and hacia == 'C':
            return valor - 273.15            
    #K -> F    
        if desde == 'K' and hacia == 'F':
            return ((valor - 273.15) * 1.8) + 32
    #F -> K    
        if desde == 'F' and hacia == 'K':
            return ((valor - 32)/1.8)+273.15
        else:
            print("Ingrese una unidad de temperatura válida.")
            return None
        
#Conversor de distancia

def convertir_longitud(cantidad: float, unidad_origen: str, unidad_destino: str) -> float:

    #convertir a mayusculas y eliminar espacios
    unidad_origen = unidad_origen.strip().upper()
    unidad_destino = unidad_destino.strip().upper()
    
    metros = 0.0

    #  Parte 1: convertir desde cualquier unidad a metros 
    # mm -> m (dividir entre 1000)
    if unidad_origen == "MM":
        metros = cantidad / 1000
    # cm -> m (dividir entre 100)
    elif unidad_origen == "CM":
        metros = cantidad / 100
    # dm -> m (dividir entre 10)
    elif unidad_origen == "DM":
        metros = cantidad / 10
    # m -> m (ya está en metros)
    elif unidad_origen == "M":
        metros = cantidad
    # dam -> m (multiplicar por 10)
    elif unidad_origen == "DAM":
        metros = cantidad * 10
    # hm -> m (multiplicar por 100)
    elif unidad_origen == "HM":
        metros = cantidad * 100
    # km -> m (multiplicar por 1000)
    elif unidad_origen == "KM":
        metros = cantidad * 1000
    else:
        print("Ingrese una unidad de longitud válida.")
        return None

    # Parte 2: convertir desde metros a cualquier unidad
    # m -> mm (multiplicar por 1000)
    if unidad_destino == "MM":
        return metros * 1000
    # m -> cm (multiplicar por 100)
    elif unidad_destino == "CM":
        return metros * 100
    # m -> dm (multiplicar por 10)
    elif unidad_destino == "DM":
        return metros * 10
    # m -> m (ya está en metros)
    elif unidad_destino == "M":
        return metros
    # m -> dam (dividir entre 10)
    elif unidad_destino == "DAM":
        return metros / 10
    # m -> hm (dividir entre 100)
    elif unidad_destino == "HM":
        return metros / 100
    # m -> km (dividir entre 1000)
    elif unidad_destino == "KM":
        return metros / 1000
    else:
        print("Ingrese una unidad de longitud válida.")
        return None

#Conversor de divisas

def convertir_divisas(cantidad: float, moneda_origen: str, moneda_destino: str) -> float:
    moneda_origen = moneda_origen.strip().upper()
    moneda_destino = moneda_destino.strip().upper()
    
    # Tasas de conversión basadas en el Dolar estadounidense (USD)
    # USD -> EUR
    if moneda_origen == "USD" and moneda_destino == "EUR":
        return cantidad * 0.85
    # USD -> GBP
    elif moneda_origen == "USD" and moneda_destino == "GBP":
        return cantidad * 0.75
    # USD -> JPY
    elif moneda_origen == "USD" and moneda_destino == "JPY":
        return cantidad * 110.0
    # USD -> COP
    elif moneda_origen == "USD" and moneda_destino == "COP":
        return cantidad * 3800.0
    # EUR -> USD
    elif moneda_origen == "EUR" and moneda_destino == "USD":
        return cantidad / 0.85
    # GBP -> USD
    elif moneda_origen == "GBP" and moneda_destino == "USD":
        return cantidad / 0.75
    # JPY -> USD
    elif moneda_origen == "JPY" and moneda_destino == "USD":
        return cantidad / 110.0
    # COP -> USD
    elif moneda_origen == "COP" and moneda_destino == "USD":
        return cantidad / 3800.0
    else:
        print("Ingrese una moneda válida.")
        return None

# Menú principal
def menu():
    print("Seleccione el tipo de conversor:")
    print("1. Conversor de Temperatura")
    print("2. Conversor de Longitud")
    print("3. Conversor de Divisa")
    opcion = input("Ingrese el número de la opción deseada: ")
    
    #Conversor de temperatura
    if opcion == '1':
        valor = float(input("Ingrese el valor a convertir: "))
        desde = input("Ingrese la unidad de origen (C, F, K): ")
        hacia = input("Ingrese la unidad de destino (C, F, K): ")
        resultado = convertir_temperatura(valor, desde, hacia)
        if resultado is not None:
            print(f"{valor:.0f} {desde.upper()}° son {resultado:.2f} {hacia.upper()}°")
    
    #Conversor de longitud
    elif opcion == '2':
        cantidad = float(input("Ingrese la cantidad a convertir: "))
        unidad_origen = input("Ingrese la unidad de origen (MM, CM, DM, M, DAM, HM, KM): ")
        unidad_destino = input("Ingrese la unidad de destino (MM, CM, DM, M, DAM, HM, KM): ")
        resultado = convertir_longitud(cantidad, unidad_origen, unidad_destino)
        if resultado is not None:
            print(f"{cantidad:.0f} {unidad_origen.upper()} son {resultado:.2f} {unidad_destino.upper()}")
        
    #Conversor de moneda
    elif opcion == '3':
        cantidad = float(input("Ingrese la cantidad a convertir: "))
        moneda_origen = input("Ingrese la divisa de origen (USD, EUR, GBP, JPY, COP): ")
        moneda_destino = input("Ingrese la divisa de destino (USD, EUR, GBP, JPY, COP): ")
        resultado = convertir_divisas(cantidad, moneda_origen, moneda_destino)
        if resultado is not None:
            print(f"{cantidad:.0f} {moneda_origen.upper()} son {resultado:.2f} {moneda_destino.upper()}")
            
    else:
        print("Opción no válida.")
        
if __name__ == "__main__":
    menu()