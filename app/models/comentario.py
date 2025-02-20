from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.controllers.db.database import Base

class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    video_id = Column(Integer, ForeignKey('videos.id'))
    conteudo = Column(Text)

    usuario = relationship("Usuario", back_populates="comentarios")
    video = relationship("Video", back_populates="comentarios")