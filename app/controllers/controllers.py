from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.seguidor import Seguidor
from app.models.video import Video
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.notificacao import Notificacao

def criar_usuario(db: Session, gmail: str, nome: str, senha: str):
    db_usuario = Usuario(gmail=gmail, nome=nome, senha=senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def criar_seguidor(db: Session, usuario_id: int, seguindo_id: int):
    db_seguidor = Seguidor(usuario_id=usuario_id, seguindo_id=seguindo_id)
    db.add(db_seguidor)
    db.commit()
    db.refresh(db_seguidor)
    return db_seguidor

def criar_video(db: Session, usuario_id: int, titulo: str, caminho: str, likes: int = 0):
    db_video = Video(usuario_id=usuario_id, titulo=titulo, caminho=caminho, likes=likes)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def criar_conversa(db: Session, usuario1_id: int, usuario2_id: int):
    db_conversa = Conversa(usuario1_id=usuario1_id, usuario2_id=usuario2_id)
    db.add(db_conversa)
    db.commit()
    db.refresh(db_conversa)
    return db_conversa

def criar_mensagem(db: Session, conversa_id: int, usuario_id: int, conteudo: str):
    db_mensagem = Mensagem(conversa_id=conversa_id, usuario_id=usuario_id, conteudo=conteudo)
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem

def criar_notificacao(db: Session, usuario_id: int, tipo: str, conteudo: str = None, lida: bool = False):
    db_notificacao = Notificacao(usuario_id=usuario_id, tipo=tipo, conteudo=conteudo, lida=lida)
    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)
    return db_notificacao