from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

#login manager messages and config
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You must be logged in to access this page!'
login_manager.login_message_category = 'danger'

#import my blueporint onto app
from app.blueprints.auth import auth
from app.blueprints.main import main

#register blueprint onto the app
app.register_blueprint(auth)
app.register_blueprint(main)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)