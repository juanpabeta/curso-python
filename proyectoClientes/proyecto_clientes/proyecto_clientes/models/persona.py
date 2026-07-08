# modelo/persona.py
from abc import ABC, abstractmethod


class Persona(ABC):
    """
    Clase abstracta base para personas del sistema.

    Aplica:
    - Abstracción: no se instancia directamente.
    - Encapsulamiento: atributos privados con getters/setters.
    - SRP: solo modela datos y comportamiento básico de una persona.
    """

    def __init__(self, nombre: str, documento: str) -> None:
        # Inicializar directamente los atributos privados para evitar problemas con getters
        if isinstance(nombre, str) and nombre.strip():
            self._nombre = nombre.strip().title()
        else:
            raise ValueError("El nombre debe ser un texto no vacío.")
        
        if isinstance(documento, str) and documento.strip():
            self._documento = documento.strip()
        else:
            raise ValueError("El documento/identificación no puede estar vacío.")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if isinstance(valor, str) and valor.strip():
            self._nombre = valor.strip().title()
        else:
            raise ValueError("El nombre debe ser un texto no vacío.")

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if isinstance(valor, str) and valor.strip():
            self._documento = valor.strip()
        else:
            raise ValueError("El documento/identificación no puede estar vacío.")

    @abstractmethod
    def presentar(self) -> None:
        """Cada subclase debe definir cómo se presenta."""
        pass

