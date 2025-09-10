from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class audiolibro_categoria(Base):
    __tablename__ = "categoria_audiolibros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    narrador = Column(String(150), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    formato = Column(String(50), nullable=False)  # mp3, wav, flac

    producto = relationship("Producto", back_populates="audiolibro_categoria")