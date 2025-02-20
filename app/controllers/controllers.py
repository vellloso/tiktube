from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.seguidor import Seguidor
from app.models.video import Video
from app.models.like import Like
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.notificacao import Notificacao
from app.models.comentario import Comentario

def criar_usuario(db: Session, nome: str, senha: str):
    db_usuario = Usuario(nome=nome, senha=senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def criar_usuario_admin(db: Session, nome: str, senha: str):
    db_usuario = Usuario(nome=nome, senha=senha, is_admin=True)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def autenticar_usuario(db: Session, nome: str, senha: str):
    return db.query(Usuario).filter(Usuario.nome == nome, Usuario.senha == senha).first()

def criar_seguidor(db: Session, usuario_id: int, seguindo_id: int):
    novo_seguidor = Seguidor(usuario_id=usuario_id, seguindo_id=seguindo_id)
    db.add(novo_seguidor)
    db.commit()

def remover_seguidor(db: Session, usuario_id: int, seguindo_id: int):
    db_seguidor = db.query(Seguidor).filter(Seguidor.usuario_id == usuario_id, Seguidor.seguindo_id == seguindo_id).first()
    if db_seguidor:
        db.delete(db_seguidor)
        db.commit()

def incrementar_seguidores(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.seguidores += 1
        db.commit()

def decrementar_seguidores(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.seguidores -= 1
        db.commit()

def incrementar_seguindo(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.seguindo += 1
        db.commit()

def decrementar_seguindo(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.seguindo -= 1
        db.commit()

def editar_perfil(db: Session, usuario_id: int, novo_nome: str, nova_senha: str):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.nome = novo_nome
        usuario.senha = nova_senha  # Certifique-se de hash a senha antes de salvar
        db.commit()

def criar_video(db: Session, usuario_id: int, titulo: str, caminho: str, likes: int = 0):
    db_video = Video(usuario_id=usuario_id, titulo=titulo, caminho=caminho, likes=likes)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def deletar_video(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        db.delete(video)
        db.commit()

def incrementar_likes(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        video.likes += 1
        db.commit()

def adicionar_like(db: Session, usuario_id: int, video_id: int):
    like = Like(usuario_id=usuario_id, video_id=video_id)
    db.add(like)
    db.commit()

def verificar_like(db: Session, usuario_id: int, video_id: int):
    return db.query(Like).filter(Like.usuario_id == usuario_id, Like.video_id == video_id).first() is not None

def criar_comentario(db: Session, usuario_id: int, video_id: int, conteudo: str):
    comentario = Comentario(usuario_id=usuario_id, video_id=video_id, conteudo=conteudo)
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario

def listar_comentarios(db: Session, video_id: int):
    return db.query(Comentario).filter(Comentario.video_id == video_id).all()

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