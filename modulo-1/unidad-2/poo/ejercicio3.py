from dataclasses import dataclass

@dataclass
class Producto:
    _nombre:str
    _categoria:str
    _codigo_interno:str
    _precio_unitario:float
    _cantidad_inventario:int
    
    @property
    def nombre(self)-> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self,nombre:str)->None:
        if isinstance(nombre,str) and nombre.strip():
            self._nombre = nombre
        else:
            raise ValueError("El nombre debe ser un texto valido")
    
    @property
    def categoria(self)-> str:
        return self._categoria
    
    @categoria.setter 
    def categoria(self,categoria:str)->None:
        if isinstance(categoria,str) and categoria.strip():
            self._nombre = categoria
        else:
            raise ValueError("La categoría debe ser un texto valido")
    @property
    def codigoInterno(self)-> str:
        return self._codigo_interno
    
    @codigoInterno.setter 
    def codigoInterno(self,codigo:str)->None:
        if isinstance(codigo,str) and codigo.strip():
            self._nombre = codigo
        else:
            raise ValueError("El codigo interno debe ser un texto valido")
    @property
    def precioUnitario(self)-> str:
        return self._precio_unitario
    
    @precioUnitario.setter 
    def preciounitario(self,precio:float)->None:
        if isinstance(precio,float) and precio:
            self._nombre = precio
        else:
            raise ValueError("El precio unitario debe ser un numero positivo")
    @property
    def cantidadInventario(self)-> str:
        return self._cantidad_inventario
    
    @cantidadInventario.setter 
    def cantidadInventario(self,inventario:int)->None:
        if isinstance(inventario,int) and inventario:
            self._nombre = inventario
        else:
            raise ValueError("El codigo interno debe ser un texto valido")

    def __repr__(self) -> str:
        return (
            f"Producto Industrial(nombre ='{self._nombre}', categoría ='{self._categoria}', "
            f"codigo interno ='{self._codigo_interno}', precio unitario ={self._precio_unitario},"
            f"cantidad de inventario ='{self._cantidad_inventario}')"
        )

def main()-> None:
    producto1 = Producto("Batman","Juguetería","rt-533-67",85800.0,120)
    
    print("\n ¡¡¡ Informacion del producto !!! \n")
    print(producto1)
    producto1.preciounitario = 150000.0
    producto1.nombre = "goku"
    
    print("\n #### Información actualizada del producto #### \n")
    print(f"{producto1}\n")
    
if __name__ == "__main__":
    main()
