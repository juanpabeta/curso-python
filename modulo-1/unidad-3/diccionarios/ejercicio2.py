usuarios = {
    "u001": {"nombre": "Ana", "correo": "ana@mail.com", "roles": ["admin"]},
    "u002": {"nombre": "Pedro", "correo": "pedro@mail.com", "roles": ["cliente"]}
}

#Acceder al nombre del usuario "u001"
print("Nombre del u001: ",usuarios['u001']['nombre'])

#Agregar un nuevo rol al usuario "u002"
usuarios['u002']['roles'].append('ventas')
print("Roles actualizados del usuario u002: ",usuarios["u002"]['roles'])

#Agregar un nuevo usuario
usuarios['u003'] = {"nombre":'Juan',"correo":"juan@gmail.com","roles":['comprador']}
usuarios['u004'] = {"nombre":'Maria',"correo":"maria@gmail.com","roles":['secretario']}

#Imprimir los usuarios registrados
print("\n ------Listados de usuarios registrados------ \n")
for id_usuario,valores_usuario in usuarios.items():
    print(f"{id_usuario} - {valores_usuario}")
    
#Buscar un usuario de acuerdo a su rol
rol = input("Ingresa un rol para encontrar el usuario: ")
print(f"\nBuscar el rol{rol}")
for id_usuario, valores_usuario in usuarios.items():
    if rol in valores_usuario.get("roles",[]):
        print(f"Usuario: {id_usuario}- Nombre: {valores_usuario['nombre']}")