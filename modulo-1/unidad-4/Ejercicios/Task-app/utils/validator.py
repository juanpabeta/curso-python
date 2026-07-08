def validate_title(title:str)-> str:
    title = title.strip()
    
    if not title:
        raise ValueError("La tarea no puede estar vacía")
    
    if len(title) > 60:
        raise ValueError("El nombre de la tarea supera el limite de caracteres")
    
    if "|" in title:
        raise ValueError("El nombre de la tarea no puede contener el caracter '|'")
    
    return title

def validate_index(index:int,size:int)-> int:
    if size == 0:
        raise ValueError("No hay tareas registradas")
    if index < 1:
        raise ValueError("El indice de la tarea modificar de ser superior a 0 ")
    if index > size:
        raise ValueError("El indice de la tarea modificar debe estar dentro del rango de registros")
    
    return index-1