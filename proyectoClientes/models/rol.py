from abc import ABC,abstractmethod

class Rol(ABC):
    
    @abstractmethod
    def aplicarRegla(self,monto:float) -> float:
        pass
    
    @abstractmethod
    def descripcion(self) -> str:
        pass
    
class RolRegular