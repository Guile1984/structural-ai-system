"""
Módulo: api/__init__.py
Descrição: Application Factory do Flask
"""

from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app() -> Flask:
    """Cria e configura a aplicação Flask.

    Returns:
        Instância configurada do Flask.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "dev-secret-key"
    )
    app.config["JSON_SORT_KEYS"] = False

    from api.routes import api_bp
    app.register_blueprint(api_bp)

    return app