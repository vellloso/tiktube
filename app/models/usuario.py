from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    senha = Column(String)
    seguidores = Column(Integer, default=0)
    seguindo = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)

    seguidores_rel = relationship("Seguidor", foreign_keys="[Seguidor.usuario_id]", back_populates="usuario")
    seguindo_rel = relationship("Seguidor", foreign_keys="[Seguidor.seguindo_id]", back_populates="seguindo_usuario")
    videos = relationship("Video", back_populates="usuario")
    notificacoes = relationship("Notificacao", back_populates="usuario")
    conversas1 = relationship("Conversa", foreign_keys="[Conversa.usuario1_id]", back_populates="usuario1")
    conversas2 = relationship("Conversa", foreign_keys="[Conversa.usuario2_id]", back_populates="usuario2")
    mensagens = relationship("Mensagem", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")