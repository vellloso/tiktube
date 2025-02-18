from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'login': self.login,
            'register': self.register,
            'home': self.home
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')
    
    def login(self):
        return template('app/views/html/login')
    
    def register(self):
        return template('app/views/html/register')
    
    def home(self):
        return template('app/views/html/home')