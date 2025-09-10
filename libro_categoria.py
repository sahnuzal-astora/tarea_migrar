from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class libro_categoria(Base):
    __tablename__ = "categoria_libros"

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    genero = Column(String(100), nullable=False)
    paginas = Column(Integer, nullable=False)

    # Relación inversa
    producto = relationship("Producto", back_populates="libro_categoria")

