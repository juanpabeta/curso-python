
from repositories.estudiante_repository_csv import EstudianteRepositoryCSV
from services.estudiante_service import EstudianteService

if __name__ == "__main__":
    repo = EstudianteRepositoryCSV()
    service = EstudianteService(repo)

    service.registrar_estudiante(1, "Ana", 20)
    service.registrar_estudiante(2, "Luis", 22)
    service.registrar_estudiante(3, "Carlos", 24)
    service.registrar_estudiante(4, "Juan", 19)
    service.registrar_estudiante(5, "Andres", 11)
    service.registrar_estudiante(6, "Pablo", 54)
    service.registrar_estudiante(7, "Cristina", 40)
    service.registrar_estudiante(8, "Anny", 9)
    service.registrar_estudiante(9, "Fernando", 33)
    service.registrar_estudiante(10, "Pedro", 34)

    service.mostrar_estudiantes()
 
    service.mostrar_estudiantes()
    
    