"""
Arquivo: main.py
Projeto: structural-ai-system
Descrição: Ponto de entrada principal do sistema
Autor: Guilherme
Versão: 1.0.0
"""

import argparse


def main() -> None:
    """Ponto de entrada principal do sistema.

    Permite iniciar diferentes componentes via linha de comando:
        python main.py --api    -> inicia a API REST
        python main.py --dashboard -> inicia o dashboard
        python main.py --train  -> treina os modelos ML
        python main.py --report -> gera relatório manual
    """
    parser = argparse.ArgumentParser(
        description="Structural AI System - Sistema de Análise Estrutural com ML"
    )
    parser.add_argument("--api", action="store_true", help="Inicia a API REST Flask")
    parser.add_argument("--dashboard", action="store_true", help="Inicia o Dashboard Streamlit")
    parser.add_argument("--train", action="store_true", help="Treina os modelos ML")
    parser.add_argument("--report", action="store_true", help="Gera relatórios manual")

    args = parser.parse_args()

    if args.api:
        print("Iniciando API REST...")
        from api import create_app
        app = create_app()
        app.run(debug=True, port=5000)

    elif args.dashboard:
        print("Iniciando Dashboard...")
        import subprocess
        subprocess.run(["streamlit", "run", "dashboard/app.py"])

    elif args.train:
        print("Treinando modelos ML...")
        from ml.pipeline import treinar_pipeline
        treinar_pipeline()

    elif args.report:
        print("Gerando relatório...")
        from automation.reporter import gerar_relatorio_manual
        gerar_relatorio_manual()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
