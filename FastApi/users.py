#creacion de api para usuarios 
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
async def users(): 
    return "Hola usuario"

#inicializar el servidor uvicorn users:app --reload
