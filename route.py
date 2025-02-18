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

@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')

#-----------------------------------------------------------------------------
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
    return ctl.render('home', info)

@app.route('/validar-login', method='POST')
def validarLogin():
    form_data = request.forms        
    # Processar os dados do formulário
    nome = form_data.get('username')
    senha = form_data.get('password')
    
    usuario = controllers.autenticar_usuario(db, nome=nome, senha=senha)
    if usuario is None:
        redirect('/login')

    # Codificar o campo para evitar problemas com caracteres especiais
    print("NOME: " + nome)
    print("SENHA: " + senha)
    # Define cookies
    response.set_cookie("nome", nome, path="/")
    response.set_cookie("logado", "SIM", path="/")
    redirect('/home')

@app.route('/validar-registro', method='POST')
def validarCadastro():
    form_data = request.forms        
    # Processar os dados do formulário
    nome = form_data.get('username')
    senha = form_data.get('password')
    
    usuario1 = controllers.criar_usuario(db, nome=nome, senha=senha)
    # Codificar o campo para evitar problemas com caracteres especiais
    print("NOME: " + nome)
    print("SENHA: " + senha)
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

@app.route('/profile')
def profile():
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    if logado == "SIM":
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
        if usuario:
            redirect(f'/profile/{usuario.id}')
    else:
        redirect('/login')

@app.route('/profile/<usuario_id:int>')
def view_profile(usuario_id):
    nome = request.get_cookie("nome", default="Visitante")
    logado = request.get_cookie("logado", default="NAO")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if usuario:
        is_self = usuario_logado and usuario_logado.id == usuario.id
        is_following = db.query(Seguidor).filter(Seguidor.usuario_id == usuario_logado.id, Seguidor.seguindo_id == usuario.id).first() is not None
        videos = db.query(Video).filter(Video.usuario_id == usuario.id).all()
        info = {
            'nome': usuario.nome,
            'seguidores': usuario.seguidores,
            'seguindo': usuario.seguindo,
            'is_self': is_self,
            'is_following': is_following,
            'usuario_id': usuario.id,
            'videos': [{'titulo': video.titulo, 'caminho': video.caminho, 'descricao': 'Descrição do vídeo...', 'comentarios': ['Comentário 1...', 'Comentário 2...']} for video in videos]
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
    
    redirect(f'/profile/{usuario_id}')

@app.route('/unfollow', method='POST')
def unfollow():
    usuario_id = int(request.forms.get('usuario_id'))
    nome = request.get_cookie("nome", default="Visitante")
    usuario_logado = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if usuario_logado:
        controllers.remover_seguidor(db, usuario_logado.id, usuario_id)
        controllers.decrementar_seguidores(db, usuario_id)
        controllers.decrementar_seguindo(db, usuario_logado.id)
    
    redirect(f'/profile/{usuario_id}')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)