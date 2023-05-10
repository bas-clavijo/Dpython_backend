#Primeros pasos
#inicializar el modulo de FastApi
from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI() #Se crea una variable 

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
#Agregando imagenes
app.mount("/static", StaticFiles(directory="static"), name="static")

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