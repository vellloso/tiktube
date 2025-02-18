import os
from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, response, template
from urllib.parse import quote, unquote
from app.controllers.db.database import engine, Base, SessionLocal
from app.models.usuario import Usuario
from app.models.seguidor import Seguidor
from app.models.video import Video
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.notificacao import Notificacao
from app.controllers import controllers

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'app', 'controllers', 'db', 'videos')

app = Bottle()
ctl = Application()
Base.metadata.create_all(bind=engine)
# Cria uma sessão para interagir com o banco de dados
db = SessionLocal()

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
    # Recupera cookies
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    info = {'nome': nome, 'logado': logado}
    videos = controllers.listar_videos(db)
    return ctl.render('home', {'info': info, 'videos': videos})

@app.route('/validar-login', method='POST')
def validarLogin():
    form_data = request.forms        
    # Processar os dados do formulário
    nome = form_data.get('username')
    senha = form_data.get('password')
    # Verifique se o usuário existe no banco de dados
    usuario = db.query(Usuario).filter(Usuario.nome == nome, Usuario.senha == senha).first()
    if usuario:
        # Define cookies
        response.set_cookie("nome", nome, path="/")
        response.set_cookie("logado", "SIM", path="/")
        redirect('/home')
    else:
        return "Nome de usuário ou senha incorretos!"

@app.route('/validar-registro', method='POST')
def validarCadastro():
    form_data = request.forms        
    # Processar os dados do formulário
    nome = form_data.get('username')
    senha = form_data.get('password')
    # Verifique se o usuário já existe no banco de dados
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if usuario:
        return "O nome de usuário já existe!"
    else:
        # Exemplo de criação de usuários
        usuario1 = controllers.criar_usuario(db, gmail=nome, nome=nome, senha=senha)
        # Define cookies
        response.set_cookie("nome", nome, path="/")
        response.set_cookie("logado", "SIM", path="/")
        redirect('/home')

@app.route('/logout')
def logout():
    # Limpa cookies
    response.set_cookie("nome", "", expires=0)
    response.set_cookie("logado", "", expires=0)
    redirect('/home')

@app.route('/upload')
def upload():
    nome = request.get_cookie("nome")
    logado = request.get_cookie("logado")
    if logado == "SIM":
        return ctl.render('upload')
    else:
        return "Você precisa estar logado para fazer upload de vídeos."

@app.route('/upload-video', method='POST')
def upload_video():
    titulo = request.forms.get('titulo')
    video = request.files.get('video')
    
    # Verifique se o diretório de upload existe, caso contrário, crie-o
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    # Salve o vídeo na pasta de uploads com permissões adequadas
    video_path = os.path.join(UPLOAD_DIR, video.filename)
    video.save(video_path)
    os.chmod(video_path, 0o644)
    
    # Obtenha o usuário atual a partir do cookie
    nome = request.get_cookie("nome")
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        return "Erro: Usuário não encontrado!"
    
    # Adicione o vídeo ao banco de dados
    novo_video = controllers.criar_video(db, usuario_id=usuario.id, titulo=titulo, caminho=video.filename)
    
    return f"Upload concluído! Vídeo salvo em: {video_path}"

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)