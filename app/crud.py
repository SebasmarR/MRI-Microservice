from app.database import db
from app.schemas import MRICreate
from app.crypto_utils import encrypt, decrypt

async def create_mri(data: MRICreate, usuario_id: str):
    doc = data.dict()
    doc["fecha"] = doc["fecha"].isoformat()
    doc["hora"] = doc["hora"].isoformat()
    doc["usuario_id"] = usuario_id
    doc["descripcion"] = encrypt(doc["descripcion"])
    result = await db.mris.insert_one(doc)
    return await db.mris.find_one({"_id": result.inserted_id})


from datetime import date, time

async def get_mris_by_user(usuario_id: str, skip: int = 0, limit: int = 10):
    cursor = db.mris.find({"usuario_id": usuario_id}).skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        try:
            doc["descripcion"] = decrypt(doc["descripcion"])
            if "fecha" in doc:
                doc["fecha"] = date.fromisoformat(doc["fecha"])
            if "hora" in doc:
                doc["hora"] = time.fromisoformat(doc["hora"])
            if "paciente_id" not in doc:
                doc["paciente_id"] = "No asignado"
        except Exception:
            doc["descripcion"] = "Descripción no disponible"
            if "paciente_id" not in doc:
                doc["paciente_id"] = "No asignado"
        results.append(doc)
    return results
