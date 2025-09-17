import uuid
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    usuario_id = Column(ForeignKey("usuarios.id_usuario"), nullable=False)
    producto_id = Column(ForeignKey("productos.id_producto"), nullable=False)

    # Relaciones
    usuario = relationship(
        "Usuario", foreign_keys=[usuario_id], back_populates="prestamos"
    )
    producto = relationship(
        "Producto", foreign_keys=[producto_id], back_populates="prestamos"
    )

    # campos autoria
    id_usuario_crea = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    # Relaciones de auditoría
    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario,usuario_edita"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario,usuario_crea"
    )

    def __repr__(self):
        return f"<Prestamo(id_prestamo={self.id_prestamo}, usuario_id={self.usuario_id}, producto_id={self.producto_id})>"
