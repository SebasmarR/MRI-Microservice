from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv
import os
import requests

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

def require_roles(allowed_roles: list[str]):
    def role_checker(user_info: dict = Depends(get_current_user_info)):
        role = user_info.get("nickname")  # Cambia si usas otro campo para roles
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Unauthorized User: role is '{role}'"
            )
        return user_info
    return role_checker
