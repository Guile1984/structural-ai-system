"""
Módulo: core/elements.py
Descrição: Classes de elementos estruturais do domínio
"""

from __future__ import annotations

from core.exceptions import (
    InvalidDimensionError,
    UnsupportedElementTypeError,
    UnsupportedMaterialError,
)


class StructuralElement:
    """Classe base abstrata para elementos estruturais.

    Attributes:
        SUPPORTED_MATERIALS: Materiais suportados pelo sistema.
        _material: Material do elemento.
        _length: Comprimento principal em metros.
    """

    SUPPORTED_MATERIALS: list[str] = ["concrete", "steel", "eng_wood"]
    DENSITY: dict[str, float] = {"concrete": 2500.0, "steel": 7850.0, "eng_wood": 600.0}

    def __init__(self, material: str, length: float) -> None:
        """Inicializa um elemento estrutural.

        Args:
            material: Material do elemento.
            length: Comprimento principal em metros.

        Raises:
            UnsupportedMaterialError: Se o material não for suportado.
            InvalidDimensionError: Se o comprimento for inválido.
        """
        if material not in self.SUPPORTED_MATERIALS:
            raise UnsupportedMaterialError(material)
        if length <= 0:
            raise InvalidDimensionError("length", length)

        self._material = material
        self._length = length

    @property
    def material(self) -> str:
        """Retorna o material do elemento."""
        return self._material

    @property
    def length(self) -> float:
        """Retorna o comprimento do elemento."""
        return self._length

    @property
    def density(self) -> float:
        """Retorna a densidade do material em kg/m³."""
        return self.DENSITY[self._material]

    def calculate_volume(self) -> float:
        """Calcula o volume do elemento.

        Raises:
            NotImplementedError: Se a subclasse não implementar.
        """
        raise NotImplementedError("Subclasses must implement calculate_volume.")

    def calculate_mass(self) -> float:
        """Calculate a massa do elemento em kg.

        Returns:
            Massa em quilogramas.
        """
        return self.calculate_volume() * self.density

    def calculate_load(self, gravity: float = 9.81) -> float:
        """Calcula a carga gerada pelo peso do elemento.

        Args:
            gravity: Aceleração gravitacional em m/s². Padrão: 9.81.

        Returns:
            Carga em Newtons.
        """
        return self.calculate_mass() * gravity

    def to_dict(self) -> dict:
        """Serializa o elemento para dicionário.

        Raises:
            NotImplementedError: Se a subclasse não implementar.
        """
        raise NotImplementedError("Subclasses must be implement to_dict.")

    @classmethod
    def from_dict(cls, data: dict) -> StructuralElement:
        """Reconstrói um elemento a partir de um dicionário.

        Args:
            data: Dicionário com os dados do elemento.

        Returns:
            Instância do elemento reconstruído.

        Raises:
            UnsupportedElementTypeError: Se o tipo for desconhecido.
        """
        element_type = data.get("type")
        if element_type == "Beam":
            return Beam(data["length"], data["width"], data["height"], data["material"])
        elif element_type == "Column":
            return Column(data["height"], data["section"], data["material"])
        elif element_type == "Slab":
            return Slab(data["length"], data["width"], data["thickness"], data["material"])
        elif element_type == "Footing":
            return Footing(data["length"], data["width"], data["depth", data["material"]])
        else:
            raise UnsupportedElementTypeError(element_type)

    def __lt__(self, other: StructuralElement) -> bool:
        """Compara elementos pelo volume."""
        return self.calculate_volume() < other.calculate_volume()

    def __eq__(self, other: object) -> bool:
        """Compara elementos pelo volume."""
        if not isinstance(other, StructuralElement):
            return False
        return self.calculate_volume() == other.calculate_volume()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(material={self._material})"


class Beam(StructuralElement):
    """Viga estrutural.

    Attributes:
        _width: Largura da viga em metros.
        _height: Altura da viga em metros.
    """

    def __init__(
        self, length: float, width: float, height: float, material: str = "concrete"
    ) -> None:
        """Inicializa uma viga estrutural.

        Args:
            length: Comprimento em metros.
            width: Largura em metros.
            height: Altura em metros.
            material: Material da viga. Padrão: concrete.

        Raises:
            InvalidDimensionError: Se alguma dimensão for inválida.
        """
        super().__init__(material, length)
        if width <= 0:
            raise InvalidDimensionError("width", width)
        if height <= 0:
            raise InvalidDimensionError("height", height)
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        """Retorna a largura da viga."""
        return self._width

    @property
    def height(self) -> float:
        """Retorna a altura da viga."""
        return self._height

    def calculate_volume(self) -> float:
        """Calcula o volume da viga.

        Returns:
            Volume em metros cúbicos.
        """
        return round(self._length * self._width * self._height, 4)

    def to_dict(self) -> dict:
        """Serializa a viga para dicionário.

        Returns:
            Dicionário com os dados da viga.
        """
        return {
            "type": "Beam",
            "material": self._material,
            "length": self._length,
            "width": self._width,
            "height": self._height,
            "volume": self.calculate_volume(),
            "mass_kg": round(self.calculate_mass(), 2),
            "load_n": round(self.calculate_load(), 2),
        }

    def __str__(self) -> str:
        return (
            f"[BEAM] {self._material} | "
            f"{self._length}x{self._width}x{self._height}m | "
            f"V={self.calculate_volume():.3f}m³"
        )


class Column(StructuralElement):
    """Pilar estrutural.

    Attributes:
        _section: Lado da seção quadrada em metros.
    """

    def __init__(self, height: float, section: float, material: str = "concrete") -> None:
        """Inicializa um pilar estrutural.

        Args:
            height: Altura do pilar em metros.
            section: Lado da seção quadrada em metros.
            material: Material do pilar. Padrão: concrete.

        Raises:
            InvalidDimensionError: Se alguma dimensão for inválida.
        """
        super().__init__(material, height)
        if section <= 0:
            raise InvalidDimensionError("section", section)
        self._section = section

    @property
    def section(self) -> float:
        """Retorna a seção do pilar."""
        return self._section

    def calculate_volume(self) -> float:
        """Calcula o volume do pilar.

        Returns:
            Volume em metros cúbicos.
        """
        return round(self._length * self._section**2, 4)

    def to_dict(self) -> dict:
        """Serializa o pilar para dicionário.

        Returns:
            Dicionário com os dados do pilar.
        """
        return {
            "type": "Column",
            "material": self._material,
            "height": self._length,
            "section": self._section,
            "volume": self.calculate_volume(),
            "mass_kg": round(self.calculate_mass(), 2),
            "load_n": round(self.calculate_load(), 2),
        }

    def __str__(self) -> str:
        return (
            f"[COLUMN] {self._material} | "
            f"h={self._length}m, s={self._section}m | "
            f"V={self.calculate_volume():.3f}m³"
        )


class Slab(StructuralElement):
    """Laje estrutural.

    Attributes:
        _width: Largura da laje em metros.
        _thickness: Espessura da laje em metros.
    """

    def __init__(
        self, length: float, width: float, thickness: float, material: str = "concrete"
    ) -> None:
        """Inicializa uma laje estrutural.

        Args:
            length: Comprimento em metros.
            width: Largura em metros.
            thickness: Espessura em metros.
            material: Material da laje. Padrão: concrete.

        Raises:
            InvalidDimensionError: Sea alguma dimensão for inválida.
        """
        super().__init__(material, length)
        if width <= 0:
            raise InvalidDimensionError("width", width)
        if thickness <= 0:
            raise InvalidDimensionError("thickness", thickness)
        self._width = width
        self._thickness = thickness

    @property
    def width(self) -> float:
        """Retorna a largura da laje."""
        return self._width

    @property
    def thickness(self) -> float:
        """Retorna a espessura da laje."""
        return self._thickness

    def calculate_volume(self) -> float:
        """Calcula o volume da laje.

        Returns:
            Volume em metros cúbicos.
        """
        return round(self._length * self._width * self._thickness, 4)

    def to_dict(self) -> dict:
        """Serializa a laje para dicionário.

        Returns:
            Dicionário com os dados da laje.
        """
        return {
            "type": "Slab",
            "material": self._material,
            "length": self._length,
            "width": self._width,
            "thickness": self._thickness,
            "volume": self.calculate_volume(),
            "mass_kg": round(self.calculate_mass(), 2),
            "load_n": round(self.calculate_load(), 2),
        }

    def __str__(self) -> str:
        return (
            f"[SLAB] {self._material} | "
            f"{self._length}x{self._width}x{self._thickness}m | "
            f"V={self.calculate_volume():.3f}m³"
        )


class Footing(StructuralElement):
    """Sapata estrutural.

    Attributes:
        _width: Largura da sapata em metros.
        _depth: Profundidade da sapata em metros.
    """

    def __init__(
        self, length: float, width: float, depth: float, material: str = "concrete"
    ) -> None:
        """Inicializa uma sapata estrutural.

        Args:
            length: Comprimento em metros.
            width: Largura em metros.
            depth: Profundidade em metros.
            material: Material da sapata. Padrão: concrete.

        Raises:
            InvalidDimensionError: Se alguma dimensão for inválida.
        """
        super().__init__(material, length)
        if width <= 0:
            raise InvalidDimensionError("width", width)
        if depth <= 0:
            raise InvalidDimensionError("depth", depth)
        self._width = width
        self._depth = depth

    @property
    def width(self) -> float:
        """Retorna a largura da sapata."""
        return self._width

    @property
    def depth(self) -> float:
        """Retorna a profundidade da sapata."""
        return self._depth

    def calculate_volume(self) -> float:
        """Calcula o volume da sapata.

        Returns:
            Volume em metros cúbicos.
        """
        return round(self._length * self._width * self._depth, 4)

    def to_dict(self) -> dict:
        """Serializa a sapata para dicionário.

        Returns:
            Dicionário com os dados da sapata.
        """
        return {
            "type": "Footing",
            "material": self._material,
            "length": self._length,
            "width": self._width,
            "depth": self._depth,
            "volume": self.calculate_volume(),
            "mass_kg": round(self.calculate_mass(), 2),
            "load_n": round(self.calculate_load(), 2),
        }

    def __str__(self) -> str:
        return (
            f"[FOOTING] {self._material} | "
            f"{self._length}x{self._width}x{self._depth}m | "
            f"V={self.calculate_volume():.3f}m³"
        )
