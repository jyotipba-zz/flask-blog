from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()

login.login_view = 'users.login'

mail = Mail()




def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    mail.init_app(app)


    from my_blog.main.routes import main
    from my_blog.posts.routes import posts
    from my_blog.users.routes import users
    from my_blog.error.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
