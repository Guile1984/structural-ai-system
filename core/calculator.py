"""
Módulo: core/calculator.py
Descrição: Funções de cálculo estrutural do domínio
"""


from core.elements import StructuralElement


def total_volume(elements: list[StructuralElement]) -> float:
    """Calcula o volume total de uma lista de elementos.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Volume total em metros cúbicos.
    """
    return round(sum(e.calculate_volume() for e in elements), 4)


def total_mass(elements: list[StructuralElement]) -> float:
    """Calcula a massa total de uma lista de elementos.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Massa total em quilogramas.
    """
    return round(sum(e.calculate_mass() for e in elements), 2)


def total_load(elements: list[StructuralElement]) -> float:
    """Calcula a carga total de uma lista de elementos.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Carga total em Newtons.
    """
    return round(sum(e.calculate_load() for e in elements), 2)


def heaviest_element(elements: list[StructuralElement]) -> StructuralElement | None:
    """Retorna o elemento de maior massa.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Elemento com maior massa ou None se lista vazia.
    """
    if not elements:
        return None
    return max(elements, key=lambda e: e.calculate_mass())


def elements_by_material(
        elements: list[StructuralElement]
) -> dict[str, list[StructuralElement]]:
    """Agrupa elementos por material.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Dicionário com material com chave e lista de elementos como valor.
    """
    result: dict[str, list[StructuralElement]] = {}
    for element in elements:
        if element.material not in result:
            result[element.material] = []
        result[element.material].append(element)
    return result


def structural_summary(elements: list[StructuralElement]) -> dict:
    """Gera um resumo completo da estrutura.

    Args:
        elements: Lista de elementos estruturais.

    Returns:
        Dicionário com resumo estatístico da estrutura.
    """
    if not elements:
        return {"error:": "No elements provided."}

    by_material = elements_by_material(elements)
    heaviest = heaviest_element(elements)

    return {
        "total_elements": len(elements),
        "total_volume_m³": total_volume(elements),
        "total_mass_kg": total_mass(elements),
        "total_load_n": total_load(elements),
        "total_load_kn": round(total_load(elements) / 1000, 2),
        "heaviest_element": str(heaviest) if heaviest else None,
        "by_material": {
            mat: len(elems) for mat, elems in by_material.items()
        },
        "average_volume_m³": round(
            total_volume(elements) / len(elements), 4
        )
    }