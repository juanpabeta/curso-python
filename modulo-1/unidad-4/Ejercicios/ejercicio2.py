import csv
from pathlib import Path

FILE_PATH = Path("data.csv")

def create_inventory_file() -> None:
    with FILE_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "nombre", "precio", "stock"])
        writer.writerow([1, "Mouse", 40, 10])
        writer.writerow([2, "Teclado", 30, 5])
        writer.writerow([3, "Pantalla", 250, 3])


def read_inventory() -> None:
    if not FILE_PATH.exists():
        print("El archivo no existe")
        return

    with FILE_PATH.open("r", encoding="utf-8") as file:
        reader = csv.reader(file)
        print("\n--- Inventario ---\n")
        for row in reader:
            print(row)


def read_inventory_formatted() -> None:
    if not FILE_PATH.exists():
        print("El archivo no existe")
        return

    with FILE_PATH.open("r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)

        print("\n--- Inventario con formato ---")
        print(f"{header[0]} | {header[1]} | {header[2]} | {header[3]}")

        for row in reader:
            print(
                f"ID: {row[0]} | "
                f"PRODUCTO: {row[1]} | "
                f"PRECIO: {row[2]} | "
                f"STOCK: {row[3]}"
            )


def main() -> None:
    create_inventory_file()
    read_inventory()
    read_inventory_formatted()


if __name__ == "__main__":
    main()