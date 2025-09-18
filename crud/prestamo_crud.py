"""
Operaciones de lectura para Prestamo
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from Prestamo import Prestamo  # Ajusta el import si tu modelo está en otro módulo

class PrestamoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def obtener_prestamo(self, prestamo_id: UUID) -> Optional[Prestamo]:
        return self.db.query(Prestamo).filter(Prestamo.id_prestamo == prestamo_id).first()

    def obtener_prestamos(self, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        return self.db.query(Prestamo).offset(skip).limit(limit).all()

    def obtener_prestamos_por_usuario(self, usuario_id: UUID) -> List[Prestamo]:
        return self.db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id).all()

    def obtener_prestamos_por_producto(self, producto_id: UUID) -> List[Prestamo]:
        return self.db.query(Prestamo).filter(Prestamo.producto_id == producto_id).all()