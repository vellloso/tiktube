import os
import uuid
import datetime # Adicionado import para uso do datetime
import json # Adicionado import para uso do json.dumps
import pytz  # Adicionado import para uso do pytz
from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, response, template
from urllib.parse import quote, unquote
from app.controllers.db.database import engine, Base, SessionLocal
from app.models.usuario import Usuario
from app.models.seguidor import Seguidor
from app.models.video import Video
from app.models.like import Like
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.notificacao import Notificacao
from app.controllers import controllers

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'app', 'static', 'videos')
app = Bottle()
ctl = Application()
Base.metadata.create_all(bind=engine)
# Cria uma sessão para interagir com o banco de dados
db = SessionLocal()

#usuarios = db.query(Usuario).all()
#print("Usuários no banco de dados:")
#for usuario in usuarios:
    #print(f"ID: {usuario.id}, Nome: {usuario.nome}")

admin_usuario = db.query(Usuario).filter(Usuario.nome == "admin").first()
if not admin_usuario:
    controllers.criar_usuario_admin(db, nome="admin", senha="admin")

#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/videos/<filename:path>')
def serve_videos(filename):
    return static_file(filename, root=UPLOAD_DIR)

@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')

# Suas rotas aqui:

@app.route('/login')
def login():
    return ctl.render('login')

@app.route('/register')
def register():
    return ctl.render('register')

@app.route('/home')
def home():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    info = {'nome': nome, 'logado': logado, 'usuario_id': usuario.id if usuario else None, 'is_admin': usuario.is_admin if usuario else False}
    videos = db.query(Video).all()
    videos_info = []
    for video in videos:
        comentarios = [{'conteudo': comentario.conteudo, 'autor': comentario.usuario.nome} for comentario in video.comentarios]
        videos_info.append({
            'id': video.id,
            'titulo': video.titulo,
            'caminho': video.caminho,
            'likes': video.likes,
            'autor': video.usuario.nome,
            'autor_id': video.usuario.id,
            'comentarios': comentarios
        })
    conteudo = {'info': info, 'videos': videos_info, 'verificar_like': controllers.verificar_like, 'db': db}    
    return ctl.render('home', conteudo)

@app.route('/home/following')
def home_following():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario:
        redirect('/login')        @app.route('/home/following')
        def home_following():
            nome = request.get_cookie("nome", default="Visitante")
            logado = request.get_cookie("logado", default="NAO")
            usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
            if not usuario:
                redirect('/login')
                return
            
            seguindo_ids = [seguidor.seguindo_id for seguidor in db.query(Seguidor).filter(Seguidor.usuario_id == usuario.id).all()]
            videos = db.query(Video).filter(Video.usuario_id.in_(seguindo_ids)).all()
            videos_info = []
            for video in videos:
                print(f"Video caminho: {video.caminho}")  # Adicionando print para depuração
                comentarios = [{'conteudo': comentario.conteudo, 'autor': comentario.usuario.nome} for comentario in video.comentarios]
                videos_info.append({
                    'id': video.id,
                    'titulo': video.titulo,
                    'caminho': video.caminho,
                    'likes': video.likes,
                    'autor': video.usuario.nome,
                    'autor_id': video.usuario.id,
                    'comentarios': comentarios
                })
            info = {'nome': nome, 'logado': logado, 'usuario_id': usuario.id, 'is_admin': usuario.is_admin}
            return template('app/views/html/home', info=info, videos=videos_info, verificar_like=controllers.verificar_like, db=db)
    seguindo_ids = [seguidor.seguindo_id for seguidor in db.query(Seguidor).filter(Seguidor.usuario_id == usuario.id).all()]
    videos = db.query(Video).filter(Video.usuario_id.in_(seguindo_ids)).all()
    videos_info = []
    for video in videos:
        print(f"Video caminho: {video.caminho}")  # Adicionando print para depuração
        comentarios = [{'conteudo': comentario.conteudo, 'autor': comentario.usuario.nome} for comentario in video.comentarios]
        videos_info.append({
            'id': video.id,
            'titulo': video.titulo,
            'caminho': video.caminho,
            'likes': video.likes,
            'autor': video.usuario.nome,
            'autor_id': video.usuario.id,
            'comentarios': comentarios
        })
    info = {'nome': nome, 'logado': logado, 'usuario_id': usuario.id, 'is_admin': usuario.is_admin}
    conteudo = {'info': info, 'videos': videos_info, 'verificar_like': controllers.verificar_like, 'db': db}
    return ctl.render('home', conteudo)

@app.route('/validar-login', method='POST')
def validarLogin():
    form_data = request.forms        
    nome = form_data.get('username')
    senha = form_data.get('password')
    
    usuario = controllers.autenticar_usuario(db, nome=nome, senha=senha)
    if usuario is None:
        redirect('/login')
    
    response.set_cookie("nome", nome, path="/")
    response.set_cookie("logado", "SIM", path="/")
    redirect('/home')
    return 

@app.route('/validar-registro', method='POST')
def validarCadastro():
    form_data = request.forms        
    nome = form_data.get('username')
    senha = form_data.get('password')
    usuario1 = controllers.criar_usuario(db, nome=nome, senha=senha)
    response.set_cookie("nome", nome, path="/")
    response.set_cookie("logado", "SIM", path="/")
    redirect('/home')
    return

@app.route('/logout')
def logout():
    response.set_cookie("nome", "", expires=0)
    response.set_cookie("logado", "", expires=0)
    redirect('/home')

@app.route('/profile')
def profile():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    if logado == "SIM":
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
        if usuario:
            redirect(f'/profile/{usuario.id}')
            return
    else:
        redirect('/login')
        return

@app.route('/profile/<usuario_id:int>')
def view_profile(usuario_id):
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if usuario:
        is_self = usuario_logado and usuario_logado.id == usuario.id
        is_following = False
        if usuario_logado:
            is_following = db.query(Seguidor).filter(Seguidor.usuario_id == usuario_logado.id, Seguidor.seguindo_id == usuario.id).first() is not None
        videos = db.query(Video).filter(Video.usuario_id == usuario.id).all()
        videos_info = []
        for video in videos:
            comentarios = [{'conteudo': comentario.conteudo, 'autor': comentario.usuario.nome} for comentario in video.comentarios]
            videos_info.append({
                'id': video.id,
                'titulo': video.titulo,
                'caminho': video.caminho,
                'likes': video.likes,
                'autor': video.usuario.nome,
                'comentarios': comentarios
            })
        info = {
            'nome': usuario.nome,
            'seguidores': usuario.seguidores,
            'seguindo': usuario.seguindo,
            'is_self': is_self,
            'is_following': is_following,
            'usuario_id': usuario.id,
            'videos': videos_info
        }
    else:
        info = {'nome': 'Usuário não encontrado', 'seguidores': 0, 'seguindo': 0, 'is_self': False, 'is_following': False, 'usuario_id': 0, 'videos': []}
    
    return ctl.render('profile', info)

@app.route('/follow', method='POST')
def follow():
    usuario_id = int(request.forms.get('usuario_id'))
    nome = request.get_cookie("nome", default="Visitante")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if usuario_logado:
        controllers.criar_seguidor(db, usuario_logado.id, usuario_id)
        controllers.incrementar_seguidores(db, usuario_id)
        controllers.incrementar_seguindo(db, usuario_logado.id)
        
        # Verificar se o usuário 2 (usuario_id) segue o usuário 1 (usuario_logado.id)
        if db.query(Seguidor).filter(Seguidor.usuario_id == usuario_id, Seguidor.seguindo_id == usuario_logado.id).first():
            # Criar uma conversa entre os dois usuários
            if not db.query(Conversa).filter(
                (Conversa.usuario1_id == usuario_logado.id) & (Conversa.usuario2_id == usuario_id) |
                (Conversa.usuario1_id == usuario_id) & (Conversa.usuario2_id == usuario_logado.id)
            ).first():
                nova_conversa = Conversa(usuario1_id=usuario_logado.id, usuario2_id=usuario_id)
                db.add(nova_conversa)
                db.commit()
    
    redirect(f'/profile/{usuario_id}')
    return

@app.route('/unfollow', method='POST')
def unfollow():
    usuario_id = int(request.forms.get('usuario_id'))
    nome = request.get_cookie("nome", default="Visitante")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if usuario_logado:
        controllers.remover_seguidor(db, usuario_logado.id, usuario_id)
        controllers.decrementar_seguidores(db, usuario_id)
        controllers.decrementar_seguindo(db, usuario_logado.id)
        
        # Verificar se existe uma conversa entre os dois usuários
        conversa = db.query(Conversa).filter(
            (Conversa.usuario1_id == usuario_logado.id) & (Conversa.usuario2_id == usuario_id) |
            (Conversa.usuario1_id == usuario_id) & (Conversa.usuario2_id == usuario_logado.id)
        ).first()
        
        if conversa:
            db.delete(conversa)
            db.commit()
    
    redirect(f'/profile/{usuario_id}')
    return

@app.route('/editar-perfil', method='POST')
def editar_perfil():
    nome = request.get_cookie("nome", default="Visitante")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if usuario_logado:
        novo_nome = request.forms.get('nome')
        nova_senha = request.forms.get('senha')
        controllers.editar_perfil(db, usuario_logado.id, novo_nome, nova_senha)
        response.set_cookie("nome", novo_nome, path="/")
    
    redirect(f'/profile/{usuario_logado.id}')
    return

@app.route('/upload-video', method='POST')
def upload_video():
    titulo = request.forms.get('titulo')
    video = request.files.get('video')
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    # Gerar um nome de arquivo único
    unique_filename = f"{uuid.uuid4()}_{video.filename}"
    video_path = os.path.join(UPLOAD_DIR, unique_filename)
    video.save(video_path)
    os.chmod(video_path, 0o644)
    
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        redirect('/erro?tipo=Erro: Usuário não encontrado!')
        return
    
    novo_video = controllers.criar_video(db, usuario_id=usuario.id, titulo=titulo, caminho=unique_filename)
    
    redirect(f'/sucesso?mensagem=Upload concluído! Vídeo salvo.')
    return

@app.route('/delete-video', method='POST')
def delete_video():
    video_id = int(request.forms.get('video_id'))
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        return "Erro: Usuário não encontrado!"
    
    video = db.query(Video).filter(Video.id == video_id, Video.usuario_id == usuario.id).first()
    
    if not video:
        return "Erro: Vídeo não encontrado ou você não tem permissão para excluí-lo!"
    
    video_path = os.path.join(UPLOAD_DIR, video.caminho)
    if os.path.exists(video_path):
        os.remove(video_path)
    
    controllers.deletar_video(db, video_id)
    
    redirect(f'/profile/{usuario.id}')
    return

@app.route('/like-video', method='POST')
def like_video():
    video_id = int(request.forms.get('video_id'))
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        redirect('/erro?tipo=Erro: Usuário não encontrado! Caso queira logar ou registrar,' +  
                 ' volte para a página home e clique para logar, ou cliquem em registrar.')
        return
    
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        return "Erro: Vídeo não encontrado!"
    
    if not controllers.verificar_like(db, usuario.id, video_id):
        controllers.incrementar_likes(db, video_id)
        controllers.adicionar_like(db, usuario.id, video_id)
    
    redirect('/home')
    return

@app.route('/comentar-video', method='POST')
def comentar_video():
    video_id = int(request.forms.get('video_id'))
    conteudo = request.forms.get('conteudo')
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        return "Erro: Usuário não encontrado!"
    
    controllers.criar_comentario(db, usuario.id, video_id, conteudo)
    
    redirect('/home')
    return  # Adicionado return após redirect

@app.route('/admin')
def admin():
    nome = request.get_cookie("nome", default="Visitante")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario or not usuario.is_admin:
        redirect('/home')
        return  # Adicionado return após redirect
    
    usuarios = db.query(Usuario).all()
    videos = db.query(Video).all()
    info = {'usuarios': usuarios, 'videos': videos}
    return ctl.render('admin', info)

@app.route('/delete-user', method='POST')
def delete_user():
    usuario_id = int(request.forms.get('usuario_id'))
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario or not usuario.is_admin:
        redirect('/erro?tipo=Permissão negada!')
        return
    
    usuario_a_deletar = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario_a_deletar:
        redirect('/erro?tipo=Usuário não encontrado!')
        return
    
    if usuario_a_deletar.nome == "admin":
        redirect('/erro?tipo=Não é permitido excluir o usuário admin!')
        return
    
    db.delete(usuario_a_deletar)
    db.commit()
    
    redirect('/admin')
    return  # Adicionado return após redirect

@app.route('/delete-video-admin', method='POST')
def delete_video_admin():
    video_id = int(request.forms.get('video_id'))
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario or not usuario.is_admin:
        return "Erro: Permissão negada!"
    
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        return "Erro: Vídeo não encontrado!"
    
    video_path = os.path.join(UPLOAD_DIR, video.caminho)
    if os.path.exists(video_path):
        os.remove(video_path)
    
    db.delete(video)
    db.commit()
    
    redirect('/admin')
    return

@app.route('/delete-conversa-2')
def delete_conversa_2():
    conversa = db.query(Conversa).filter(Conversa.id == 2).first()
    if conversa:
        db.delete(conversa)
        db.commit()
        return "Conversa com ID 2 excluída com sucesso!"
    return "Conversa com ID 2 não encontrada!"

@app.route('/erro')
def erro():
    tipo_erro = request.query.tipo
    return ctl.render('erro', tipo_erro)

@app.route('/sucesso')
def sucesso():
    mensagem_sucesso = request.query.mensagem
    return ctl.render('sucesso', mensagem_sucesso)

@app.route('/chat')
def chat():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario_logado:
        redirect('/login')
        return
    
    # Puxar as conversas do usuário
    conversas = db.query(Conversa).filter(
        (Conversa.usuario1_id == usuario_logado.id) | (Conversa.usuario2_id == usuario_logado.id)
    ).all()
    
    contatos = []
    for conversa in conversas:
        if conversa.usuario1_id == usuario_logado.id:
            contato = db.query(Usuario).filter(Usuario.id == conversa.usuario2_id).first()
        else:
            contato = db.query(Usuario).filter(Usuario.id == conversa.usuario1_id).first()
        contatos.append(contato)
    
    info = {'nome': nome, 'logado': logado, 'usuario_id': usuario_logado.id, 'contatos': contatos}
    return ctl.render('chat', info)

@app.route('/chat-<usuario_id:int>')
def chat(usuario_id):
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario_logado:
        redirect('/login')
        return
    
    # Puxar as conversas do usuário
    conversas = db.query(Conversa).filter(
        (Conversa.usuario1_id == usuario_logado.id) | (Conversa.usuario2_id == usuario_logado.id)
    ).all()
    
    contatos = []
    for conversa in conversas:
        if conversa.usuario1_id == usuario_logado.id:
            contato = db.query(Usuario).filter(Usuario.id == conversa.usuario2_id).first()
        else:
            contato = db.query(Usuario).filter(Usuario.id == conversa.usuario1_id).first()
        contatos.append(contato)
    
    info = {'nome': nome, 'logado': logado, 'usuario_id': usuario_logado.id, 'contatos': contatos}
    return ctl.render('chat', info)

@app.route('/bate-papo')
def bate_papo():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario_id = request.query.usuario_id
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        redirect('/login')
        return
    
    info = {'nome': nome, 'logado': logado, 'usuario_id': usuario.id, 'is_admin': usuario.is_admin, 'usuario': usuario}
    return ctl.render('bate_papo', info)

@app.route('/send-message', method='POST')
def send_message():
    nome = request.get_cookie("nome", default="Visitante")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario:
        return "Erro: Usuário não encontrado!"

    data = request.json
    mensagem = data.get('mensagem')
    destinatario_id = data.get('destinatario_id')

    if not mensagem or not destinatario_id:
        return "Erro: Dados da mensagem incompletos!"

    conversa = db.query(Conversa).filter(
        ((Conversa.usuario1_id == usuario.id) & (Conversa.usuario2_id == destinatario_id)) |
        ((Conversa.usuario1_id == destinatario_id) & (Conversa.usuario2_id == usuario.id))
    ).first()

    if not conversa:
        return "Erro: Conversa não encontrada!"

    # Definir o fuso horário de São Paulo
    tz = pytz.timezone('America/Sao_Paulo')
    data_envio = datetime.datetime.now(tz)

    nova_mensagem = Mensagem(
        conteudo=mensagem,
        usuario_id=usuario.id,
        conversa_id=conversa.id,
        data_envio=data_envio
    )
    db.add(nova_mensagem)
    db.commit()
    print(f"Nova mensagem criada: {nova_mensagem.id}")

    return json.dumps({'mensagem': mensagem, 'autor': usuario.nome})

@app.route('/get-messages/<destinatario_id:int>')
def get_messages(destinatario_id):
    nome = request.get_cookie("nome", default="Visitante")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario:
        response.status = 400
        return {"error": "Usuário não encontrado!"}

    conversa = db.query(Conversa).filter(
        ((Conversa.usuario1_id == usuario.id) & (Conversa.usuario2_id == destinatario_id)) |
        ((Conversa.usuario1_id == destinatario_id) & (Conversa.usuario2_id == usuario.id))
    ).first()

    if not conversa:
        return json.dumps({'mensagens': []})

    mensagens = db.query(Mensagem).filter(Mensagem.conversa_id == conversa.id).all()

    mensagens_info = [{'conteudo': mensagem.conteudo, 'autor': mensagem.usuario.nome} for mensagem in mensagens]
    response.content_type = 'application/json'
    return json.dumps({'mensagens': mensagens_info})

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)