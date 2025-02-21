from bottle import template

class Application:
    def __init__(self):
        self.pages = {
            'login': self.login,
            'register': self.register,
            'home': self.home,
            'helper': self.helper,
            'profile': self.profile,
            'admin': self.admin,
            'chat': self.render_chat,
            'erro': self.erro,
            'sucesso': self.sucesso,
            'bate_papo': self.bate_papo  
        }

    def render(self, page, info=None):
        content = self.pages.get(page, self.helper)
        if info:
            return content(info)  
        else: 
            return content()

    def helper(self, info=None):
        return template('app/views/html/helper')

    def login(self, info=None):
        return template('app/views/html/login')

    def register(self, info=None):
        return template('app/views/html/register')

    def home(self, info=None):
        return template('app/views/html/home', info=info)
    
    def profile(self, info=None):
        return template('app/views/html/profile', info=info)

    def admin(self, info=None):
        return template('app/views/html/admin', info=info)

    def render_chat(self, info=None):
        return template('app/views/html/chat', info=info)
    
    def erro(self, info=None):
        return template('app/views/html/erro', info=info)
    
    def sucesso(self, info=None):
        return template('app/views/html/sucesso', info=info) 
    
    def  bate_papo(self, info=None):
        return template('app/views/html/bate_papo.tpl', info=info)