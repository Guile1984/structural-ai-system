"""
Módulo: tests/test_calculator.py
Descrição: Testes das funções de cálculo estrutural
"""

import pytest

from core.calculator import (
    elements_by_material,
    heaviest_element,
    structural_summary,
    total_load,
    total_mass,
    total_volume,
)
from core.elements import Beam, Column, Footing, Slab


@pytest.fixture
def sample_elements():
    """Fixture com elementos de teste reutilizáveis."""
    return [Beam(6.0, 0.3, 0.5), Column(3.0, 0.4), Slab(5.0, 4.0, 0.12), Footing(1.0, 1.0, 0.4)]


class TestTotalVolume:
    """Testes para total_volume."""

    def test_calculates_sum(self, sample_elements):
        """Verifica a soma de volumes."""
        result = total_volume(sample_elements)
        expected = 0.9 + 0.48 + 2.4 + 0.4
        assert result == round(expected, 4)

    def test_empty_list(self):
        """Verifica com lista vazia."""
        assert total_volume([]) == 0


class TestTotalMass:
    """Testes para total_mass."""

    def test_calculates_sum(self, sample_elements):
        """Verifica soma de massas."""
        result = total_mass(sample_elements)
        assert result > 0

    def test_empty_list(self):
        """Verifica com lista vazia"""
        assert total_mass([]) == 0


class TestTotalLoad:
    """Testes para total_load."""

    def test_calculates_sum(self, sample_elements):
        """Verifica soma de cargas."""
        result = total_load(sample_elements)
        assert result > 0


class TestHeaviestElement:
    """Testes para heaviest_element."""

    def test_finds_heaviest(self, sample_elements):
        """Verifica que encontra o mais pesado."""
        result = heaviest_element(sample_elements)
        assert "SLAB" in str(result)

    def test_empty_list(self):
        """Verifica com lista vazia."""
        assert heaviest_element([]) is None


class TestElementsByMaterial:
    """Testes para elements_by_material."""

    def test_groups_correctly(self, sample_elements):
        """Verifica agrupamento por material."""
        result = elements_by_material(sample_elements)
        assert "concrete" in result
        assert len(result["concrete"]) == 4

    def test_mixed_materials(self):
        """Verifica agrupamento com materiais mistos."""
        elements = [Beam(6.0, 0.3, 0.5, "concrete"), Beam(4.0, 0.2, 0.4, "steel")]
        result = elements_by_material(elements)
        assert len(result["concrete"]) == 1
        assert len(result["steel"]) == 1


class TestStructuralSummary:
    """Testes para structural_summary."""

    def test_has_required_keys(self, sample_elements):
        """Verifica que o resumo contém todas as chaves."""
        result = structural_summary(sample_elements)
        required = [
            "total_elements",
            "total_volume_m3",
            "total_mass_kg",
            "total_load_n",
            "heaviest_element",
            "by_material",
        ]
        for key in required:
            assert key in result

    def test_total_elements_count(self, sample_elements):
        """Verifica contagem total."""
        result = structural_summary(sample_elements)
        assert result["total_elements"] == 4

    def test_empty_list(self):
        """Verifica com lista vazia."""
        result = structural_summary([])
        assert "error" in result
