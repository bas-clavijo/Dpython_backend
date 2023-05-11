#creacion de api para usuarios db
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


#Lista de usuarios
users_list =[]

#obtener todos los usuarios 
@router.get("/", response_class=list[User])
async def users():
    return users_schema(db_client.local.users.find())

#Busqueda de todos los usuarios por id
#Utilizacion del Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id",ObjectId(id))

#Utilizacion de Query
@router.get("/")
async def user(id: str):
    return search_user("_id",ObjectId(id))
    
#Operacion para agregar usuarios
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)

#Operacion para actualizar usuarios
@router.put("/")
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
@router.delete("/{id}")
async def user(id: str, status_code=status.HTTP_204_NO_CONTENT):

    found = db_client.local.user.find_one_and_delete()

    if not found:
        return{"Error": "No se ha eliminado el usuario"}

#funcion de busqueda
def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
