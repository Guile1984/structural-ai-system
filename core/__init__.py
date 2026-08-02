"""
Pacote: core
Descrição: Camada de domínio do sistema estrutural
Expõe as classes e funções principais do domínio
"""


from core.calculator import (
    heaviest_element,
    structural_summary,
    total_load,
    total_mass,
    total_volume,
)
from core.elements import Beam, Column, Footing, Slab, StructuralElement
from core.exceptions import (
    ElementNotFoundError,
    InvalidDimensionError,
    StructuralError,
    UnsupportedElementTypeError,
    UnsupportedMaterialError,
)

__all__ = [
    "Beam", "Column", "Slab", "Footing", "StructuralElement",
    "StructuralError", "InvalidDimensionError",
    "UnsupportedMaterialError", "UnsupportedElementTypeError",
    "ElementNotFoundError",
    "total_volume", "total_mass", "total_load",
    "heaviest_element", "structural_summary"
]
