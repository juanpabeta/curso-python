# servicio/cliente_servicio.py
from typing import Dict, Optional, List
from models.cliente import Cliente
from models.accion import Accion
from models.rol import RolEmpresarial
import re


class ClienteServicio:
    """
    Servicio de dominio para gestionar clientes.
    Aplica SRP: esta clase se encarga de las operaciones sobre clientes,
    no de la interacción con el usuario.
    """

    def __init__(self) -> None:
        self._clientes: Dict[int, Cliente] = {}

    def registrar_cliente(self, cliente: Cliente) -> None:
        if cliente.id_interno in self._clientes:
            raise ValueError("Ya existe un cliente con ese ID interno.")
        self._clientes[cliente.id_interno] = cliente

    def obtener_cliente(self, id_interno: int) -> Optional[Cliente]:
        return self._clientes.get(id_interno)

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes.values())

    def registrar_accion(self, id_interno: int, descripcion: str) -> None:
        cliente = self.obtener_cliente(id_interno)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")

        # Regla especial para empresarial: validar NIT
        if isinstance(cliente.rol, RolEmpresarial):
            if not self._validar_nit(cliente.documento):
                raise ValueError("NIT empresarial no válido. No se registra la acción.")

        cliente.agregar_accion(Accion(descripcion))

    def calcular_monto_con_regla(self, id_interno: int, monto: float) -> float:
        cliente = self.obtener_cliente(id_interno)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        return cliente.calcular_monto_final(monto)

    @staticmethod
    def _validar_nit(nit: str) -> bool:
        """
        Validación sencilla de NIT:
        - Solo dígitos y/o guión
        - Longitud mínima y máxima razonable
        """
        nit_limpio = nit.strip()
        if not re.fullmatch(r"[0-9\-]+", nit_limpio):
            return False
        return 7 <= len(nit_limpio) <= 15
