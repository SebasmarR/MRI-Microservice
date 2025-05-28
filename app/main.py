import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routes import mri  
from app.auth import router as auth_router  

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(auth_router) 
app.include_router(mri.router, prefix="/mris", tags=["MRIs"]) 

