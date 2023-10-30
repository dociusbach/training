from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "hohtrainingapp.db"


def app_begin():

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'callfromsecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hohtrainingapp.db'
    

    db.init_app(app)
   

    from .locations import location
    from .auth import auth
    

    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .dbmodels import User, Group, UserGroup, Competition, CompetitionGroup

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader

    def load_user(id):
        return User.query.get(int(id)) 

    return app


