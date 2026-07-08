from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
from models import Base, Estudiante
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/estudiantes")
def crear_estudiante(nombre:str,db: Session = Depends(get_db)):
    estudiante_existe = db.query(Estudiante).filter(Estudiante.nombre == nombre).first()  
    
    if estudiante_existe:
        raise HTTPException(status_code= 400,detail= "Este estudiante ya existe")
    nuevo_estudiante = Estudiante(nombre = nombre,notas = [])
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

@app.get("/estudiantes")
def listar_estudiante(db:Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).all()
    
    resultado = []
    for e in estudiantes:
        if e.notas == None:
            notas = []
        else:
            notas = e.notas
        
        if len(notas) > 0:
            promedio = sum(notas)/len(notas)
        else:
            promedio = 0
        
        resultado.append({
            "id": e.id,
            "nombre":e.nombre,
            "notas":notas,
            "promedio":promedio            
        } )
    return resultado    

@app.put("/estudiantes/{id}")
def remplazar_notas(id: int,nuevas_notas:List[float],db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()  
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.notas = nuevas_notas
    db.commit()
    
    return{"Mensaje":"Nota remplazada exitosamente"}

@app.patch("/estudiantes/{id}")
def agregar_nota(id:int,nota:float,db:Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()  
    
    if not estudiante:
        return{"Error": "No existe"}
    
    if estudiante is None:
        estudiante.notas = []
    
    estudiante.notas.append(nota)
    db.commit()
    
    return{"Mensaje":"Nota creada exitosamente"}

@app.delete("/estudiantes/{id}")
def eliminar_estudiante(id:int,db:Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()  
    
    if not estudiante:
        return{"Error": "No existe"}
    
    db.delete(estudiante)
    db.commit()
    return {"mensaje":"Estudiante eliminado correctamnete"}
    