# modelo/rol.py
from abc import ABC, abstractmethod


class Rol(ABC):
    """
    Interfaz de Rol (cliente regular, VIP, empresarial).

    Open/Closed: para agregar nuevos roles no se modifica código existente,
    se crean nuevas clases que implementen esta interfaz.
    """

    @abstractmethod
    def aplicar_regla(self, monto: float) -> float:
        """Aplica las reglas comerciales según el tipo de cliente."""
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """Descripción legible del rol."""
        pass


class RolRegular(Rol):
    def aplicar_regla(self, monto: float) -> float:
        return monto

    def descripcion(self) -> str:
        return "Cliente Regular"


class RolVIP(Rol):
    def aplicar_regla(self, monto: float) -> float:
        # 10% de descuento
        return round(monto * 0.90, 2)

    def descripcion(self) -> str:
        return "Cliente VIP"


class RolEmpresarial(Rol):
    def aplicar_regla(self, monto: float) -> float:
        # Por ahora no aplica descuento directo
        return monto

    def descripcion(self) -> str:
        return "Cliente Empresarial"
