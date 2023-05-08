#creacion de api para usuarios 
from fastapi import FastAPI
#definicion de entidad para el usuario
from pydantic import BaseModel

app = FastAPI()

#Entidad user
class User():
    name: str
    surname: str
    url: str
    age: int


@app.get("/users")
async def users(): 
    #creacion de usarios
    return [{"name": "Bastian", "surname" : "Clavijo", "url": "https://github.com/bas-clavijo", "age": 22},
            {"name": "Brais", "surname" : "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Marco", "surname" : "Tflay", "url": "https://github.com/Tflay", "age": 17}]

#inicializar el servidor uvicorn users:app --reload
#prueba