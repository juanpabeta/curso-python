from fastapi import FastAPI, HTTPException,status
from typing import List
from schemas import EquipoCreate, EquipoResponse, ReporteCreate

app = FastAPI(title="API MultiSedes S.A.")

equipos_db = []
mantenimientos_db = []
id_equipo = 1

@app.get("/equipos",response_model=List[EquipoResponse])
def obtener_equipos():
    try:
        return equipos_db
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,          detail=f"Error al obtener los equipos: {str(e)}"
        )
@app.get("/equipos/alerta",response_model= List[EquipoResponse])
def obtener_alerta():
    try:
        for equipo in equipos_db:
            if equipo["estado"] == "en falla":
                return equipo
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar las alertas: {str(e)}"
        )
    
@app.post("/equipos", response_model=EquipoResponse)
def registrar_equipo(equipo: EquipoCreate):

    try:
        tipos_equipo = ["planta", "ups", "subestacion"]
        tipo = equipo.tipo.lower()
        
        if tipo not in tipos_equipo:
            raise ValueError(f"El tipo '{equipo.tipo}' no es válido. Las opciones de equipo que se permiten son: {tipos_equipo}")
            
        nuevo_equipo = {
            "id": id_equipo,
            "nombre": equipo.nombre,
            "tipo": tipo,
            "sede": equipo.sede,
            "estado": "operativo" 
        }
        
        equipos_db.append(nuevo_equipo)
        id_equipo += 1
    
        return nuevo_equipo
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al registrar el equipo: {str(e)}"
        )

@app.post("/mantenimiento/crear")
def crear_mantenimiento(reporte: ReporteCreate):
    try:

        reporte_dict = reporte.model_dump()       
        
        equipo_encontrado = None
        
        for equipo in equipos_db:
            if equipo["id"] == reporte_dict["equipo_id"]:
                equipo_encontrado = equipo
                break        
            
        if not equipo_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"El equipo con ID {reporte_dict['equipo_id']} no fue encontrado."
            )
            
        equipo_encontrado["estado"] = "mantenimiento"
        
        mantenimientos_db.append(reporte_dict)
        
        return {
            "mensaje": "Orden de trabajo creada exitosamente",
            "orden_trabajo": reporte_dict,
            "equipo_actualizado": equipo_encontrado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al procesar el mantenimiento: {str(e)}"
        )
