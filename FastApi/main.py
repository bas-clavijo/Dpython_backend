#Primeros pasos
#inicializar el modulo de FastApi
from fastapi import FastAPI



app = FastAPI() #Se crea una variable 

#siempre que se quiera acceder a un servidor las funciones deben de ser asyncrona
@app.get("/")
async def root(): #se crea una funcion/operacion(funcion asyncrona)
    return {"message": "Hello World"}