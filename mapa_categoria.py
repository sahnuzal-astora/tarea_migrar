from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class mapa_categoria(Base):
    __tablename__ = "categoria_mapas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    region = Column(String(200), nullable=False)
    escala = Column(String(50), nullable=False)  # Ej: 1:50,000
    tipo = Column(String(100), nullable=False)  # Ej: Político, Topográfico, Histórico

    producto = relationship("Producto", back_populates="mapa_categoria")