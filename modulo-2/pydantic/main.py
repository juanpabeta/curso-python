from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import CreateTask,UpdateTask,ReponseTask
from database import tasks
from typing import List

app = FastAPI

@app.post("/tasks",response_model=ReponseTask)

def create_task(task:CreateTask):
    task_new ={
        "id":len(tasks)+1,
        "titulo":task.titulo,
        "descripcion":task.descripcion,
        "prioridad":task.prioridad,
        "completada":task.completada
    }
    tasks.append(task_new)
    return JSONResponse(status_code=201,content=task_new)

@app.get("/tasks", response_model=List[ReponseTask])
def listar_tareas():
    return tasks

@app.get("task/{task_id}")
def get_task(task_id:int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    return JSONResponse(
        status_code=404,
        content= {"mensaje": "Tarea no encontrada"}
    )
    
@app.patch("/tasks/{task_id}")
def update_task(task_id:int,dates: UpdateTask):
    for task in task:
        if task["id"] == task_id:
            
            if dates.titulo is not None:
                task["titulo"] = dates.titulo
                
            if dates.descripcion is not None:
                task["descripcion"] = dates.descripcion
            
            if dates.prioridad is not None:
                task["prioridad"] = dates.prioridad
                
            if dates.completada is not None:
                task["completada"] = dates.completada
                
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return tasks.remove()
                
    return JSONResponse(
        status_code=404,
        content= {"mensaje": "Tarea no encontrada"}
    )