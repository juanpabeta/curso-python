class Estudiante:
    def __init__(self, id, nombre, edad ):
        self.id = id
        self.nombre =  nombre
        self.edad = edad
        
    def to_list(self):
        return [self.id, self.nombre, self.edad]
    
    @staticmethod
    def from_list(data):
        return Estudiante(int(data[0]),data[1],int(data[2]))
    
    def __repr__(self):
        return f"Estudiante(id={self.id},nombre='{self.nombre}', edad={self.edad})" 