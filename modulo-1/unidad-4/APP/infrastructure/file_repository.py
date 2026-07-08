import csv
from domain.exceptions import (
    LineaCorruptaError,
    ArchivoVacioError,
    EdadInvalidaError
)

from domain.models import Usuario

class FileRepository:
    def __init__(self, path: str):
        self.path = path
        
    def read_users(self):
        usuarios = []
        
        try:
            with open(self.path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                
                if reader.fieldnames is None:
                    raise ArchivoVacioError("El archivo esta vacio")
                for numero_linea, row in enumerate(reader, start=2):
                    try:
                        if row is None:
                            raise LineaCorruptaError(f"Línea corrupta en linea {numero_linea}")
                        
                        nombre = (row.get("nombre") or "").strip()
                        edad_str = (row.get("edad") or "").strip()
                        
                        if not nombre or not edad_str:
                            raise LineaCorruptaError(f"Línea corrupta en linea {numero_linea}")
                        
                        if not edad_str.isdigit():
                            raise EdadInvalidaError(f"Edad invalida en la linea: {numero_linea}")
                        
                        edad = int(edad_str)
                        
                        usuario = Usuario(nombre, edad)
                        usuarios.append(usuario)
                        
                    except ValueError:
                        raise LineaCorruptaError
                
                if not usuarios:
                    raise ArchivoVacioError("El archivo no contiene usuarios.")
        
        except FileNotFoundError:
            raise FileNotFoundError("El archivo no existe")
        except PermissionError:
            raise PermissionError("Permisos insuficientes para leer/gestionar el archivo")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                "utf-8",
                b"",
                0,
                1,
                "Encoding incorrecto"
            )
        return usuarios