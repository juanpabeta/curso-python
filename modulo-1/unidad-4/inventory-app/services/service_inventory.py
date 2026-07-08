from repository.repository_inventory import ProductRepository
from models.model_inventory import Producto

class InventoryService:
    
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo
    
    def add_product(self, product: Producto) -> None:
        productos = self._repo.get_all()
        
        if any(p.id == product.id for p in productos):
            raise ValueError("Producto duplicado")
        
        productos.append(product)
        self._repo.save_all(productos)
    
    def list_products(self) -> list[Producto]:
        return self._repo.get_all()


        
        