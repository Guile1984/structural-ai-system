"""
Módulo: core/exceptions.py
Descrição: Exceções customizadas do domínio estrutural
"""


class StructuralError(Exception):
    """Classe base para errors do sistema estrutural."""
    pass


class InvalidDimensionError(StructuralError):
    """Erro para dimensões inválidas em elementos estruturais.

    Attributes:
        dimension: Nome da dimensão inválida.
        value: Valor inválido fornecido.
    """

    def __init__(self, dimension: str, value: float) -> None:
        """Inicializa o erro com detalhes da dimensão.

        Args:
            dimension: Nome da dimensão inválida.
            value: Valor inválido fornecido.
        """
        self.dimension = dimension
        self.value = value
        super().__init__(
            f"Invalid dimension - {dimension}: {value}. Must be positive."
        )


class UnsupportedMaterialError(StructuralError):
    """Erro para materiais não suportados.

    Attributes:
        material: Nome do material não suportado.
    """

    def __init__(self, material: str) -> None:
        """Inicializa o erro com material inválido.

        Args:
            material: Nome do material não suportado.
        """
        self.material = material
        super().__init__(
            f"Unsupported material: '{material}'. "
            f"Supported: concrete, steel, eng_wood"
        )


class UnsupportedElementTypeError(StructuralError):
    """Erro para tipos de elementos não suportados.

    Attributes:
        element_type: Tipo de elemento não suportado.
    """

    def __init__(self, element_type: str) -> None:
        """Inicializa o erro com o tipo inválido.

        Args:
            element_type: Tipo de elemento não suportado.
        """
        self.element_type = element_type
        super().__init__(
            f"Unsupported element_type: '{element_type}'. "
            f"Supported: Beam, Column, Slab, Footing"
        )


class ElementNotFoundError(StructuralError):
    """Erro quando um elemento não é encontrado.

    Attributes:
        element_id: ID do elemento não encontrado.
    """

    def __init__(self, element_id: int) -> None:
        """Inicializa o erro com o ID não encontrado.

        Args:
            element_id: ID do elemento buscado.
        """
        self.element_id = element_id
        super().__init__(f"Element with id={element_id} not found.")

