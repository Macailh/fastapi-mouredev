from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []

items_list = [Item(name="Bed", description="Red bed", price=1345315.12, tax=4.4, tags=["tag1", "tag2", "tag3"]),
              Item(name="Chair", description="Simple chair", price=1000.12, tax=5.4, tags=["tag1", "tag2", "tag3"]),
              Item(name="Desk", description="Standing desk", price=4500.00, tax=1.4, tags=["tag1", "tag2", "tag3"])]

@router.get("/")
async def root():
    return items_list