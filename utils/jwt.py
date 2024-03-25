from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException
from starlette.requests import Request
import jwt
from dotenv import dotenv_values
env = dotenv_values(".env")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials : HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,detail="Invalid scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,detail="Invalid authorization code")
        
    def verify_jwt(self,jwtoken:str)->bool:
        isTokenValid : bool = False
        try:
            payload = jwt.decode(jwtoken,env["SECRETS"],algorithms=["HS256"])
        except:
            payload = None
        if payload:
            isTokenValid = True
            print(payload)
        return isTokenValid