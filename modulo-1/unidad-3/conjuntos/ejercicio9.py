"""
Enunciado

Desarrolle un programa en Python que permita comparar los productos disponibles en dos tiendas.

El sistema debe solicitar por teclado los nombres de los productos de la "Tienda A" y la "Tienda B", almacenándolos en estructuras de tipo set[str].

Implemente "todas las funciones necesarias con tipado fuerte (type hints)", incluyendo:

* Una función para leer los productos por teclado
* Una función que reciba ambos conjuntos y retorne:

  * La "unión"
  * La "intersección"
  * La "diferencia" (productos exclusivos de la Tienda A)

Finalmente, el programa principal debe invocar las funciones y mostrar los resultados obtenidos.

"""
from typing import Set

def leer_productos_teclado(nombre_tienda:str) -> set[str]:
    productos = set()
    
    print(f"\n Ingrese los productos de {nombre_tienda} (escriba 'salir' para finalizar) ")

    while True:
        producto = input("> ")
        
        if producto == "salir":
            break
        if producto:
            productos.add(producto)
            
    return productos        

def operaciones_producto(tienda_a:Set[str],tienda_b:Set[str])-> Set[str]:
    union = tienda_a | tienda_b
    interseccion = tienda_a & tienda_b
    diferencia = tienda_a - tienda_b
    return union,interseccion,diferencia

def main()-> None:
    tienda_a = leer_productos_teclado("Tienda A")
    tienda_b = leer_productos_teclado("Tienda B")
    
    union,interseccion,diferencia = operaciones_producto(tienda_a,tienda_b)
    
    print(f"\n Unión: {union}")
    print(f"\n Intersección: {interseccion}")
    print(f"\n Diferencia tienda A:{diferencia}")
    
if __name__ == "__main__":
    main()