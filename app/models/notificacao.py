from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base
from datetime import datetime

class Notificacao(Base):
    __tablename__ = 'notificacoes'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    tipo = Column(String)
    conteudo = Column(Text, nullable=True)
    data_criacao = Column(TIMESTAMP, default=datetime.utcnow)
    lida = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="notificacoes")