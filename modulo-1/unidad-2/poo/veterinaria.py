class Animal():
    def __init__(self,nombre,raza,color):
        self.nombre = nombre
        self.raza = raza
        self.color = color


class Gatito(Animal):
    def maullar():
        return "El gato esta maullando"
    
class Perrito(Animal):
    def ladrar():
        return "El perro esta ladrando"

def main():
    mascotas = [Gatito("Tom","Angora","Blanco con cafecito"),Perrito("Punchis","criollo","Negro con blanco")]

if __name__ == "__main__":
    main()