from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union, List

router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    id: int
    name: str | None = None
    lastname: str | None = None
    age: int | None = None
    url: str | None = None

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

users_list = [User(id=1, name="Salvador", lastname="German", age=23, url="salvadorgerman.com"),
              User(id=2, name="Jamila", lastname="Fonsen", age=19, url="jamilafon.com"),
              User(id=3, name="Lizx", lastname="Domm", age=34, url="roperded.com")]

@router.get("/")
async def get_users():
    return users_list

@router.get("/json")
async def get_users_json():
    return {"name": "Salvador", "lastname": "German", "age": 23, "url": "https://salvadorgerman.com"}

@router.get("/{user_id}")
async def get_user_by_id(user_id: int): 
    try:
        return next(filter(lambda user: user.id == user_id, users_list))
    except:
        return {"error": "user not found"}
    
@router.get("/")
async def get_user_by_query(id: int):
    return search_user(id)

@router.post("/")
async def add_user(user: User):
    for i, u in enumerate(users_list):
        if u.id == user.id:
            raise HTTPException(status_code=409, detail="There is already a user with that id")
    users_list.routerend(user)
    return user

@router.put("/")
async def update_user(user: User):
    # Iterar sobre la lista de usuarios
    for i, u in enumerate(users_list):
        # Si el usuario en la lista tiene el mismo id que el id proporcionado, actualizarlo
        if u.id == user.id:
            users_list[i] = user
            return {"message": f"User with id { user.id} updated successfully."}
    # Si no se encuentra el usuario en la lista, devolver un mensaje de error
    raise HTTPException(status_code=404, detail="User for update not found")

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    for user in users_list:
        if user.id == user_id:
            users_list.remove(user)
            
            return {"user_deleted": user}
    raise HTTPException(status_code=404, detail="User not found")

def search_user(id: int):
    try:
        return next(filter(lambda user: user.id == id, users_list))
    except:
        return {"error", "user not found"}
    
