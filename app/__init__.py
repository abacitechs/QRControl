from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object('config')  # Load configurations from config.py

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to 'auth.login' if not authenticated

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))  # Fetch user by ID

    # Register blueprints
    from .views.auth import auth_bp
    from .views.system import system_bp
    from .views.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(main_bp)

    # Create database tables and default user
    with app.app_context():
        db.create_all()  # Create all tables if they do not exist

        # Create default admin user if not present
        from .models import User
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            hashed_password = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_user = User(username="admin", password=hashed_password)
            db.session.add(admin_user)
            db.session.commit()

    return app
