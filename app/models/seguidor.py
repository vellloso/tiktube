from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base

class Seguidor(Base):
    __tablename__ = 'seguidores'

    seguidor_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    seguindo_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="seguidores_rel")
    seguindo_usuario = relationship("Usuario", foreign_keys=[seguindo_id], back_populates="seguindo_rel")