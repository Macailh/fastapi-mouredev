from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    email: str
    is_disabled: bool

class UserDB(User):
    password: str

users_db = {
    "saen": {
        "username": "saen",
        "email": "saen@gmail.com",
        "is_disabled": False
    },
    "adrian": {
        "username": "adrian",
        "email": "adrian@email.com",
        "is_disabled": False
    },
    "serman": {
        "username": "serman",
        "email": "serman@email.com",
        "is_disabled": False
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"})

    if user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disabled user")

    return user

    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    users_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong data")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong data")

    return {"access_token": user.username, "token_type": "bearer"}

    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
