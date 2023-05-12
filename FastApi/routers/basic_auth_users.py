#Autenticacion basica
from fastapi import APIRouter, Depends,HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

#clase que se encargara de la autenticacion
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

#Funcion para verificar si el usuario existe
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
    #Criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                            detail="Credenciales de autentificacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Usuario inactivo")
    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

#Funcion que devuelve el usuario autentificado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user





