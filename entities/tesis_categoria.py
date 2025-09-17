from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Tesis(Base):
    __tablename__ = "tesis"

    id_tesis = Column(Integer, primary_key=True, index=True)
    universidad = Column(String(150), nullable=False)
    director = Column(String(100), nullable=False)
    grado_academico = Column(String(100), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="tesis")