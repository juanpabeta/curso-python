"""
class Libro:
    # método constructor
    def __init__(self, titulo, autor, isbn, precio):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.precio = precio
    

libro1 = Libro("Matemáticas", "Luis Molero", "21654987-98", 321654)
print(libro1.titulo)
print(libro1.autor)

"""
"""
# ERROR en Encapsulamiento

class Libro:
    def __init__(self, titulo, precio):
        self.titulo = titulo
        self.precio = precio

libro2 = Libro("Ciencias", 100)

libro2.precio = 250  # => ERROR
print(libro2.precio)

"""
"""
# Encapsulamiento correcto

class Libro:
    def __init__(self, titulo, precio):
        self.__titulo = titulo
        self.__precio = precio

    def get_precio(self):
        return self.__precio
    
    def set_precio(self, nuevo_precio):
        # validar el precio
        if isinstance(nuevo_precio, (int, float)) and nuevo_precio > 0:
            self.__precio = nuevo_precio
        else:
            print("ERROR al ingresar el precio del libro")
        
    def mostrar_info(self):
        print(f"Título: {self.__titulo}")
        print(f"Precio: {self.__precio}")

def main():
    print("\n*** SISTEMA DE REGISTRO DE LIBROS ***") 
    
    book1 = Libro("Biología", 1000)
    
    print("Información del libro")
    
    # Mostrar información actual del objeto/instancia/ejemplar
    book1.mostrar_info()
    
    # mostrar el precion actual
    print("Precio actual:", book1.get_precio())
    
    # Cambiar el precio actual del libro (ERROR)
    book1.set_precio(-1500)
    
    # Cambiar nuevamente el precio actual del libro
    book1.set_precio(2000)
    
    print("Nuevo precio: ", book1.get_precio())
    
    print("\n Software IA finalizado")

if __name__ == "__main__":
    main()

"""

class Libro:
    
    def __init__(self, titulo, precio):
        self.__titulo = titulo
        self.__precio = precio
        
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        if isinstance(nuevo_precio, (int, float)) and nuevo_precio > 0:
            self.__precio = nuevo_precio
        else:
            print("ERROR al ingresar el precio del libro")
    
    def mostrar_info(self):
        print(f"Título: {self.__titulo}")
        print(f"Precio: {self.__precio}")
    
def main():
    print("\n*** SISTEMA DE REGISTRO DE LIBROS ***") 
    
    book1 = Libro("Biología", 1000)
    
    print("Información del libro")
    
    # Mostrar información actual del objeto/instancia/ejemplar
    book1.mostrar_info()
    
    # mostrar el precio actual
    print("Precio actual:", book1.precio)
    
    # Cambiar el precio actual del libro (ERROR)
    book1.precio = 2000
    
    print("Nuevo precio: ", book1.precio)
    
    print("\n Software IA finalizado")

if __name__ == "__main__":
    main()
    

