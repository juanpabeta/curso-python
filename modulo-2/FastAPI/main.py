from fastapi import FastAPI
from pydantic import BaseModel


class Estudiante(BaseModel):
    nombre: str
    edad: int


app = FastAPI()

estudiantes = {}


@app.get("/")
def inicio():
    return {"mensaje": "API de prueba con FastAPI"}


@app.post("/estudiantes/{id}")
def crear_estudiante(id: int, estudiante: Estudiante):
    estudiantes[id] = estudiante
    return {"mensaje": f"Estudiante {estudiante.nombre} agregado", "data": estudiante}


@app.get("/estudiantes")
def listar_estudiantes():
    return estudiantes


@app.get("/estudiantes/{id}")
def obtener_estudiante(id: int):
    if id in estudiantes:
        return estudiantes[id]
    return {"error": "Estudiante no encontrado"}


@app.put("/estudiantes/{id}")
def actualizar_estudiante(id: int, estudiante: Estudiante):
    estudiantes[id] = estudiante
    return {"mensaje": f"Estudiante {id} actualizado", "data": estudiante}


@app.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int):
    if id in estudiantes:
        del estudiantes[id]
        return {"mensaje": f"Estudiante {id} eliminado"}
    return {"error": "Estudiante no encontrado"}