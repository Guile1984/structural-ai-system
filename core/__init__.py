"""
Pacote: core
Descrição: Camada de domínio do sistema estrutural
Expõe as classes e funções principais do domínio
"""


from core.elements import Beam, Column, Slab, Footing, StructuralElement
from core.exceptions import (
    StructuralError,
    InvalidDimensionError,
    UnsupportedMaterialError,
    UnsupportedElementTypeError,
    ElementNotFoundError
)
from core.calculator import (
    total_volume,
    total_mass,
    total_load,
    heaviest_element,
    structural_summary
)


__all__ = [
    "Beam", "Column", "Slab", "Footing", "StructuralElement",
    "StructuralError", "InvalidDimensionError",
    "UnsupportedMaterialError", "UnsupportedElementTypeError",
    "ElementNotFoundError",
    "total_volume", "total_mass", "total_load",
    "heaviest_element", "structural_summary"
]
