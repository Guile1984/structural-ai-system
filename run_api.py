"""
Arquivo: run_api.py
Descrição: Inicializa a API REST do sistema estrutural
"""

import os

from api import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", "5000"))
    print(f"API rodando em http://127.0.0.1:{port}/api/v1")
    app.run(debug=True, port=port)
