from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from admin_page import AdminView
#from my_blog.models import User


db = SQLAlchemy()
admin = Admin()
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
    from my_blog.models import User,Post
    admin.init_app(app)
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Post, db.session))

    # Initialize the SQLAlchemy data store and Flask-Security.
    #user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    #security = Security(app, user_datastore)



    from my_blog.main.routes import main
    from my_blog.posts.routes import posts
    from my_blog.users.routes import users
    from my_blog.error.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)


    return app
