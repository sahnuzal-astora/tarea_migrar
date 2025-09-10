from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

class revista_categoria(Base):
    __tablename__ = "categoria_revistas"

    id_revista = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    numero_edicion = Column(Integer, nullable=False)

    # Relación inversa
    producto = relationship("Producto", back_populates="revista_categoria")