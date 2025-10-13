import os
from flask import Flask
from dotenv import load_dotenv
from .models import db

load_dotenv()  # loads .env

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Basic config
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GOOGLE_MAPS_API_KEY'] = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # Build DB URI
    db_user = os.getenv("DB_USER", "root")
    db_pass = os.getenv("DB_PASS", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "parksmart")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"

    # Session cookie security flags
    use_https = os.getenv("USE_HTTPS", "0") == "1"
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = use_https

    db.init_app(app)

    # register routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
