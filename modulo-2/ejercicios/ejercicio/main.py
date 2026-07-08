from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

import models, schemas
from database import engine, SessionLocal

# Crear las tablas al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Crear tarea
@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Task).filter(models.Task.title == task.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="La tarea ya existe")
    
    new_task = models.Task(**task.model_dump()) # model_dump() es el nuevo .dict()
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 2. Listar todas las tareas
@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# 3. Listar tarea por ID
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea inexistente")
    return task

# 4. Actualizar tarea (PATCH)
@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# 5. Eliminar tarea
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(task)
    db.commit()
    return {"message": "Tarea eliminada correctamente"}

# 6. Buscar tareas (Filtro por texto)
@app.get("/tasks/search/", response_model=list[schemas.TaskResponse])
def search_task(q: str, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(
        models.Task.title.ilike(f"%{q}%")
    ).all()
    return tasks

# 7. Listar con paginación
@app.get("/tasks/paginated/", response_model=list[schemas.TaskResponse])
def get_tasks_paginated(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return db.query(models.Task).offset(skip).limit(limit).all()

# 8. Estadísticas
@app.get("/tasks/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(models.Task).count()
    pendientes = db.query(models.Task).filter(models.Task.status == "pendiente").count()
    completadas = db.query(models.Task).filter(models.Task.status == "completada").count()
    return {
        "total": total,
        "pendientes": pendientes,
        "completadas": completadas
    }