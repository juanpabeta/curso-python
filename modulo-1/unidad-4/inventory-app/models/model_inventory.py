from dataclasses import dataclass

@dataclass(frozen=True)
class Producto:
    id:int
    name:str
    price:float
    stock:int
    
    