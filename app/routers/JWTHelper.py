from typing import Optional
import jwt
from pydantic import BaseModel

from models.user import User

secret_key = "RMIT_SEPM!@#$%^&*()_+"


def encoded_jwt(payload : User):
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_jwt(token):
    return jwt.decode(token, secret_key, algorithms=['HS256'])