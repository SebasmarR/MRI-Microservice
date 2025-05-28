from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.deps import get_current_user_info, require_roles
from app import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ALLOWED_ROLES = ['missanoguga', 'sebastianmartinezarias']

@router.get("/", response_model=list[schemas.MRIOut])
def listar_mris(
    db: Session = Depends(get_db),
    user_info: dict = Depends(require_roles(ALLOWED_ROLES))
):
    return crud.get_mris_by_user(db, user_info["sub"])

@router.post("/", response_model=schemas.MRIOut)
def crear_mri(
    data: schemas.MRICreate,
    db: Session = Depends(get_db),
    user_info: dict = Depends(require_roles(ALLOWED_ROLES))
):
    return crud.create_mri(db, data, user_info["sub"])
