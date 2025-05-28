from fastapi import FastAPI
from app.routes import mri

app = FastAPI()

app.include_router(mri.router, prefix="/mris", tags=["MRIs"])
