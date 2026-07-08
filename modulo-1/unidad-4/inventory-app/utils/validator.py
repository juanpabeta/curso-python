def validate_product(row: dict) -> dict:
    
    try:
        id_ = int(row["id"])
        if id_ <= 0:
            raise ValueError
        
        name = row["name"].strip()
        if not name:
            raise ValueError("Nombre vacio")
        
        price = float(row["price"])
        if price <= 0:
            raise ValueError
        
        stock = int(row["stock"])
        if stock < 0:
            raise ValueError
        
        return {
            "id": id_,
            "name": name,
            "price": price,
            "stock": stock
        }
    
    except Exception as e:
        raise ValueError(f"Fila inválida: {row}") from e
