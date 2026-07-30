"""
Módulo: api/routes.py
Descrição: Rotas e controllers da API REST estrutural
"""

import json
from datetime import datetime
from pathlib import Path
from flask import Blueprint, request, jsonify
from core import (
    Beam, Column, Slab, Footing,
    StructuralElement, ElementNotFoundError,
    structural_summary
)
from api.validators import validate_element

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

DATA_FILE = Path("data/elements.json")


def _response(
    data: dict | list | None = None,
    error: str | None = None,
    status: int = 200
):
    """Gera resposta JSON padronizada.

    Args:
        data: Dados a retornar.
        error: Mensagem de erro.
        status: Código HTTP.

    Returns:
        Tupla com JSON e status.
    """
    return jsonify({
        "success": error is None,
        "data": data,
        "error": error,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), status


def _load_elements() -> list[dict]:
    """Carrega elementos do arquivo JSON.

    Returns:
        Lista de dicionários com os elementos.
    """
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_elements(elements: list[dict]) -> None:
    """Salva elementos no arquivo JSON.

    Args:
        elements: Lista de dicionários a salvar.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(elements, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def _build_element(data: dict) -> StructuralElement:
    """Constrói um elemento estrutural a partir de um dicionário.

    Args:
        data: Dicionário com os dados do elemento.

    Returns:
        Instância do elemento estrutural.
    """
    t = data["type"]
    m = data["material"]
    if t == "Beam":
        return Beam(data["length"], data["width"], data["height"], m)
    elif t == "Column":
        return Column(data["height"], data["section"], m)
    elif t == "Slab":
        return Slab(data["length"], data["width"], data["thickness"], m)
    elif t == "Footing":
        return Footing(data["length"], data["width"], data["depth"], m)


@api_bp.route("/health", methods=["GET"])
def health():
    """Retorna status da API.

    Returns:
        JSON com informações do sistema.
    """
    elements = _load_elements()
    return _response(data={
        "status": "online",
        "version": "1.0.0",
        "project": "structural-ai-system",
        "total_elements": len(elements)
    })


@api_bp.route("/elements", methods=["GET"])
def list_elements():
    """Lista todos os elementos cadastrados.

    Returns:
        JSON com lista e total de elementos.
    """
    elements = _load_elements()
    return _response(data={
        "total": len(elements),
        "elements": elements
    })


@api_bp.route("/elements/<int:element_id>", methods=["GET"])
def get_element(element_id: int):
    """Busca um elemento pelo ID.

    Args:
        element_id: Identificador do elemento.

    Returns:
        JSON com o elemento ou erro 404.
    """
    elements = _load_elements()
    for element in elements:
        if element.get("id") == element_id:
            return _response(data=element)
    return _response(
        error=f"Element with id={element_id} not found.",
        status=404
    )


@api_bp.route("/elements/type/<string:element_type>", methods=["GET"])
def filter_by_type(element_type: str):
    """Filtra elementos por tipo.

    Args:
        element_type: Tipo do elemento (Beam, Column, Slab, Footing).

    Returns:
        JSON com elementos filtrados.
    """
    elements = _load_elements()
    filtered = [
        e for e in elements
        if e.get("type", "").lower() == element_type.lower()
    ]
    return _response(data={
        "type": element_type,
        "total": len(filtered),
        "elements": filtered
    })


@api_bp.route("/elements", methods=["POST"])
def create_element():
    """Cria um novo elemento estrutural.

    Returns:
        JSON com elemento criado ou erros de validação.
    """
    data = request.get_json()
    errors = validate_element(data)
    if errors:
        return _response(error=errors, status=400)

    try:
        element = _build_element(data)
        elements = _load_elements()
        new_id = max((e.get("id", 0) for e in elements), default=0) + 1
        element_dict = element.to_dict()
        element_dict["id"] = new_id
        elements.append(element_dict)
        _save_elements(elements)
        return _response(data=element_dict, status=201)
    except Exception as e:
        return _response(error=str(e), status=400)


@api_bp.route("/elements/<int:element_id>", methods=["DELETE"])
def delete_element(element_id: int):
    """Remove um elemento pelo ID.

    Args:
        element_id: Identificador do elemento.

    Returns:
        JSON confirmando remoção ou erro 404.
    """
    elements = _load_elements()
    for element in elements:
        if element.get("id") == element_id:
            elements.remove(element)
            _save_elements(elements)
            return _response(data={
                "message": f"Element {element_id} deleted successfully."
            })
    return _response(
        error=f"Element with id={element_id} not found.",
        status=404
    )


@api_bp.route("/summary", methods=["GET"])
def get_summary():
    """Retorna resumo estrutural completo.

    Returns:
        JSON com estatísticas da estrutura.
    """
    raw = _load_elements()
    if not raw:
        return _response(
            error="No elements registered.",
            status=404
        )

    elements = [_build_element(e) for e in raw]
    summary = structural_summary(elements)
    return _response(data=summary)


@api_bp.errorhandler(404)
def not_found(error):
    """Trata rotas inexistentes."""
    return _response(error="Route not found.", status=404)


@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Trata métodos não permitidos."""
    return _response(error="Method not allowed.", status=405)