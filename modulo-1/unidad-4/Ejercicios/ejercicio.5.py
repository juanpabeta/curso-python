try:
    edad = int(input("Ingrese su edad: "))
except ValueError:
    print("Debes ingresar un número")
    
try: 
    edad = int(input("Ingrese su edad: "))
except ValueError: 
    print("Debes ingreasar un número")
except TypeError:
    print("Tipo de dato invalido")
except Exception as e:
    print(f"Ejecución fallida ")    
    
try: 
    edad = int(input("Ingrese su edad: "))
except ValueError: 
    print("Debes ingreasar un número entero")
else:
    print("La ejecución dio un resultado positivo(Else)")
finally:
    print("La ejecución finalizó")