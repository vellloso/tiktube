from sqlalchemy import Column, Integer, ForeignKey
from app.controllers.db.database import Base

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    video_id = Column(Integer, ForeignKey('videos.id'))