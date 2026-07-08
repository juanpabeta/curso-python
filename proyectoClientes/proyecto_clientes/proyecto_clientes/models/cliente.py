# modelo/cliente.py
from typing import List
from .persona import Persona
from .rol import Rol
from .accion import Accion


class Cliente(Persona):
    """
    Modelo de Cliente del sistema.

    Datos básicos:
    - id_interno (int)
    - documento (cédula o NIT)
    - email
    - teléfono
    - dirección
    - fecha_registro (str o datetime, aquí usaremos str simple)
    - estado (Activo/Inactivo)
    - rol (Regular, VIP, Empresarial)
    - historial de acciones
    """

    def __init__(
        self,
        id_interno: int,
        nombre: str,
        documento: str,
        email: str,
        telefono: str,
        direccion: str,
        fecha_registro: str,
        estado: str,
        rol: Rol,
    ) -> None:
        super().__init__(nombre, documento)
        # Inicializar directamente los atributos privados para evitar problemas con getters
        if isinstance(id_interno, int) and id_interno > 0:
            self._id_interno = id_interno
        else:
            raise ValueError("El ID interno debe ser un entero positivo.")
        
        if isinstance(email, str) and "@" in email:
            partes = email.split("@")
            if len(partes) == 2 and "." in partes[1]:
                self._email = email.strip()
            else:
                raise ValueError("El email no es válido.")
        else:
            raise ValueError("El email no es válido.")
        
        valor_limpio = telefono.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if valor_limpio.isdigit() and 7 <= len(valor_limpio) <= 15:
            self._telefono = valor_limpio
        else:
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos.")
        
        if isinstance(direccion, str) and direccion.strip():
            self._direccion = direccion.strip()
        else:
            raise ValueError("La dirección no puede estar vacía.")
        
        if isinstance(fecha_registro, str) and fecha_registro.strip():
            self._fecha_registro = fecha_registro.strip()
        else:
            raise ValueError("La fecha de registro no puede estar vacía.")
        
        valor_normalizado = estado.strip().lower()
        if valor_normalizado in ("activo", "inactivo"):
            self._estado = valor_normalizado
        else:
            raise ValueError("El estado debe ser 'Activo' o 'Inactivo'.")
        
        if isinstance(rol, Rol):
            self._rol = rol
        else:
            raise ValueError("El rol debe ser una instancia de una clase que implemente Rol.")
        
        self._historial: List[Accion] = []

    # Encapsulamiento y validaciones

    @property
    def id_interno(self) -> int:
        return self._id_interno

    @id_interno.setter
    def id_interno(self, valor: int) -> None:
        if isinstance(valor, int) and valor > 0:
            self._id_interno = valor
        else:
            raise ValueError("El ID interno debe ser un entero positivo.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if isinstance(valor, str) and "@" in valor:
            partes = valor.split("@")
            if len(partes) == 2 and "." in partes[1]:
                self._email = valor.strip()
            else:
                raise ValueError("El email no es válido.")
        else:
            raise ValueError("El email no es válido.")

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        valor_limpio = valor.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if valor_limpio.isdigit() and 7 <= len(valor_limpio) <= 15:
            self._telefono = valor_limpio
        else:
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos.")

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, valor: str) -> None:
        if isinstance(valor, str) and valor.strip():
            self._direccion = valor.strip()
        else:
            raise ValueError("La dirección no puede estar vacía.")

    @property
    def fecha_registro(self) -> str:
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor: str) -> None:
        # Para simplificar, se valida que no esté vacía.
        if isinstance(valor, str) and valor.strip():
            self._fecha_registro = valor.strip()
        else:
            raise ValueError("La fecha de registro no puede estar vacía.")

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        valor_normalizado = valor.strip().lower()
        if valor_normalizado in ("activo", "inactivo"):
            self._estado = valor_normalizado
        else:
            raise ValueError("El estado debe ser 'Activo' o 'Inactivo'.")

    @property
    def rol(self) -> Rol:
        return self._rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if isinstance(valor, Rol):
            self._rol = valor
        else:
            raise ValueError("El rol debe ser una instancia de una clase que implemente Rol.")

    @property
    def historial(self) -> List[Accion]:
        return list(self._historial)

    def agregar_accion(self, accion: Accion) -> None:
        self._historial.append(accion)

    def calcular_monto_final(self, monto: float) -> float:
        """
        Aplica polimorfismo: delega en el rol la regla de negocio.
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        return self.rol.aplicar_regla(monto)

    def presentar(self) -> None:
        print(f"Cliente {self.nombre} (Rol: {self.rol.descripcion()})")

    def mostrar_historial(self) -> None:
        if not self._historial:
            print("El cliente no tiene acciones registradas.")
            return
        print(f"Historial de acciones de {self.nombre}:")
        for accion in self._historial:
            print(f"  - {accion}")
