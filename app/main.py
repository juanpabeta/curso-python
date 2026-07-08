from infrastructure.file_repository import FileRepository
from application.user_service import UserService
from domain.exceptions import (
    ArchivoVacioError,
    LineaCorruptaError,
    EdadInvalidaError,
    EdadNegativaError,
)


def main():

    repo = FileRepository("app/usuarios.csv")
    service = UserService(repo)

    try:
        usuarios = service.procesar()

    except FileNotFoundError as e:
        print(f"[ERROR SISTEMA] {e}")

    except PermissionError as e:
        print(f"[ERROR PERMISOS] {e}")

    except UnicodeDecodeError:
        print("[ERROR ENCODING] El archivo no está en UTF-8.")

    except ArchivoVacioError as e:
        print(f"[ERROR DATOS] {e}")

    except LineaCorruptaError as e:
        print(f"[ERROR FORMATO] {e}")

    except EdadInvalidaError as e:
        print(f"[ERROR VALIDACIÓN] {e}")

    except EdadNegativaError as e:
        print(f"[ERROR NEGOCIO] {e}")

    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")

    else:
        print("Usuarios cargados correctamente:")
        for u in usuarios:
            print(f"{u.nombre} - {u.edad}")

    finally:
        print("Proceso finalizado.")


if __name__ == "__main__":
    main()
