import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Prestamo(Base):
    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False)

    # Relación inversa con Usuario
    usuario = relationship("Usuario", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo(id_prestamo={self.id_prestamo}, usuario_id={self.usuario_id}, producto_id={self.producto_id})>"
