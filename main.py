import uvicorn
import json
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
from routers.users.route import user_route
from fastapi import FastAPI, Request
# from starlette.middleware import Middleware
# from starlette.middleware.sessions import SessionMiddleware
from config.templates import templates
import time
import typing
from fastapi.responses import HTMLResponse
from controllers.usercontroller import usercontroller
from config.flash import get_flash_messages


# middleware = [
#     Middleware(SessionMiddleware,secret_key="super-secret")
# ]
app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
templates.env.globals['get_flash_messages'] = get_flash_messages
# app.include_router(post_route,prefix="/api",tags=["users"])
app.include_router(user_route,prefix="/api",tags=["users"])
app.include_router(usercontroller)
#app.include_router(product_route,prefix="/api",tags=["products"])
@app.middleware("http")
async def process_time_header(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/nice",response_class=HTMLResponse)
async def reg(request:Request):
    return templates.TemplateResponse("auth/register.html",{"request":request})

@app.get("/",tags=["test"])
def read():
    return {"Hai":"Haoaoao"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)

