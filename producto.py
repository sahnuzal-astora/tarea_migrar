from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False, index=True)
    autor = Column(String(200), nullable=True)
    año = Column(Integer, default=0, nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)
    tipo = Column(String(200), nullable=False)

    id_usuario_create = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="productos")

    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    id_usuario_create = Column(String(200),nullable=False)
    id_usuario_editar = Column(String(200),nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    
    libro_categoria = relationship("CategoriaLibro", back_populates="producto", uselist=False)
    revista_categoria = relationship("CategoriaRevista", back_populates="producto", uselist=False)
    periodico_categoria = relationship("CategoriaPeriodico", back_populates="producto", uselist=False)
    tesis_categoria = relationship("CategoriaTesis", back_populates="producto", uselist=False)
    comic_categoria = relationship("CategoriaComic", back_populates="producto", uselist=False)
    mapa_categoria = relationship("CategoriaMapa", back_populates="producto", uselist=False)
    audiolibro_categoria = relationship("CategoriaAudiolibro", back_populates="producto", uselist=False)