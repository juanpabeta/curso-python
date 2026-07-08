"""Ejercicio 5 — Base de datos consolidada (unión + eliminación de repetidos)
Dos sucursales registraron clientes:
sucursal_1 = {"Carlos", "Maria", "Andres"}
sucursal_2 = {"Maria", "Luisa", "Carlos", "Elena"}
Actividad
Crear una base única de clientes sin duplicados
Concepto: unión"""

sucursal_1 = {"Carlos", "Maria", "Andres"}
sucursal_2 = {"Maria", "Luisa", "Carlos", "Elena"} 
    
print(f"Los clientes unicos son {sucursal_1 | sucursal_2}")