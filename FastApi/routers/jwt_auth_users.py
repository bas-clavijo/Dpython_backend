#Autentificacion cifrada
from fastapi import APIRouter, Depends,HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
#openssl rand -hex 32
SECRET = "43170cd5566b6cb9d16406397092741d0c3bcb7cc125c6aee26484771271f7a5"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$cFQogccWaDssNXKeARKGzei9rn7Id1fQ4WWDjHAia732QeHe5pbli"
    },
    "morloc2": {
        "username": "morloc2",
        "full_name": "Bastian clavijo 2 ",
        "email": "bas.clavijo2@gmail.com",
        "disable": True,
        "password": "$2a$12$1hu160uPsRe.L6usoJFZleFWMhdwslAtaVqbu5nKVfV.bvCzU49oi"
    }
}
#Funcion para verificar si el usuario existe
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str= Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                            detail="Credenciales de autentificacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET,algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Usuario inactivo")
    return user


#Autentificacion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")


    access_token = {"sub": user.username, 
                    "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

    
#Funcion que devuelve el usuario autentificado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user