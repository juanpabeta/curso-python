# modelo/accion.py
from datetime import datetime


class Accion:
    """
    Representa una acción realizada por un cliente:
    - descripción (texto)
    - fecha y hora exacta
    """

    def __init__(self, descripcion: str) -> None:
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción de la acción no puede estar vacía.")
        self._descripcion = descripcion.strip()
        self._fecha_hora = datetime.now()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def fecha_hora(self) -> datetime:
        return self._fecha_hora

    def __str__(self) -> str:
        fecha_str = self._fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{fecha_str}] {self.descripcion}"
