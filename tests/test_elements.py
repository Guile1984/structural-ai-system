"""
Módulo: tests/test_elements.py
Descrição: Testes das classes de elementos estruturais
"""

import pytest

from core.elements import Beam, Column, Footing, Slab, StructuralElement
from core.exceptions import InvalidDimensionError, UnsupportedMaterialError


class TestBeam:
    """Testes para a classe Beam."""

    def test_create_default_material(self):
        """Verifica criação com material padrão (concrete)."""
        beam = Beam(6.0, 0.3, 0.5)
        assert beam.material == "concrete"

    def test_create_with_steel(self):
        """Verifica criação com aço."""
        beam = Beam(4.0, 0.2, 0.4, "steel")
        assert beam.material == "steel"

    def test_calculate_volume(self):
        """Verifica cálculo de volume."""
        beam = Beam(6.0, 0.3, 0.5)
        assert beam.calculate_volume() == 0.9

    def test_calculate_mass_concrete(self):
        """Verifica cálculo de massa com concreto."""
        beam = Beam(6.0, 0.3, 0.5)
        assert beam.calculate_mass() == 0.9 * 2500.0

    def test_calculate_mass_steel(self):
        """Verifica cálculo de massa com aço."""
        beam = Beam(6.0, 0.3, 0.5, "steel")
        assert beam.calculate_mass() == 0.9 * 7850.0

    def test_calculate_load(self):
        """Veririca cálculo de carga."""
        beam = Beam(6.0, 0.3, 0.5)
        expected = 0.9 * 2500.0 * 9.81
        assert beam.calculate_load() == expected

    def test_to_dict_has_required_keys(self):
        """Verifica que to_dict retorna todas as chaves."""
        beam = Beam(6.0, 0.3, 0.5)
        data = beam.to_dict()
        required = ["type", "material", "length", "width", "height", "volume", "mass_kg", "load_n"]
        for key in required:
            assert key in data

    def test_to_dict_type_is_string(self):
        """Verifica que type é string, não classe."""
        beam = Beam(6.0, 0.3, 0.5)
        assert beam.to_dict()["type"] == "Beam"
        assert isinstance(beam.to_dict()["type"], str)

    def test_from_dict_reconstructs(self):
        """Verifica que from_dict reconstrói o objeto."""
        original = Beam(6.0, 0.3, 0.5)
        data = original.to_dict()
        reconstructed = StructuralElement.from_dict(data)
        assert reconstructed.calculate_volume() == original.calculate_volume()

    def test_invalid_length_raises(self):
        """Verifica que comprimento inválido lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Beam(-1.0, 0.3, 0.5)

    def test_invalid_width_raises(self):
        """Verifica que largura inválida lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Beam(6.0, 0, 0.5)

    def test_invalid_height_raises(self):
        """Verifica que altura inválida lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Beam(6.0, 0.3, -0.5)

    def test_unsupported_material_raises(self):
        """Verifica que material inválido lança exceção."""
        with pytest.raises(UnsupportedMaterialError):
            Beam(6.0, 0.3, 0.5, "brick")

    def test_str_contains_beam(self):
        """Verifica que __str__ contém BEAM."""
        beam = Beam(6.0, 0.3, 0.5)
        assert "BEAM" in str(beam)

    def test_comparison_lt(self):
        """Verifica comparação por volume."""
        small = Beam(2.0, 0.2, 0.3)
        large = Beam(6.0, 0.3, 0.5)
        assert small < large

    def test_comparison_eq(self):
        """Verifica igualdade por volume"""
        a = Beam(6.0, 0.3, 0.5)
        b = Beam(3.0, 0.6, 0.5)
        assert a == b


class TestColumn:
    """Testes para a classe Column."""

    def test_calculate_volume(self):
        """Verifica cálculo de volume."""
        column = Column(3.0, 0.4)
        assert column.calculate_volume() == 0.48

    def test_to_dict_type(self):
        """Verifica que type retorna 'Column'."""
        column = Column(3.0, 0.4)
        assert column.to_dict()["type"] == "Column"

    def test_invalid_section_raises(self):
        """Verifica que seção inválida lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Column(3.0, -0.4)


class TestSlab:
    """Testes para a classe Slab."""

    def test_calculate_volume(self):
        """Verifica cálculo de volume."""
        slab = Slab(5.0, 4.0, 0.12)
        assert slab.calculate_volume() == 2.4

    def test_to_dict_type(self):
        """Verifica que type retorna 'Slab'."""
        slab = Slab(5.0, 4.0, 0.12)
        assert slab.to_dict()["type"] == "Slab"

    def test_invalid_thickness_raises(self):
        """Verifica que espessura inválida lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Slab(5.0, 4.0, 0)


class TestFooting:
    """Testes para a classe Footing."""

    def test_calculate_volume(self):
        """Verifica cálculo de volume."""
        footing = Footing(1.0, 1.0, 0.4)
        assert footing.calculate_volume() == 0.4

    def test_to_dict_type(self):
        """Verifica que type retorna 'Footing'."""
        footing = Footing(1.0, 1.0, 0.4)
        assert footing.to_dict()["type"] == "Footing"

    def test_invalid_depth_raises(self):
        """Verifica que profundidade inválida lança exceção."""
        with pytest.raises(InvalidDimensionError):
            Footing(1.0, 1.0, -0.4)
