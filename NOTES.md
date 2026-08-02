# Notas do projeto

Registro de decisões pendentes e descobertas que não cabem no código.

---

## [PENDENTE] Duplicação da mensagem "element not found"

**Descoberto em:** 02/08/2026, ao investigar um `unused-import`
apontado pelo Ruff (o import em si já foi removido pelo `--fix`).

**Situação:** o texto `"Element with id={id} not found."` existe em três
lugares independentes:
- `core/exceptions.py` — dentro de `ElementNotFoundError`
- `api/routes.py`, em `get_element()` — escrito à mão
- `api/routes.py`, em `delete_element()` — escrito à mão

A exceção `ElementNotFoundError` existe no domínio, mas a API nunca a
usa. O comportamento externo está correto (404 com mensagem legível,
verificado por curl), mas a mensagem tem três origens que ninguém
mantém sincronizadas.

**Opções:**
- **A)** Aceitar que a API monta suas próprias mensagens. Barato,
  mantém a duplicação.
- **B)** `core` levanta a exceção, `routes.py` captura e traduz para
  HTTP 404. Origem única e respeita a separação de camadas (domínio
  decide o que é erro, API decide como comunicar).

---

## [PENDENTE] `_build_element()` sem tratamento de tipo desconhecido

**Descoberto em:** 02/08/2026, em leitura manual de `api/routes.py`.

**Situação:** a função testa quatro tipos com `if/elif` e não tem
`else`. Tipo desconhecido faz a função retornar `None` silenciosamente.
Em `create_element()`, isso vira `AttributeError` no `.to_dict()`,
capturado pelo `except Exception` e devolvido como 400 com mensagem
incompreensível ao cliente.

Hoje `validate_element()` provavelmente barra tipos inválidos antes,
então não é falha ativa — mas a função depende de validação externa
para não quebrar, e nada no código expressa isso.

A exceção adequada já existe: `UnsupportedElementTypeError`.

---

**Status geral:** ambas as decisões adiadas. Prioridade atual é
concluir `train_regression()` em `ml/pipeline.py`.

**Nota:** `ml/pipeline.py` está fora do alcance do Ruff (linter e
formatador) enquanto `train_regression()` estiver incompleta —
arquivo com sintaxe inválida não pode ser analisado. Rodar
`ruff format ml/pipeline.py` assim que a função for concluída.