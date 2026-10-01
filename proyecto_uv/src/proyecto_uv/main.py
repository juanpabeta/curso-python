from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Proyecto UV API",
    description="API de ejemplo para gestionar elementos",
    version="1.0.0",
)


class Item(BaseModel):
    id: Optional[int] = Field(default=None, gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    in_stock: bool = True


items_db: List[Item] = [
    Item(id=1, name="Laptop", price=1200.00, in_stock=True),
    Item(id=2, name="Teclado", price=80.50, in_stock=True),
    Item(id=3, name="Mouse", price=25.00, in_stock=False),
]


@app.get("/")
def home() -> dict:
    return {"message": "API funcionando correctamente"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/items", response_model=List[Item])
def get_items(
    name: Optional[str] = Query(default=None, min_length=1),
    in_stock: Optional[bool] = None,
) -> List[Item]:
    filtered_items = items_db

    if name:
        filtered_items = [item for item in filtered_items if name.lower() in item.name.lower()]

    if in_stock is not None:
        filtered_items = [item for item in filtered_items if item.in_stock == in_stock]

    return filtered_items


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> Item:
    if any(existing.id == item.id for existing in items_db if existing.id is not None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID ya existe")

    new_item = item.copy()
    if new_item.id is None:
        new_item.id = max((existing.id or 0) for existing in items_db) + 1

    items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item) -> Item:
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = item.copy()
            updated_item.id = item_id
            items_db[index] = updated_item
            return updated_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("proyecto_uv.main:app", host="0.0.0.0", port=8000, reload=True)
