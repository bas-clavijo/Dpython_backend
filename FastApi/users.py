#creacion de api para usuarios 
from fastapi import FastAPI
#definicion de entidad para el usuario
from pydantic import BaseModel

app = FastAPI()

@app.get("/users")
async def users(): 
    #creacion de usarios
    return [{"name": "Bastian", "surname" : "Clavijo", "url": "https://github.com/bas-clavijo"},
            {"name": "Brais", "surname" : "Moure", "url": "https://moure.dev"},
            {"name": "Marco", "surname" : "Tflay", "url": "https://github.com/Tflay"}]

#inicializar el servidor uvicorn users:app --reload
