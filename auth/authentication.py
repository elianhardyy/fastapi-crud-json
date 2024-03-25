import jwt
from fastapi import FastAPI, Depends, status
from models.user import User
from passlib.context import CryptContext
from dotenv import dotenv_values
env = dotenv_values(".env")

