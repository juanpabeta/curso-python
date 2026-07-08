import csv
from pathlib import Path

FILE_PATH = Path("data2")

def create_inventory_file():
    fieldnames = ["id", "producto", "precio", "stock"]
    
    with FILE_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"id": 1, "producto": "Mouse", "precio": 40, "stock": 10})
        writer.writerow({"id": 2, "producto": "Teclado", "precio": 30, "stock": 5})
        writer.writerow({"id": 3, "producto": "Pantalla", "precio": 250, "stock": 3})
        
def read_inventory()-> None:
    if not FILE_PATH.exists():
        print("El archivo no existe")
        return

    with FILE_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("\n--- Inventario ---\n")
        for row in reader:
            print(row)
            
def read_inventory_formated()-> None:
    if not FILE_PATH.exists():
        print("El archivo no existe")
        return
    with FILE_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("\n--- Inventario con formato de salida ---\n")
        for row in reader:
            print(
                f"ID: {row['id']} | "
                f"PRODUCTO: {row['producto']} | "
                f"PRECIO: {row['precio']} | "
                f"STOCK: {row['stock']}"
            )
            
def main()-> None:
    create_inventory_file()
    read_inventory()
    read_inventory_formated()
    
if __name__ == "__main__":
    main()