from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Mapa(Base):
    __tablename__ = "mapas"

    id_mapa = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), nullable=False)
    escala = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="mapa")

