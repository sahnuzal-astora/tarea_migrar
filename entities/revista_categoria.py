from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Revista(Base):
    __tablename__ = "revistas"

    id_revista = Column(Integer, primary_key=True, index=True)
    edicion = Column(String(50), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="revista")
