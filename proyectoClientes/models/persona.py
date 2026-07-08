from abc import ABC,abstractmethod

class Persona(ABC):
    def __init__(self,nombre:str,documento:str)-> None:
        if isinstance(nombre,str)and nombre.strip():
            self._nombre = nombre.strip().title()
        else:
            raise ValueError("El nombre no debe ser un texto vacío")
        
    @property
    def nombre(self)-> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self,valor:str) -> None:
        if isinstance(valor,str) and valor.strip():
            self._documento = valor.strip()
        else:
            raise ValueError("el documento no pueede estar vacio")
        
    @abstractmethod
    def presentar(self):
        pass