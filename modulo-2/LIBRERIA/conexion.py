import psycopg2

def conectar():
    try:  
        conexion = psycopg2.connect(
            host="localhost",
            database="libreria",
            user="postgres",
            password="JP1806",
            
        )
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None