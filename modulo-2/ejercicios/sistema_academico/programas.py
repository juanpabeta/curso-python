from conexion import Conexion

def crear_programa(nombre):
    print(f"DEBUG nombre: {nombre} ")
    
    if not nombre:
        print("Nombre Vacio")
        
    conn = Conexion()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO programas (nombre) VALUES (%s)", 
            (nombre)
        )
        conn.commit()
        print("Programa creado exitosamente")
    except Exception as e:
        print(f"Error al crear programa: {e}")
    finally:
        cursor.close()
        conn.close()