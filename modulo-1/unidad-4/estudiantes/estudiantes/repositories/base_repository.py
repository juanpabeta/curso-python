from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def agregar(self,entidad):
        pass
    
    @abstractmethod
    def obtener_por_id(self,id):
        pass
    
    @abstractmethod
    def listar(self):
        pass
    
    @abstractmethod
    def eliminar(self,id):
        pass
    