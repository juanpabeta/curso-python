palabra = input("Ingrese una palabra: ")

vocales = "aeiou"
for letra in palabra:
    if letra in vocales:
        print(f"Las letras de la palabra {palabra} son estas: {letra} ")

