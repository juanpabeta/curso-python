from fastapi import FastAPI, HTTPException #Framework para crear APIs y manejar errores HTTP
from pydantic import BaseModel, Field #Validar datos de entrada
from typing import List #Para indicar que una función devuelve una lista de objetos

app = FastAPI()

tareas = []
contador_id = 1

class TareaCreate(BaseModel):
    titulo:str = Field(..., min_length=3)
    descripcion: str = Field(..., min_length=5)
    completada: bool = False

class Tarea(TareaCreate):
    id: int

@app.get("/tareas", response_model=List[Tarea])
def obtener_tareas():
    return tareas

@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: TareaCreate):
    global contador_id
    nueva_tarea = Tarea(id=contador_id, **tarea.dict())
    tareas.append(nueva_tarea)
    contador_id += 1
    return nueva_tarea

@app.put("/tareas/{id}", response_model=Tarea)
def actualizar_tarea(id: int, tarea: TareaCreate):
    if id > len(tareas) or id <= 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    tarea_actualizada = Tarea(id= id, **tarea.dict())
    tareas[id - 1] = tarea_actualizada
    return tarea_actualizada 

@app.delete("/tareas/{id}")
def eliminar_tarea(id: int):
    if id > len(tareas) or id <= 0:
        raise HTTPException (status_code=404, detail="Tarea no encontrada")
    return tareas.pop(id - 1)

