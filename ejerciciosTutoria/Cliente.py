class Cliente():
    def __init__(self, nombre:str, cedula:str, telefono:str):
        self.nombre = nombre
        self.cedula = cedula
        self.telefono = telefono
        

cliente1 = Cliente("Juan Perez", "123456789", "555-1234")
cliente2 = Cliente("Maria Gomez", "987654321", "555-5678")

clientes = {}

clientes[1] = {
    "nombre": cliente1.nombre,
    "telefono": cliente1.telefono,
    "cedula": cliente1.cedula
}
clientes[2] = {
    "nombre": cliente2.nombre,
    "telefono": cliente2.telefono,
    "cedula": cliente2.cedula
}

def agregar_clientes():
    nombre = input("Ingrese el nombre del cliente: ")
    cedula = input("Ingrese la cédula del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")

    nuevo_cliente = Cliente(nombre, cedula, telefono)

    id = int(input("Ingresa el id del usuario"))
    
    clientes[id] = {
        "nombre": nuevo_cliente.nombre,
        "telefono": nuevo_cliente.telefono,
        "cedula": nuevo_cliente.cedula
    }
print("="*40)
print("\nAgregando un nuevo cliente: ")
agregar_clientes()
print("="*40)

for id, cliente in clientes.items():
        print(f"\nID: {id}")
        print(f"Nombre: {cliente['nombre']}")
        print(f"Cédula: {cliente['cedula']}")
        print(f"Teléfono: {cliente['telefono']}")

