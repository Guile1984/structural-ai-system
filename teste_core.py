"""
Arquivo: test_core.py
Descrição: Validação rápida da camada de domínio
"""

from core import (
    Beam,
    Column,
    Footing,
    InvalidDimensionError,
    Slab,
    UnsupportedMaterialError,
    structural_summary,
)

print("=== TESTANDO CAMADA DE DOMÍNIO ===\n")

# Criando elementos
beam = Beam(6.0, 0.3, 0.5)
column = Column(3.0, 0.4)
slab = Slab(5.0, 4.0, 0.12)
footing = Footing(1.0, 1.0, 0.4)

elements = [beam, column, slab, footing]

print("=== ELEMENTOS ===")
for e in elements:
    print(e)

print("\n=== TO_DICT (Beam) ===")
import json

print(json.dumps(beam.to_dict(), indent=2))

print("\n=== FROM_DICT ===")
data = beam.to_dict()
beam_reconstructed = Beam.from_dict(data)
print(beam_reconstructed)

print("\n=== RESUMO ESTRUTURAL ===")
summary = structural_summary(elements)
for key, value in summary.items():
    print(f"    {key}: {value}")

print("\n=== VALIDAÇÃO DE EXCEÇÕES ===")
try:
    beam_invalido = Beam(-1, 0.3, 0.5)
except InvalidDimensionError as e:
    print(f"✔ InvalidDimensionError: {e}")

try:
    beam_material = Beam(6.0, 0.3, 0.5, "tijolo")
except UnsupportedMaterialError as e:
    print(f"✔ UnsupportedMaterialError: {e}")

print("\n=== DOMÍNIO VALIDADO COM SUCESSO ===")
