import uvicorn
import json
import os
from routers.route import post_route
from fastapi import FastAPI

app = FastAPI()

app.include_router(post_route,prefix="/api",tags=["users"])

@app.get("/",tags=["test"])
def read():
    return {"Hai":"Haoaoao"}

