#Programa que indica la cantidad de dinero e indica cuantos hay de cada uno

#Valida la cantidad de dinero
cantidad_dinero = int(input("Ingrese cuanto dinero tiene en pesos colombianos: $"))

#Operacion para calcular la cantidad de billetes

billetes_50Mil,billetes_20Mil = 0,0
billetes_10Mil,billetes_5Mil = 0,0
billetes_2Mil,billetes_Mil = 0,0
#Billetes de 50Mil Pesos

if cantidad_dinero >= 50000:
    billetes_50Mil = cantidad_dinero//50000
    cantidad_dinero = cantidad_dinero %50000

#Billetes de 20Mil Pesos
if cantidad_dinero >= 20000:
    billetes_20Mil = cantidad_dinero//20000
    cantidad_dinero = cantidad_dinero %20000

#Billetes de 10Mil Pesos
if cantidad_dinero >= 10000:
    billetes_10Mil = cantidad_dinero//10000
    cantidad_dinero = cantidad_dinero %10000


#Billetes de 5Mil Pesos
if cantidad_dinero >= 5000:
    billetes_5Mil = cantidad_dinero//5000
    cantidad_dinero = cantidad_dinero %5000

#Billetes de 2Mil Pesos
if cantidad_dinero >= 2000:
    billetes_2Mil = cantidad_dinero//2000
    cantidad_dinero = cantidad_dinero %2000

#Billetes de Mil Pesos
if cantidad_dinero >= 1000:
    billetes_Mil = cantidad_dinero//1000
    cantidad_dinero = cantidad_dinero %1000

print("💵--Cantidad de Billetes-- 💵: ")
if billetes_50Mil > 0:
    print(f"Billetes de 50.000: {billetes_50Mil} ")
if billetes_20Mil > 0:
    print(f"Billetes de 20.000: {billetes_20Mil} ")
if billetes_10Mil > 0:
    print(f"Billetes de 10.000: {billetes_10Mil} ")
if billetes_5Mil > 0:
    print(f"Billetes de 5.000: {billetes_5Mil} ")
if billetes_2Mil > 0:
    print(f"Billetes de 2.000: {billetes_2Mil} ")
if billetes_Mil > 0:
    print(f"Billetes de 1.000: {billetes_Mil} ")
 

    
        
    

