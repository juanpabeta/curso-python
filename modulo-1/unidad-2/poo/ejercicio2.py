#Desarrolle un programa que permita introducir 3 atributos de un automóvil y que su comportamiento sea el mostrar la información del automóvil.

class automovil:
    
    def __init__(self,color:str,marca:str,modelo:str):
        self.__color = color
        self.__marca = marca
        self.__modelo = modelo
        
    @property
    def color(self):
        return self.__color  
    @color.setter
    def color(self, nuevo_color):
        if isinstance(nuevo_color,(str)):
            self.__color = nuevo_color,
    @property
    def marca(self):
        return self.__marca  
    @marca.setter
    def marca(self, nueva_marca):
        if isinstance(nueva_marca,(str)):
            self.__color = nueva_marca,
    @property
    def modelo(self):
        return self.__modelo  
    @modelo.setter
    def modelo(self, modelo):
        if isinstance(modelo,(str)):
            self.color = modelo
            
    def mostrar_info(self):
        print(f"Color: {self.__color}")
        print(f"Marca: {self.__marca}")
        print(f"Modelo:{self.__modelo} ")

def main():
    print("\n*** SISTEMA DE REGISTRO DE LIBROS ***") 
    
    automovil1 = automovil("Azul", "Toyota","Corolla")
    print("Información del automovil")
    automovil1.mostrar_info()
    print("---------------")
    automovil1.color = "Rojo"
    print("Nuevo Color: ", automovil1.color)   

if __name__ == "__main__":
    main()
    
