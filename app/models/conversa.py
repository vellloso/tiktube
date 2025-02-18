from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base

class Conversa(Base):
    __tablename__ = 'conversas'

    id = Column(Integer, primary_key=True, index=True)
    usuario1_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario2_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario1 = relationship("Usuario", foreign_keys=[usuario1_id], back_populates="conversas1")
    usuario2 = relationship("Usuario", foreign_keys=[usuario2_id], back_populates="conversas2")
    mensagens = relationship("Mensagem", back_populates="conversa")