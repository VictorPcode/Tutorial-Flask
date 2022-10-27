from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return auth.get(user_id)    
#este arreglo se hizo siguiendo la documentacion donde originalmente buscar
# el user, return User.get(user_id). Mientras que con auth.get(user_id) 
# busca la validacion dentro de la DB 
@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app = Flask(__name__,template_folder="template", static_folder="static")
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    
    app.register_blueprint(auth)
    
    return app 