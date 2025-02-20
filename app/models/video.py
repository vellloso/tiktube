from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    titulo = Column(String, index=True)
    likes = Column(Integer, default=0)
    caminho = Column(String, index=True)

    usuario = relationship("Usuario", back_populates="videos")
    comentarios = relationship("Comentario", back_populates="video")