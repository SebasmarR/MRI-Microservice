from app.database import db
from app.schemas import MRICreate
from app.crypto_utils import encrypt, decrypt

async def create_mri(data: MRICreate, usuario_id: str):
    doc = data.dict()
    doc["usuario_id"] = usuario_id
    doc["descripcion"] = encrypt(doc["descripcion"])
    result = await db.mris.insert_one(doc)
    return await db.mris.find_one({"_id": result.inserted_id})

async def get_mris_by_user(usuario_id: str, skip: int = 0, limit: int = 10):
    cursor = db.mris.find({"usuario_id": usuario_id}).skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        try:
            doc["descripcion"] = decrypt(doc["descripcion"])
        except Exception:
            doc["descripcion"] = "Descripción no disponible"
        results.append(doc)
    return results
