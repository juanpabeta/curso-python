from conexion import Conexion

def alumnos_por_programa(programa_id):
    conn = Conexion()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT alumnos.id, alumnos.nombre, alumnos.email,programas.nombre, notas.nota
            FROM alumnos
            INNER JOIN programas 
            ON alumnos.programa_id = programas.id
            ORDER BY alumnos.nombre
            """
        )
        resultados = cursor.fetchall()
        
        for fila in resultados:
            print(f"Alumno: {fila[1]}, Programa: {fila[3]}, Nota: {fila[4]}")
    except Exception as e:
        print(f"Error al consultar alumnos por programa: {e}")
        return []
    finally:
        cursor.close()
        conn.close()