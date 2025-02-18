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

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)