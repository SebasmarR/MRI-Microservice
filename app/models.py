from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base

class MRI(Base):
    __tablename__ = "mris"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    descripcion = Column(String)
