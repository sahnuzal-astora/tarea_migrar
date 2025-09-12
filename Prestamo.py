import uuid
from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Prestamo(Base):
    __tablename__ = "prestamos"

    id_prestamo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    usuario_id = Column(ForeignKey("usuarios.id_usuario"), nullable=False)
    producto_id = Column(ForeignKey("productos.id_producto"), nullable=False)
    fecha_prestamo = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_devolucion = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="prestamos")
    producto = relationship("Producto", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo(id_prestamo={self.id_prestamo}, usuario_id={self.usuario_id}, producto_id={self.producto_id})>"