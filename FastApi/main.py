#Primeros pasos
#inicializar el modulo de FastApi
from fastapi import FastAPI



app = FastAPI() #Se crea una variable 

#siempre que se quiera acceder a un servidor las funciones deben de ser asyncrona
#se crea una funcion/operacion/peticiones(funcion asyncrona)
@app.get("/")
async def root(): 
    return "Hello World"

@app.get("/git")
async def git():
    return {"url": "https://github.com/bas-clavijo" }