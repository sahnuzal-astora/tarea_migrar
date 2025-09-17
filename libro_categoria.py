from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Libro(Base):
    __tablename__ = "libros"

    id_libro = Column(Integer, primary_key=True, index=True)
    genero = Column(String(100), nullable=False)
    paginas = Column(Integer, nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id_producto"))

    producto = relationship("Producto", back_populates="libro")

