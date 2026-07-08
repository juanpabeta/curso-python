def contar_vocales():
    vocales = "aeiou"
    palabra = input("Ingrese una palabra: ")
    palabra.lower
    
    cont_vocales = ""
    for letra in palabra:
        if letra in vocales:
            letra += cont_vocales
        return f"Las vocales en la palabra {palabra} son: {cont_vocales}"
print(contar_vocales())    
