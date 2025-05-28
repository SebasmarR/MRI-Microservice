from pydantic import BaseModel, Field
from datetime import date, time
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "format": "objectid",
            "pattern": "^[a-f\\d]{24}$"
        }

class MRICreate(BaseModel):
    fecha: date
    hora: time
    descripcion: str
    paciente_id: str    

class MRIOut(MRICreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    usuario_id: str

    class Config:
        json_encoders = {ObjectId: str}
        validate_by_name = True
