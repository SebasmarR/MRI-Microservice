from sqlalchemy.orm import Session
from . import models, schemas
from .crypto_utils import encrypt, decrypt

def create_mri(db: Session, data: schemas.MRICreate, usuario_id: str):
    encrypted_description = encrypt(data.descripcion)
    mri = models.MRI(
        usuario_id=usuario_id,
        fecha=data.fecha,
        hora=data.hora,
        descripcion=encrypted_description
    )
    db.add(mri)
    db.commit()
    db.refresh(mri)
    return mri

def get_mris_by_user(db: Session, usuario_id: str):
    mris = db.query(models.MRI).filter(models.MRI.usuario_id == usuario_id).all()
    for mri in mris:
        try:
            mri.descripcion = decrypt(mri.descripcion)
        except Exception:
            mri.descripcion = "Descripción no disponible"
    return mris
