from models.model_inventory import Producto
from utils.csv_manager import CSVManager
from utils.validator import validate_product

class ProductRepository:
    
    HEADER = ["id", "name", "price", "stock"]
    
    def __init__(self, path: str) -> None:
        self._csv = CSVManager(path)
    
    def get_all(self) -> list[Producto]:
        rows = self._csv.read_all()
        Productos = []
        
        for row in rows:
            clean = validate_product(row)
            Productos.append(Producto(**clean))
        
        return Productos
    
    def save_all(self, productos: list[Producto]) -> None:
        rows = [producto.__dict__ for producto in productos]
        self._csv.write_all(rows, self.HEADER)

