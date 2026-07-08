# main.py
from models.rol import RolRegular, RolVIP, RolEmpresarial
from models.cliente import Cliente
from services.cliente_servicio import ClienteServicio


def poblar_datos_iniciales(servicio: ClienteServicio) -> None:
    """
    Crea algunos clientes de ejemplo para probar el sistema.
    """
    c1 = Cliente(
        id_interno=1,
        nombre="Luis Pérez",
        documento="123456789",
        email="luis@example.com",
        telefono="3001234567",
        direccion="Calle 123 # 45-67",
        fecha_registro="2025-01-10",
        estado="Activo",
        rol=RolRegular(),
    )

    c2 = Cliente(
        id_interno=2,
        nombre="Ana Gómez",
        documento="987654321",
        email="ana@example.com",
        telefono="3109876543",
        direccion="Carrera 7 # 80-20",
        fecha_registro="2025-01-11",
        estado="Activo",
        rol=RolVIP(),
    )

    c3 = Cliente(
        id_interno=3,
        nombre="Empresa XYZ",
        documento="900123456-7",  # NIT
        email="contacto@xyz.com",
        telefono="6011234567",
        direccion="Zona industrial 45",
        fecha_registro="2025-01-12",
        estado="Activo",
        rol=RolEmpresarial(),
    )

    servicio.registrar_cliente(c1)
    servicio.registrar_cliente(c2)
    servicio.registrar_cliente(c3)


def main() -> None:
    servicio = ClienteServicio()
    poblar_datos_iniciales(servicio)

    print("=== LISTA INICIAL DE CLIENTES ===")
    for cliente in servicio.listar_clientes():
        cliente.presentar()

    # Registrar acciones
    servicio.registrar_accion(1, "Consultó su saldo.")
    servicio.registrar_accion(2, "Realizó una compra por 100000.")
    servicio.registrar_accion(3, "Solicitó estado de cuenta.")

    # Calcular monto con reglas de rol
    monto_original = 100000
    monto_vip = servicio.calcular_monto_con_regla(2, monto_original)

    print("\n=== REGLAS DE NEGOCIO (POLIMORFISMO) ===")
    print(f"Monto original: {monto_original}")
    print(f"Monto a pagar Cliente VIP (ID=2): {monto_vip}")

    # Mostrar historial de acciones de un cliente
    print("\n=== HISTORIAL DE ACCIONES CLIENTE VIP (ID=2) ===")
    cliente_vip = servicio.obtener_cliente(2)
    if cliente_vip:
        cliente_vip.mostrar_historial()

    print("\n=== HISTORIAL DE ACCIONES CLIENTE EMPRESARIAL (ID=3) ===")
    cliente_emp = servicio.obtener_cliente(3)
    if cliente_emp:
        cliente_emp.mostrar_historial()

    print("\nPrograma finalizado.")


if __name__ == "__main__":
    main()
