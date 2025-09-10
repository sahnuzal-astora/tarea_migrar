from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class tesis_categoria(Base):
    __tablename__ = "categoria_tesis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    universidad = Column(String(200), nullable=False)
    director = Column(String(150), nullable=False)
    grado_academico = Column(String(100), nullable=False)  # Ej: Licenciatura, Maestría, Doctorado

    producto = relationship("Producto", back_populates="tesis_categoria")