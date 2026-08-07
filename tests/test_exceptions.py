"""
Módulo: tests/test_exceptions.py
Descrição: Testes das exceções customizadas do domínio
"""

from core.exceptions import (
    ElementNotFoundError,
    InvalidDimensionError,
    StructuralError,
    UnsupportedElementTypeError,
    UnsupportedMaterialError,
)


class TestInvalidDimensionError:
    """Testes para InvalidDimensionError."""

    def test_inherits_structural_error(self):
        """Verifica que herda de StructuralError."""
        error = InvalidDimensionError("length", -1.0)
        assert isinstance(error, StructuralError)

    def test_stores_dimension_name(self):
        """Verifica que armazena o nome da dimensão."""
        error = InvalidDimensionError("width", -0.5)
        assert error.dimension == "width"

    def test_stores_value(self):
        """Verifica que armazena o valor inválido."""
        error = InvalidDimensionError("height", 0)
        assert error.value == 0

    def test_message_contains_dimension(self):
        """Verifica que a mensagem inclui a dimensão."""
        error = InvalidDimensionError("length", -3.0)
        assert "length" in str(error)
        assert "-3.0" in str(error)


class TestUnsupportedMaterialError:
    """Testes para UnsupportedMaterialError."""

    def test_inherits_structural_error(self):
        """Testes para UnsupportedMaterialError."""

        def test_inherits_structural_error(self):
            """Verifica que herda de StructuralError."""
            error = UnsupportedMaterialError("wood")
            assert isinstance(error, StructuralError)

        def test_stores_material(self):
            """Verifica que armazena o material inválido."""
            error = UnsupportedMaterialError("glass")
            assert error.material == "glass"

        def test_message_contains_material(self):
            """Verifica que a mensagem inclui o material."""
            error = UnsupportedMaterialError("brick")
            assert "brick" in str(error)


class TestUnsupportedElementTypeError:
    """Testes para UnsupportedElementTypeError."""

    def test_stores_element_type(self):
        """Verifica que armazena o tipo inválido."""
        error = UnsupportedElementTypeError("Wall")
        assert error.element_type == "Wall"


class TestElementNotFoundError:
    """Testes para ElementNotFoundError."""

    def test_stores_element_id(self):
        """Verifica que armazena o ID não encontrado."""
        error = ElementNotFoundError(42)
        assert error.element_id == 42

    def test_message_contains_id(self):
        """Verifica que a mensagem inclui o ID."""
        error = ElementNotFoundError(99)
        assert "99" in str(error)
