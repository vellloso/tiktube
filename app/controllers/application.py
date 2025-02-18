from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'login': self.login
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')
    
    def login(self):
        return template('app/views/html/login')
