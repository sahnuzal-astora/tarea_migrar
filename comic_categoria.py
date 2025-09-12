from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class Comic(Base):
    __tablename__ = "comics"

    id_comic = Column(Integer, primary_key=True, index=True)
    ilustrador = Column(String(100), nullable=False)
    editorial = Column(String(100), nullable=False)
    volumen = Column(String(50), nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id_producto"))
    producto = relationship("Producto", back_populates="comic")
