"""class Padre():
    def __init__(self, nombre):
        self.nombre = nombre
class Hijo(Padre):
    def __init__(self, nombre, edad):
        super().__init__(nombre)
        self.edad = edad

def main():
    hijo = Hijo("Juan", 10)
    print("Nombre del hijo:", hijo.nombre)
    print("Edad del hijo:", hijo.edad)
    
if __name__ == "__main__":
    main()"""
    
"""class Empleado():
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

class Gerente(Empleado):
    def __init__(self, nombre, salario, departamento):
        super().__init__(nombre, salario)
        self.departamento = departamento

def main():
    gerente = Gerente("Ana", 5000, "Ventas")
    print("Nombre del gerente:", gerente.nombre)
    print("Salario del gerente:", gerente.salario)
    print("Departamento del gerente:", gerente.departamento)
    
if __name__ == "__main__":
    main()"""
    
class Empleado():
    def __init__(self, nombre):
        self.nombre = nombre
        
    def trabajar(self):
        return f"{self.nombre} está trabajando."

class Gerente(Empleado):
    def trabajar(self):
        return super().trabajar() + " Además, está supervisando a su equipo."

class desarrollador(Empleado):
    def trabajar(self):
        return super().trabajar() + " Además, está escribiendo código."
    
def main():
    empleados = [Empleado("Carlos"), Gerente("Laura"), desarrollador("Miguel")]
    
    for empleado in empleados:
        print(empleado.trabajar())
        
if __name__ == "__main__":
    main()