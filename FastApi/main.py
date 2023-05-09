#Primeros pasos
#inicializar el modulo de FastApi
from fastapi import FastAPI
from routers import products, users

app = FastAPI() #Se crea una variable 

#Routers
app.include_router(products.router)
app.include_router(users.router)

#siempre que se quiera acceder a un servidor las funciones deben de ser asyncrona
#se crea una funcion/operacion/peticiones(funcion asyncrona)
@app.get("/")
async def root(): 
    return "Hello World"

@app.get("/git")
async def git():
    return {"url": "https://github.com/bas-clavijo"}

#para inicializar el servidor uvicorn main:app --reload
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc