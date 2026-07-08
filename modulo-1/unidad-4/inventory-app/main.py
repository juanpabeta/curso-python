from services.service_inventory import InventoryService
from repository.repository_inventory import ProductRepository
from models.model_inventory import Producto

def main() -> None:
    
    service = InventoryService(ProductRepository("data/data_inventorycsv"))
    
    while True:
        print("\n1. Agregar producto")
        print("2. Listar productos")
        print("3. Salir")
        
        opcion = input("Seleccione opción: ")
        
        if opcion == "1":
            try:
                p = Producto(
                    int(input("ID: ")),
                    input("Nombre: "),
                    float(input("Precio: ")),
                    int(input("Stock: "))
                )
                service.add_product(p)
                print("Guardado")
            except Exception as e:
                print("Error: ", e)
        
        elif opcion == "2":
            for p in service.list_products():
                print(p)
            
        elif opcion == "3":
            break

if __name__ == "__main__":
    main()