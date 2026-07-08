from abc import ABC, abstractmethod
from typing import List

class Persona(ABC):
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad    
        

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str) -> None:
        if isinstance(valor,str) and valor.strip():
            self._nombre = valor.strip()
        else:
            raise ValueError("El nombre debe ser una cadena no vacía.")
    
    @abstractmethod 
    def presentar(self)-> None:
        pass
    
class Cliente(Persona):
    def presentar(self):
        print(f"El cliente {self.nombre} esta en el restaurante")
        
class Empleado(Persona):
    @abstractmethod
    def trabajar(self) ->None:
        pass

class Mesero(Empleado):
    def presentar(self):
        print(f"El mesero {self.nombre} esta listo para atender")

class Chef(Empleado):
    def presentar(self):
        print(f"El Chef {self.nombre} esta en la cocina")
    
    def trabajar(self):
        print(f"El Chef {self.nombre} esta cocinando una delicioso platillo")