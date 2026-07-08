from models.estudiante import Estudiante


class EstudianteService:
    def __init__(self, repository):
        self.repository = repository

    def registrar_estudiante(self, id, nombre, edad):
        estudiante = Estudiante(id, nombre, edad)
        self.repository.agregar(estudiante)
        print(f"Estudiante registrado: {estudiante}")

    def mostrar_estudiantes(self):
        print("Listado de estudiantes:")
        for est in self.repository.listar():
            print(est)

    def buscar_estudiante(self, id):
        est = self.repository.obtener_por_id(id)
        print(f"Resultado búsqueda: {est}")
        return est

    def eliminar_estudiante(self, id):
        self.repository.eliminar(id)
        print(f"Estudiante con id={id} eliminado.")