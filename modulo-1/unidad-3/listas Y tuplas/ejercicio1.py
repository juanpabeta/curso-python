def agregarCliente(listaClientes:list,nombre:str):
    if isinstance(nombre,str) and 2 <= len(nombre) <= 50:
        listaClientes.append(nombre.title())
        print("Clinete agregado")
    else:
        print("Nombre inválido")
        
def mostrarClientes(listaClientes):
    for cliente in listaClientes:
        print(cliente)

def modificarCliente(listaClientes:list,indice:int,nuevoNombre:str):
    if not(isinstance(nuevoNombre,str)) and 2 <= len(nuevoNombre) <= 50:
        print("Nombre inválido")
        return
    if 0 <= indice < len(listaClientes):
        listaClientes[indice] = nuevoNombre.title()
        print(f"Cliente Modificado - Nuevo nombre: {nuevoNombre} ")
    else:
        print("Indice fuera de rango")
        
def eliminarCliente(listaCliente, indice):
    if 0 <= indice  < len(listaCliente):
        eliminado = listaCliente.pop(indice)
        print(f"Cliente eliminado: {eliminado}")
    else:
        print("Indice fuera del rango")
        
def main():
    clientes = ["Juan Pablo","Santiago","Rigel"]
    
    print("Clientes actuales:")
    mostrarClientes(clientes)
    
    agregarCliente(clientes,"Kevin")
    
    modificarCliente(clientes,1,"Alexander")
    
    eliminarCliente(clientes,1)

    print("Clientes Actuales: ")        
    mostrarClientes(clientes)
    
if __name__ == "__main__":
    main()