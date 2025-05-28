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

def get_current_user_info(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuario inválido")

        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"https://{AUTH0_DOMAIN}/userinfo", headers=headers)

        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Error al consultar userinfo de Auth0")

        userinfo = resp.json()
        userinfo["sub"] = user_id
        return userinfo

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

def require_roles(allowed_roles: list[str]):
    def role_checker(user_info: dict = Depends(get_current_user_info)):
        role = user_info.get("nickname")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Unauthorized User: role is '{role}'"
            )
        return user_info
    return role_checker
