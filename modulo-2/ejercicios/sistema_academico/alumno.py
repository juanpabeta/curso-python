from conexion import Conexion

def crear_alumno(nombre,email, programa_id):
    if not nombre or not email:
        print("Nombre o email vacíos")
        return
    
    conn = Conexion()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO alumnos (nombre, email, programa_id) VALUES (%s, %s, %s)", 
            (nombre, email, programa_id)
        )
        conn.commit()
        print("Alumno creado exitosamente")     
        
    except Exception as e:
        print(f"Error:{e} ")
        
    finally:
        cursor.close()
        conn.close()
        
def eliminar_alumno(id_alumno):
        conn = Conexion()
    
        if conn is None:
            print("Error al conectar a la base de datos")
            return
        
        cursor = conn.cursor()
    
        try:
            cursor.execute(
                "DELETE FROM alumnos WHERE id = %s", 
                (id_alumno,)
            )
            if cursor.rowcount == 0:
                print("No se encontró el alumno con el ID proporcionado")
                return
            
            else:           
                conn.commit()
                print("Alumno eliminado exitosamente")     
            
        except Exception as e:
            print(f"Error:{e} ")
            
        finally:
            cursor.close()
            conn.close()