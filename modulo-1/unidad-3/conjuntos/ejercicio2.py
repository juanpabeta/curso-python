

from typing import List

def eliminar_duplicados(numeros:List[int])->List[int]:
    if not isinstance(numeros,list):
        raise TypeError("se esperaba una Lista de números")
    
    if not all(isinstance(n,int)for n in numeros):
        raise ValueError("Todos los elementos dentro de lista deben ser números enteros")
    
    return sorted(set(numeros))

def main()-> None:
    numeros = [1,2,4,7,5,8,5,1,2,4,6,8,9,9,9,19]
    print("Lista original: ",numeros)

    try:
        resultado = eliminar_duplicados(numeros)
        print(f"Sin duplicados: {resultado}")
    except(TypeError,ValueError) as error:
        print(f"Error: {error}")    

if __name__ == "__main__":
    main()