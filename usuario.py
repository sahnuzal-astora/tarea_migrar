from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# ====================== USUARIO ======================
class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con productos (un usuario puede tener muchos materiales prestados)
    prestamos = relationship("Prestamo", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}', email='{self.email}')>"