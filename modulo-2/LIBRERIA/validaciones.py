def validar_texto(texto):
    return texto.strip() != ""

def validar_numero(numero):
    try:
        int(numero)
        return True
    except:
        return False