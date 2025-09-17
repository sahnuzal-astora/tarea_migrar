from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    anio = Column(Integer, nullable=False)
    disponible = Column(Boolean, default=True)

    # Campos de auditoría
    id_usuario_crea = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    # Relaciones de auditoría
    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea"
    )

    # Relación con préstamos
    prestamos = relationship("Prestamo", back_populates="producto", lazy="dynamic")

    # Relaciones con categorías
    libro = relationship("Libro", back_populates="producto", uselist=False)
    revista = relationship("Revista", back_populates="producto", uselist=False)
    periodico = relationship("Periodico", back_populates="producto", uselist=False)
    audiolibro = relationship("Audiolibro", back_populates="producto", uselist=False)
    comic = relationship("Comic", back_populates="producto", uselist=False)
    mapa = relationship("Mapa", back_populates="producto", uselist=False)
    tesis = relationship("Tesis", back_populates="producto", uselist=False)

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, titulo='{self.titulo}', autor='{self.autor}')>"
