"""
Módulo: api/validators.py
Descrição: Validação de dados de entrada nas requisições da API
"""

from core.elements import StructuralElement

VALID_TYPES = ["Beam", "Column", "Slab", "Footing"]
VALID_MATERIALS = StructuralElement.SUPPORTED_MATERIALS
REQUIRED_FIELDS: dict[str, list[str]] = {
    "Beam": ["length", "width", "height", "material"],
    "Column": ["height", "section", "material"],
    "Slab": ["length", "width", "thickness", "material"],
    "Footing": ["length", "width", "depth", "material"],
}


def validate_element(data: dict) -> list[str]:
    """Valida os dados de um novo elemento estrutural.

    Args:
        data: Dicionário com os dados recebidos na requisição.

    Returns:
        Lista de erros encontrados. Vazia se válido.
    """
    errors = []

    if not data:
        return ["Request body is empty or invalid JSON."]

    element_type = data.get("type")
    if not element_type:
        errors.append("Field 'type' is required.")
        return errors

    if element_type not in VALID_TYPES:
        errors.append(f"Invalid type '{element_type}'. Valid types: {VALID_TYPES}")
        return errors

    material = data.get("material")
    if not material:
        errors.append("Field 'material' is required.")
    elif material not in VALID_MATERIALS:
        errors.append(f"Invalid material '{material}'. Valid materials: {VALID_MATERIALS}")

    required = REQUIRED_FIELDS[element_type]
    for field in required:
        if field == "material":
            continue
        value = data.get(field)
        if value is None:
            errors.append(f"Field '{field}' is required for {element_type}.")
        elif not isinstance(value, (int | float)):
            errors.append(f"Field '{field}' must be a number.")
        elif value <= 0:
            errors.append(f"Field '{field}' must be positive.")

    return errors
