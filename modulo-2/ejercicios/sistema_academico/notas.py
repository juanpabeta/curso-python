from conexion import Conexion

def crear_nota(id_alumno,nota):
    if nota < 0 or nota > 5:
        print("Nota inválida, la nota debe ser de 0 a 5")
        return
    
    conn = Conexion()
    cursor = conn.cursor()
    

    try:
        cursor.execute(
            "INSERT INTO notas (id_alumno,nota) VALUES (%s)", 
            (id_alumno,nota)
        )
        conn.commit()
        print("nota creada exitosamente")
    except Exception as e:
        print(f"Error al crear la nota: {e}")
    finally:
        cursor.close()
        conn.close()
    
    #Actualizar notas
""" 
    try:
        cursor.execute(
            "UPDATE alumnos SET nota = %s WHERE id  = %s"
            (id_alumno,nota)
        )
        conn.commit()
        print("nota actualizada exitosamente")
        
    except Exception as e:
        print(f"Error al actualizar la nota: {e}")
    finally:
        cursor.close()
        conn.close()
    """