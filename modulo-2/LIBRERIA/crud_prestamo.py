from validaciones import validar_texto, validar_numero

def prestar_libro(conexion):
    libro_id = input("ID del libro: ")
    usuario = input("Nombre del usuario: ")

    if not validar_numero(libro_id) or not validar_texto(usuario):
        print("Datos inválidos")
        return
    
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM libro WHERE id = %s", (libro_id,))
    libro = cursor.fetchone()

    if not libro:
        print("El libro no exite")
        return
    
    cursor.execute(
        "SELECT * FROM prestamo WHERE libro_id =%s",
        (libro_id)
    )
    prestamo = cursor.fetchone()

    if prestamo:
        print("El libro esta prestado")
        return
    
    cursor.execute(
        "INSERT INTO prestamo (libro_id, usuario, fecha_prestamo) VALUES (%s, %s, NOW())",
        (libro_id, usuario)
    )
    conexion.commit()
    print("Préstamo realizado")

def ver_prestamo(conexion):
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT p.id, l.titulo, p.usuario, p.fecha_prestamo
        FROM prestamo p
        INNER JOIN libro l ON p.libro_id = l.id

    """)
    prestamos = cursor.fetchall()

    print("Lista de prestamos:")
    for p in prestamos:
        print(f"ID: {p[0]} | Libro: {p[1]} | Usuario: {p[2]} | Fecha: {p[3]}")




