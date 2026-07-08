from validaciones import validar_texto

def agregar_libro(conexion):
    titulo = input("Título: ")
    autor = input("Autor: ")

    if not validar_texto(titulo) or not validar_texto(autor):
        print("Datos invalidos")
        return
    
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO libro (titulo, autor) VALUES (%s, %s)",
        (titulo, autor)
    )

    conexion.commit()
    print("Libro agregado correctamente")

def ver_libros(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libro")
    libros = cursor.fetchall()

    print("Lista de libros:")
    for libro in libros:
        print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]}")

def eliminar_libro(conexion):
     id_libro = input("ID del libro a eliminar: ") 
     cursor = conexion.cursor()
     cursor.execute("DELETE FROM libro WHERE id = %s", (id_libro,))
     conexion.commit()
     print("Libro eliminado")


