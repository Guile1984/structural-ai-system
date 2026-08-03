# Notas do projeto

Registro de decisões pendentes, descobertas e rotinas que não cabem no código.

---

## Rotina de verificação ao fim de cada sprint

1. `ruff check --output-format=concise .` — varredura completa
2. `ruff check --fix .` — aplica correções seguras
3. `python -c "import core, api"` — confirma que nada quebrou
4. Analisar os apontamentos restantes: são hipóteses, não fatos.
   Verificar antes de corrigir.
5. Registrar aqui o que for adiado; commitar.

Apontamento de ferramenta automática nunca é corrigido sem verificação
prévia. Na varredura inicial deste projeto, dois de três "bugs críticos"
apontados pelo `/init` não existiam.

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

## [RESOLVIDO] Duplicação da mensagem "element not found"

**Resolução:** Opção B implementada em 02/08/2026. API agora levanta
`ElementNotFoundError` do domínio. Handler `@api_bp.errorhandler`
traduz para HTTP 404. Origem única da mensagem.
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

## [RESOLVIDO] `_build_element()` sem tratamento de tipo desconhecido

**Resolução:** `else` adicionado em 02/08/2026. Tipo desconhecido agora
levanta `UnsupportedElementTypeError` explicitamente.
---

## [PENDENTE] `eq-without-hash` em `core/elements.py`

`StructuralElement` define `__eq__` sem definir `__hash__`. Em Python,
isso torna as instâncias não-hasheáveis: não podem entrar em `set` nem
servir de chave de `dict`.

Decidir se a igualdade estrutural faz sentido para o domínio. Se sim,
implementar `__hash__` coerente com o `__eq__`. Se elementos são sempre
distintos por identidade, talvez o `__eq__` é que esteja sobrando.

---

## [PENDENTE] `subprocess.run` sem `check` em `main.py`

`subprocess.run(["streamlit", "run", ...])` não passa o argumento
`check`. Se o Streamlit falhar ao iniciar, o programa segue como se
tudo tivesse dado certo, sem sinalizar nada ao usuário.

Decidir entre `check=True` (levanta exceção em caso de falha) ou
`check=False` explícito (documenta que o retorno é ignorado de
propósito).

---

## [PENDENTE] `os.getenv` com padrão numérico em `run_api.py`

`int(os.getenv("FLASK_PORT", 5000))` — o padrão é `int`, mas
`os.getenv` retorna `str`. Funciona porque `int()` aceita ambos, mas o
tipo é inconsistente. Correção: `os.getenv("FLASK_PORT", "5000")`.

## [RESOLVIDO] `os.getenv` com padrão numérico em `run_api.py`

**Resolução:** Corrigido em 02/08/2026. Padrão alterado para `"5000"` (string).
---

## [PENDENTE] `try` extenso em `create_element()` (`api/routes.py`)

O bloco `try` envolve 7 instruções. Quanto mais amplo o `try`, menos
preciso o diagnóstico: o `except Exception` captura qualquer falha das
sete, incluindo erro de escrita em disco, e devolve tudo como 400.

Avaliar reduzir o escopo do `try` ao que realmente pode falhar por dado
inválido, tratando erros de I/O separadamente.

---

## [ACEITO] Import no meio de `teste_core.py`

`module-import-not-at-top-of-file` na linha 31. É script exploratório de
teste manual, não código de produção. Sem correção prevista — se
incomodar nas varreduras, silenciar via `per-file-ignores` no
`pyproject.toml`.

---

## Limitação atual do Ruff

`ml/pipeline.py` está fora do alcance do linter e do formatador
enquanto `train_regression()` estiver incompleta — arquivo com sintaxe
inválida não pode ser analisado. Rodar `ruff format ml/pipeline.py`
assim que a função for concluída.

**Resolução:** `train_regression()` concluída em 02/08/2026. `ruff check`
e `ruff format` rodados com sucesso — All checks passed.
---

**Status geral:** todas as decisões adiadas. Prioridade é concluir
`train_regression()` em `ml/pipeline.py`.