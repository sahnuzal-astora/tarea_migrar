from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class comic_categoria(Base):
    __tablename__ = "categoria_comics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    ilustrador = Column(String(150), nullable=False)
    editorial = Column(String(150), nullable=False)
    volumen = Column(Integer, nullable=False)

    producto = relationship("Producto", back_populates="comic_categoria")