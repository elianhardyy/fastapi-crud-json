from fastapi import Request
import typing

def flash(request:Request, message:typing.Any,category:str = "") -> None :
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message":message,"category":category})

def get_flash_messages(request:Request):
    print(request.session)
    return request.session.pop("_messages")