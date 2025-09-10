from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

from ..database.database import Base


class Usuario(Base):
    """
    Modelo de Usuario que representa la tabla 'usuarios'
    
    Atributos:
        id: Identificador único del usuario
        nombre: Nombre del usuario
        apellido: Apellido del usuario
        telefono: Número de teléfono (opcional)
        correo: Correo electrónico (único)
    """
    
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    apellido = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(200), nullable=False, unique=True, index=True)

    # Relación con productos
    productos = relationship("Producto", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        """Representación en string del objeto Usuario"""
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', correo='{self.correo}')>"

    def to_dict(self):
        """Convierte el objeto en un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "correo": self.correo
        }


class UsuarioBase(BaseModel):
    """Esquema base para Usuario"""
    nombre: str = Field(..., min_length=2, max_length=200, description="Nombre del usuario")
    apellido: str = Field(..., min_length=2, max_length=200, description="Apellido del usuario")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")

    @validator("nombre", "apellido")
    def validar_cadena(cls, v):
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip().title()

    @validator("telefono")
    def validar_telefono(cls, v):
        if v is not None:
            v = v.strip()
            if v and not v.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
                raise ValueError("Formato de teléfono inválido")
        return v


class UsuarioCreate(UsuarioBase):
    """Esquema para creación de un nuevo usuario"""
    pass


class UsuarioUpdate(BaseModel):
    """Esquema para actualización de un usuario"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    apellido: Optional[str] = Field(None, min_length=2, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None

    @validator("nombre", "apellido")
    def validar_cadena(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip().title() if v else v

    @validator("telefono")
    def validar_telefono(cls, v):
        if v is not None:
            v = v.strip()
            if v and not v.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
                raise ValueError("Formato de teléfono inválido")
        return v


class UsuarioResponse(UsuarioBase):
    """Esquema para respuesta de usuario"""
    id: int

    class Config:
        from_attributes = True


class UsuarioListResponse(BaseModel):
    """Esquema para lista de usuarios"""
    usuarios: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True