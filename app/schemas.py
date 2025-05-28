from pydantic import BaseModel
from datetime import date, time

class MRICreate(BaseModel):
    fecha: date
    hora: time
    descripcion: str

class MRIOut(MRICreate):
    id: int
    usuario_id: str

    class Config:
        orm_mode = True
