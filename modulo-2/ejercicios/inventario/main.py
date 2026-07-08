from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Base, Producto
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos")
def registrar_producto(nombre:str,descripcion:str,stock:int,db: Session = Depends(get_db)):
    producto_existe = db.query(Producto).filter(Producto.nombre == nombre).first()  
    
    if producto_existe:
        raise HTTPException(status_code= 400,detail= "Este producto ya existe")
    nuevo_producto = Producto( nombre= nombre,descripcion = descripcion,stock = stock)
    
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@app.get("/productos")
def consultar_stock(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    
    stock = []
    for producto in productos:
        stock.append({
            "id": producto.id,
            "nombre":producto.nombre,
            "descripcion":producto.descripcion,
            "stock":producto.stock            
        } )
    return stock


@app.put("/productos/{id}")
def remplazar_notas(id: int,nuevo_stock:int,db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()  
    
    if not producto:
        raise HTTPException(status_code=400, detail="Producto no encontrado")
    
    producto.stock = nuevo_stock
    db.commit()
    
    return{"Mensaje":"Stock actualizado con exito"}
 
#@app.patch("/productos/{id}")
