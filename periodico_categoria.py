from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Periodico(Base):
    __tablename__ = "periodicos"

    id_periodico = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    fecha_publicacion = Column(String(50), nullable=False)

    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="periodico")
