#creacion de api para usuarios 
from fastapi import APIRouter, HTTPException
#definicion de entidad para el usuario
from pydantic import BaseModel

router = APIRouter()

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

#Lista de usuarios
users_list = [User(id=1,name="Bastian", surname="Clavijo",url="https://github.com/bas-clavijo", age=22),
              User(id=2,name="Brais", surname="Moure",url="https://moure.dev", age=35),
              User(id=3,name="Marco", surname="Tflay", url="https://github.com/Tflay", age=17)]

#Clase que esta heredando un comportamiento de basemodel
@router.get("/users")
async def users():
    return users_list

#Entrada de forma manual
@router.get("/usersjson")
async def usersjson(): 
    #creacion de usarios
    return [{"name": "Bastian", "surname" : "Clavijo", "url": "https://github.com/bas-clavijo", "age": 22},
            {"name": "Brais", "surname" : "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Marco", "surname" : "Tflay", "url": "https://github.com/Tflay", "age": 17}]


#Utilizacion del Path
@router.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id ==id, users_list)
    #comprobacion de si la lista esta vacia
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
#Utilizacion de Query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)
    
#Operacion para agregar usuarios
#Http status code
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

#Operacion para actualizar usuarios(Actualizar datos completos)
@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return{"Error": "No se ha actualizado el usuario"}
    else:
        return user

#Operacion para eliminar usuarios
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return{"Error": "No se ha eliminado el usuario"}

#funcion de busqueda(se puede reutilizar esta funcion en path y query)
def search_user(id: int):
    users = filter(lambda user: user.id ==id, users_list)
    #comprobacion de si la lista esta vacia
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}

#inicializar el servidor uvicorn users:app --reload
