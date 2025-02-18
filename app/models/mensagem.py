from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base
from datetime import datetime

class Mensagem(Base):
    __tablename__ = 'mensagens'

    id = Column(Integer, primary_key=True, index=True)
    conversa_id = Column(Integer, ForeignKey('conversas.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    conteudo = Column(Text)
    data_envio = Column(TIMESTAMP, default=datetime.utcnow)

    conversa = relationship("Conversa", back_populates="mensagens")
    usuario = relationship("Usuario", back_populates="mensagens")