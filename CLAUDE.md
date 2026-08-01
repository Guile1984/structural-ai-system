# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Structural engineering calculation system — computes volume, mass, and load for structural elements (Beam, Column, Slab, Footing) across materials (concrete, steel, engineered wood). Flask REST API with JSON file persistence, planned ML pipeline for load approval prediction, and planned Streamlit dashboard.

## Commands

```bash
# Run the Flask API
python main.py --api
# or directly:
python run_api.py

# Run Streamlit dashboard (not yet implemented)
python main.py --dashboard

# Run ML training (ml/pipeline.py is incomplete)
python main.py --train

# Quick domain layer smoke test
python teste_core.py

# Install dependencies
pip install -r requirements.txt
```

No test framework is configured yet. No linter/formatter config exists. The `tests/` directory is empty.

## Architecture

Three-layer design with strict dependency direction: API → Core. ML → Core.

**Core (`core/`)** — Pure domain logic, no framework dependencies. `StructuralElement` base class with `Beam`, `Column`, `Slab`, `Footing` subclasses. `calculator.py` provides aggregate functions (`total_volume`, `total_mass`, `total_load`, `heaviest_element`, `structural_summary`). Material densities are hardcoded in elements.py.

**API (`api/`)** — Flask application factory in `__init__.py`. Routes in `routes.py` under `/api/v1/`. Input validation in `validators.py`. Persistence is a JSON file at `data/elements.json` read/written directly in route handlers.

**ML (`ml/`)** — Incomplete. `pipeline.py` has `generate_dataset()` and `prepare_features()` but `train_regression()` is unfinished (file cuts off at line 98 with a syntax error).

**Unimplemented modules:** `automation/`, `dashboard/`, `reports/` — directories exist but are empty or have only `__init__.py`.

## API Endpoints

All under `/api/v1/`:
- `GET /health` — health check
- `GET|POST /elements` — list or create elements
- `GET|DELETE /elements/<id>` — single element operations
- `GET /elements/type/<type>` — filter by element type
- `GET /summary` — structural summary

## Estado atual

- `ml/pipeline.py` está em desenvolvimento: `train_regression()` ainda
  não foi concluída. Não é corrupção nem truncamento — é trabalho em
  andamento. Não reescrever nem "consertar" por conta própria.

## Sobre varreduras automáticas

Apontamentos gerados por varredura do código são hipóteses, não fatos.
Verificar antes de propor correção (`py_compile`, import do módulo,
execução do teste). Na varredura inicial deste projeto, dois de três
"bugs críticos" apontados não existiam.

## Environment

- Python with pip, dependencies in `requirements.txt`
- `.env.example` has config template (Flask port, secret key, model version, approval threshold)
- Virtual environment expected at `.venv/`
- Data persisted to `data/elements.json` (gitignored)


## Método de trabalho com o Claude Code

O autor deste projeto é estudante de Engenharia Civil em processo de
aprendizado de Python. O objetivo não é entregar código rápido, é
consolidar a capacidade de escrever código de forma independente.

Papel do Claude Code neste repositório: **revisor e depurador**.

Regras:
- NÃO escrever implementação por conta própria. Quando identificar o que
  falta, descrever o que precisa ser feito e por quê — o autor digita.
- Ao encontrar um bug: apontar o arquivo e a linha, explicar a causa raiz
  e o efeito, e parar. Só propor o código corrigido se for pedido
  explicitamente.
- Ao revisar código já escrito: comentar arquitetura, legibilidade,
  tratamento de erro e casos de borda, mesmo que o código funcione.
- Um assunto por vez. Não despejar dez apontamentos de uma vez; começar
  pelo mais crítico e aguardar.
- Responder sempre em português brasileiro.
- Exceção: quando o autor declarar explicitamente que há prazo curto,
  as restrições acima ficam suspensas para aquela sessão.