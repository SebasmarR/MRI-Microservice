from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
APP_URL = os.getenv("APP_URL")

router = APIRouter()

@router.get("/login")
async def login():
    return RedirectResponse(
        url=f"https://{AUTH0_DOMAIN}/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={CALLBACK_URL}&"
            f"scope=openid profile email"
    )

@router.get("/callback")
async def callback(request: Request, code: str = None):
    if not code:
        return HTMLResponse("Error: no code in callback", status_code=400)

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": CALLBACK_URL,  # Debe ser igual que en Auth0 y .env
    }


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url=f"https://{AUTH0_DOMAIN}/v2/logout?"
            f"client_id={CLIENT_ID}&"
            f"returnTo={APP_URL}"
    )

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return user
