from services.services_task import TaskService
from repository.repository_task import TaskRepository

def main() -> None:
    service = TaskService(TaskRepository("data/tasks.txt"))
    
    while True:
        print("\n1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Completar tarea")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            title = input("Ingrese la tarea: ")
            try:
                service.create_task(title)
                print("Registro guardado")
            except Exception as e:
                print("Error", e)
                
        elif opcion == "2":
            tasks = service.list_tasks()
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")
        
        elif opcion == "3":
            try:
                number = int(input("Ingrese el número de la tarea: "))
                service.complete_task(number)
                print("Tarea completada")
            except ValueError as e:
                print("Error: ", e)
                
        elif opcion == "4":
            break
        
        else:
            print("Opción invalida")

if __name__ == "__main__":
    main()
    
                