from domain.exceptions import EdadNegativaError

class Usuario:
    def __init__(self,nombre:str,edad:int)-> None:
        if edad <= 0:
            raise EdadNegativaError("La edad no puede ser cero o menor a cero")
        
        self._nombre = nombre
        self._edad = edad