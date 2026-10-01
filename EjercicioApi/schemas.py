from pydantic import BaseModel, Field, ConfigDict


class EquipoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del equipo", examples=["Planta de Emergencia"])
    tipo: str = Field(..., description="Tipo de equipo (planta, ups, subestación)", examples=["planta"])
    sede: str = Field(..., min_length=2, description="Sede a la que pertenece el equipo", examples=["Sede Norte"])
        

class EquipoResponse(BaseModel):
    id: int
    nombre: str = Field(..., examples=["Planta de Emergencia Principal"])
    tipo: str = Field(..., examples=["planta"])
    sede: str = Field(..., examples=["Sede Norte"])
    estado: str = Field(..., description="Estado actual del equipo", examples=["operativo", "en falla", "mantenimiento"])
    
    model_config = ConfigDict(from_attributes=True)

class ReporteCreate(BaseModel):
    equipo_id: int = Field(..., description="ID del equipo al que se le realiza el mantenimiento", examples=[1])
    fecha_reporte: str = Field(..., description="Fecha en la que se reporta el mantenimiento", examples=["2026-07-21"])
    descripcion: str = Field(..., min_length=5, description="Detalles del trabajo realizado", examples=["Cambio de aceite, filtros y revisión de baterías."])
    tecnico: str = Field(..., description="Nombre del técnico responsable", examples=["Juan Pablo"])
    proxima_fecha: str = Field(..., description="Fecha sugerida para el siguiente mantenimiento", examples=["2027-01-21"])

class Message(BaseModel):
    mensaje: str = Field(examples=['Operación realizada de forma exitosa'])