import csv
from pathlib import Path

FILE_PATH = Path("registro_avistamientos.csv")

def crear_archivo_avistamientos()-> None:
    with FILE_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        
        writer.writerow(["avistamiento_id","especie","zona","cantidad"])
        
        writer.writerow([1, "Delfín", "Costa Norte", 5])
        writer.writerow([2, "Ballena ", "Océano Pacífico", 2])
        writer.writerow([3, "Tortuga Marina", "Playa Sur", 8])
        writer.writerow([4, "Tiburón Blanco", "Mar Abierto", 1])
        writer.writerow([5, "Pelícano", "Zona Costera", 12])
        writer.writerow([6, "León Marino", "Isla Rocosa", 6])
        writer.writerow([7, "Mantarraya", "Arrecife Coralino", 4])
        writer.writerow([8, "Pingüino", "Región Austral", 15])
        writer.writerow([9, "Gaviota", "Puerto Pesquero", 20])
        writer.writerow([10, "Orca", "Océano Atlántico", 3])
        
def leer_datos_crudos()-> None:
    if not FILE_PATH.exists():
        print("El archivo ni existe")
        return
    
    with FILE_PATH.open("r",encoding="utf-8",newline="")as file:
        reader = csv.DictReader(file)
        print("\n --- AVISTAMIENTOS --- \n")
        for row in reader:
            print(row)
            
def mostrar_reporte_biologo()-> None:
    if not FILE_PATH.exists():
        print("El archivo no existe")
        return
    with FILE_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("\n\033[95m---- AVISTAMIENTOS ----\033[0m\n")
        print("╔═════════════════════════════════════════════════════════╗")
        print("║                    AVISTAMIENTOS REGISTRADOS            ║")
        print("╠══════╦════════════════╦════════════════════╦════════════╣")
        print("║ ID   ║ ESPECIE        ║ LOCALIZACIÓN       ║ EJEMPLARES ║")
        print("╠══════╬════════════════╬════════════════════╬════════════╣")

        for row in reader:
            print(
            f"║ {row['avistamiento_id']:<4} "
            f"║ {row['especie']:<14} "
            f"║ {row['zona']:<18} "
            f"║ {row['cantidad']:<10} ║"
    )

    print("╚══════╩════════════════╩════════════════════╩════════════╝")       
            
def main()-> None:
    crear_archivo_avistamientos()
    leer_datos_crudos()
    mostrar_reporte_biologo()
    
if __name__ == "__main__":
    main()