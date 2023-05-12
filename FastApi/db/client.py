#Encargado de gestionar la conexion
from pymongo import MongoClient
#Base de datos local
#db_client = MongoClient().local

#base de datos remota
db_client = MongoClient("mongodb+srv://basclavijo:bas.clavijo@cluster0.o3tomww.mongodb.net/?retryWrites=true&w=majority").basclavijo