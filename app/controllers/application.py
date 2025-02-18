from bottle import template

class Application:
    def __init__(self):
        self.pages = {
            'login': self.login,
            'register': self.register,
            'home': self.home,
            'helper': self.helper,
            'upload': self.upload
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
    
    def upload(self, info=None):
        return template('app/views/html/upload')