from domain.exceptions import EdadNegativaError


# Modelo de dominio

class Usuario:

    def __init__(self, nombre: str, edad: int):
        if edad < 0:
            raise EdadNegativaError("La edad no puede ser negativa.")

        self.nombre = nombre
        self.edad = edad
