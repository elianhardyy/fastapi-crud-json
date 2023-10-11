from fastapi import FastAPI,Body
from models.user import UserSchema
import uvicorn
import json
import os

app = FastAPI()

# users:dict = open("data/data.json","r")
file_path = 'data/data.json'

@app.get("/",tags=["test"])
def read():
    return {"Hai":"Haoaoao"}

@app.get("/user",tags=["users"])
def findAll():
    with open("data/data.json","r") as file:
        return json.load(file)

@app.post("/add", tags=["users"])
def create(user:UserSchema):
    if(os.path.exists(file_path)):
        with open("data/data.json","r") as file:
            data = json.load(file)
        
        obj = [{
            "id":len(data)+1,
            "name":user.name,
            "age":user.age,
            "email":user.email,
            "address":user.address
        }]
        data.extend(obj)
        with open("data/data.json","w") as add:
            json.dump(data,add)
        return {
            "info":data
        }
    else:
        with open("data/data.json","a") as createFile:
            createFile.read()

@app.get("/detail/{id}",tags=["users"])
def getSingle(id:int):
    with open("data/data.json","r") as file:
        data=json.load(file)
    if id > len(data):
        return {
            "error":"Post data not found"
        }
    for d in data:
        if d["id"] == id:
            return {
                "data":d
            }


    

