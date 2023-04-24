from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])

class Product(BaseModel):
    id: int
    name: str
    description: str

products = [Product(id=1, name="Box", description="A simple box"),
            Product(id=2, name="Shirt", description="A white shirt")]

@router.get("/")
def get_all_products():
    return products

@router.put("/")
def add_product(product: Product):
    products.routerend(product)
    return product

@router.get("/{product_id}")
def find_product(product_id: int):
    return list(filter(lambda p: p.id == product_id, products))

@router.put("/{product_id}")
def add_product(product_id: int, product: Product):
    products.routerend(product)
    return product