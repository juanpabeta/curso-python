#dict, Hay dos formas de usar definir ditc

persona = {"nombre" : "Juan Pablo", "edad" : 19, "residencia": "Colombia"}

persona = {
    "nombre":  "Juan Pablo",
    "edad" : 19,
    "residencia":"Colombia"   
}

cliente = dict(
    nombre = "Juan Pablo",
    telefono = "3215563732"
)

print(cliente["nombre"])
print(cliente.get("telefono"))

paciente = {
        "nombre":"Punchis",
        "especie":"perrito",
        "edad": 6,
        "vacunado": True
}

#uso del metodo .keys()
print("\n Claves resgistradas en el diccionario \n")
for clave in paciente.keys():
    print(f"Claves disponibles {clave}")

print("\n Valores registrados en el diccionario \n")