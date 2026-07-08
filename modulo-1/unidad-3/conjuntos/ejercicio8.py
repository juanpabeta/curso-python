from typing import Set,Tuple,List

def _obtener_usuarios_con_acceso(usuarios_autorizados:Set[str],usuarios_intentando:Set[str])-> Set[str]:
    return {u for u in usuarios_intentando if u in usuarios_autorizados}

def _obtener_usuarios_sin_acceso(usuarios_autorizados:Set[str],usuarios_intentando:Set[str])-> Set[str]:
    return {u for u in usuarios_intentando if u not in usuarios_autorizados}

def validar_acceso(usuarios_autorizados:Set[str],usuarios_intentando:Set[str])-> Tuple[set[str],Set[str]]:
    autorizados = set(usuarios_autorizados)
    intentando = set(usuarios_intentando)
    
    acceso = _obtener_usuarios_con_acceso(autorizados,intentando)
    no_acceso = _obtener_usuarios_sin_acceso(autorizados,intentando)
    
    return acceso,no_acceso

def main()-> None:
    autorizados = {"Alexis","Julian","Pablo"}
    intentando = {"Ignancio","Jerónimo","Anobis","Julian","Diego","Pablo"}
    
    acceso,no_acceso = validar_acceso(autorizados,intentando)
    
    print(f"Usuario con acceso: {acceso}")
    print(f"Usuarios sin acceso: {no_acceso}")
    
if __name__ == "__main__":
    main()
    
    