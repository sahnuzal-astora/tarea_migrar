from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Audiolibro(Base):
    __tablename__ = "audiolibros"

    id_audiolibro = Column(Integer, primary_key=True, index=True)
    narrador = Column(String(100), nullable=False)
    duracion = Column(Float, nullable=False)
    formato = Column(String(20), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="audiolibro")