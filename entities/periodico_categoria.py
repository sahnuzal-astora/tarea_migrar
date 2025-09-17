from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Periodico(Base):
    __tablename__ = "periodicos"

    id_periodico = Column(Integer, primary_key=True, index=True)
    fecha_publicacion = Column(String(50), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="periodico")