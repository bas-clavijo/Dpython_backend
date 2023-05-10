#Autentificacion cifrada
from fastapi import FastAPI, Depends,HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str 
    disable: bool

class UserDB(User):
    password: str


users_db={
    "morloc": {
        "username": "morloc",
        "full_name": "Bastian clavijo",
        "email": "bas.clavijo@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "morloc2": {
        "username": "morloc2",
        "full_name": "Bastian clavijo 2 ",
        "email": "bas.clavijo2@gmail.com",
        "disable": True,
        "password": "654321"
    }
}