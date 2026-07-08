from typing import Tuple, List
from dataclasses import dataclass


# =========================
# Excepciones de dominio
# =========================
class ListaEmpleadosVaciaError(Exception):
    pass


# =========================
# Validaciones
# =========================
def _validar_datos_empleado(nombre: str, cargo: str, salario: float) -> None:
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no debe ser un texto vacío")

    if not isinstance(cargo, str) or not cargo.strip():
        raise ValueError("El cargo no debe ser un texto vacío")

    if not isinstance(salario, (int, float)) or salario <= 0:
        raise ValueError("El salario debe ser un número mayor a cero")


# =========================
# Lógica de negocio
# =========================
def registrar_empleado(nombre: str, cargo: str, salario: float) -> Tuple[str, str, float]:
    _validar_datos_empleado(nombre, cargo, salario)

    return (
        nombre.strip().title(),
        cargo.strip().title(),
        float(salario)
    )


# =========================
# Result Pattern
# =========================
@dataclass
class ResultadoRegistro:
    empleados: List[Tuple[str, str, float]]
    errores: List[str]


def registrar_empleados(datos: List[Tuple[str, str, float]]) -> ResultadoRegistro:
    empleados_registrados: List[Tuple[str, str, float]] = []
    errores: List[str] = []

    for nombre, cargo, salario in datos:
        try:
            empleado = registrar_empleado(nombre, cargo, salario)
            empleados_registrados.append(empleado)
        except (ValueError, TypeError) as error:
            errores.append(str(error))

    return ResultadoRegistro(
        empleados=empleados_registrados,
        errores=errores
    )


# =========================
# Presentación
# =========================
def mostrar_empleados(empleados: List[Tuple[str, str, float]]) -> None:
    if not empleados:
        raise ListaEmpleadosVaciaError("No existen registros para mostrar")

    print("\nRegistro histórico de contratos de empleados\n")

    for indice, (nombre, cargo, salario) in enumerate(empleados, start=1):
        print(f"{indice}. {nombre} - {cargo} - ${salario:,.2f}")


# =========================
# Main
# =========================
def main() -> None:
    datos_prueba = [
        ("Ana García", "Ingeniera de Software", 8500),
        ("Luis Pérez", "Analista de Datos", 7200),
        ("Marta León", "Diseñadora UX", 6800)        
    ]

    resultados = registrar_empleados(datos_prueba)

    try:
        mostrar_empleados(resultados.empleados)
    except ListaEmpleadosVaciaError as error:
        print(error)

    if resultados.errores:
        print("\nErrores capturados durante el registro:")
        for error in resultados.errores:
            print(f"- {error}")


if __name__ == "__main__":
    main()
