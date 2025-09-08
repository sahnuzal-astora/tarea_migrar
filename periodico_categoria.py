from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


class periodico_categoria(Base):
    __tablename__ = "categoria_periodicos"

    id_periodico = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    fecha_publicacion = Column(DateTime, nullable=False)

    # Relación inversa
    producto = relationship("Producto", back_populates="periodico_categoria")