from typing import Set, Tuple

def _normalizar_producto(nombre: str) -> str:
  return nombre.strip().capitalize()

def _es_producto_valido(nombre: str) -> bool:
  return nombre != ""

# Entrada de datos

def _leer_entero(mensaje: str) -> int:
  while True:
    valor: str = input(mensaje)
    if valor.isdigit():
      return int(valor)
    print("Error: debe ingresar un número entero válido")

def _leer_texto(mensaje: str) -> str:
  return input(mensaje)

def _leer_producto(indice: int) -> str:
  while True:
    texto: str = _leer_texto(f"Producto {indice}: ")
    producto: str = _normalizar_producto(texto)
    
    if _es_producto_valido(producto):
      return producto
    
    print("El producto no puede estar vácio")
  
def _construir_conjunto_productos(nombre_tienda: str) -> Set[str]:
  productos: Set[str] = set()
  cantidad: int = _leer_entero(f"Ingrese la cantidad de productos de {nombre_tienda}: ")
  for i in range(1, cantidad + 1):
    producto: str = _leer_producto(i)
    productos.add(producto)
    
  return productos

# Lógica del software ó el servicio (service layer)
def operaciones_productos(
  tienda_a: Set[str],
  tienda_b: Set[str]
) -> Tuple[Set[str], Set[str], Set[str]]:
  union: Set[str] = tienda_a | tienda_b
  interseccion: Set[str] = tienda_a & tienda_b
  diferencia: Set[str] = tienda_a - tienda_b
  return union, interseccion, diferencia

# Presentación (Capa de presentación)

def _mostrar_conjunto(nombre: str, datos: Set[str]) -> None:
  print(f"{nombre}: {sorted(datos)}")

def _mostrar_resultados(
  union: Set[str],
  interseccion: Set[str],
  diferencia: Set[str]
) -> None:
  print("\n--- RESULTADOS ---")
  _mostrar_conjunto("Unión", union)
  _mostrar_conjunto("Interseción: ", interseccion)
  _mostrar_conjunto("Solo en la Tienda A ", diferencia)

def main() -> None:
  print("=== INVENTARIO DE TIENDAS ===\n")
  
  tienda_a: Set[str] = _construir_conjunto_productos("Tienda A")
  tienda_b: Set[str] = _construir_conjunto_productos("Tienda B")
  
  union, interseccion, diferencia = operaciones_productos(tienda_a, tienda_b)
  
  _mostrar_resultados(union, interseccion, diferencia)
  
if __name__ == "__main__":
  main()