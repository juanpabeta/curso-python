import csv
import os

from models.estudiante import Estudiante
from repositories.base_repository import BaseRepository


class EstudianteRepositoryCSV(BaseRepository):
    
    def __init__(self,archivo="data/estudiantes.csv"):
        self.archivo=archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo,"w",newline="") as f:
                writer=csv.writer(f)
                writer.writerow (["id","nombre","edad"])
                
    def _leer_archivo(self):
        with open (self.archivo,"r",newline="") as f:
            reader=csv.reader(f)
            next(reader)
            
            return[row for row in reader]
            
            
    def _guardar_archivo(self,data):
        with open (self.archivo,"w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow (["id","nombre","edad"])
            writer.writerows(data)
    
    def agregar(self,estudiante:Estudiante):
        data=self._leer_archivo()
        data.append(estudiante.to_list())
        self._guardar_archivo(data)
        
    def obtener_por_id(self, id):
        data=self._leer_archivo()
        for est in data:
            if int(est[0])==id:
                return Estudiante.from_list(est)
        return None  
    
    def listar(self):
        data=self._leer_archivo()
        return [Estudiante.from_list(est)for est in data]
    
    def eliminar(self,id):
        data=self._leer_archivo()
        data=[est for est in data if int (est[0])!=id]
        self._guardar_archivo(data)
    