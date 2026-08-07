"""
Módulo: tests/test_api.py
Descrição: Testes dos endpoints da API REST
"""

import pytest

from api import create_app


@pytest.fixture
def client(tmp_path):
    """Fixture que cria um cliente de teste com dados temporários."""
    app = create_app()
    app.config["TESTING"] = True

    data_file = tmp_path / "elements.json"
    data_file.write_text("[]", encoding="utf-8")

    from api import routes

    routes.DATA_FILE = data_file

    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_beam():
    """Fixture com dados de uma viga válida."""
    return {"type": "Beam", "material": "concrete", "length": 6.0, "width": 0.3, "height": 0.5}


class TestHealthEndpoint:
    """Testes para GET /api/vi/health."""

    def test_returns_200(self, client):
        """Verifica que retorna 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_returns_online_status(self, client):
        """Verifica que status é online."""
        response = client.get("/api/v1/health")
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["status"] == "online"


class TestListElements:
    """Testes para GET /api/v1/elements."""

    def test_empty_list(self, client):
        """Verifica lista vazia."""
        response = client.get("/api/v1/elements")
        data = response.get_json()
        assert data["data"]["total"] == 0
        assert data["data"]["elements"] == []

    def test_after_create(self, client, sample_beam):
        """Verifica lista após criar elemento."""
        client.post("/api/v1/elements", json=sample_beam)
        response = client.get("/api/v1/elements")
        data = response.get_json()
        assert data["data"]["total"] == 1


class TestCreateElement:
    """Testes para POST /api/v1/elements."""

    def test_create_beam(self, client, sample_beam):
        """Verifica criação de viga."""
        response = client.post("/api/v1/elements", json=sample_beam)
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["type"] == "Beam"

    def test_create_assigns_id(self, client, sample_beam):
        """Verifica que ID é atribuído."""
        response = client.post("/api/v1/elements", json=sample_beam)
        data = response.get_json()
        assert "id" in data["data"]

    def test_invalid_material(self, client):
        """Verifica rejeição de material inválido."""
        response = client.post(
            "/api/v1/elements",
            json={"type": "Beam", "material": "brick", "length": 6.0, "width": 0.3, "height": 0.5},
        )
        assert response.status_code == 400

    def test_missing_field(self, client):
        """Verifica rejeição quando campo obrigatório falta."""
        response = client.post("/api/v1/elements", json={"type": "Beam", "material": "concrete"})
        assert response.status_code == 400

    def test_negative_dimension(self, client):
        """Verifica rejeição de dimensão negativa."""
        response = client.post(
            "/api/v1/elements",
            json={
                "type": "Beam",
                "material": "concrete",
                "length": -1.0,
                "width": 0.3,
                "height": 0.5,
            },
        )
        assert response.status_code == 400


class TestGetElement:
    """Tests para GET /api/v1/elements/<id>."""

    def test_get_existing(self, client, sample_beam):
        """Verifica busca de elemento existente."""
        create = client.post("/api/v1/elements", json=sample_beam)
        element_id = create.get_json()["data"]["id"]
        response = client.get(f"/api/v1/elements/{element_id}")
        assert response.status_code == 200

    def test_get_nonexistent(self, client):
        """Verifica 404 para ID inexistente."""
        response = client.get("/api/v1/elements/999")
        assert response.status_code == 404


class TestDeleteElement:
    """Testes para DELETE /api/v1/elements/<id>."""

    def test_delete_existing(self, client, sample_beam):
        """Verifica remoção de elemento existente."""
        create = client.post("/api/v1/elements", json=sample_beam)
        element_id = create.get_json()["data"]["id"]
        response = client.delete(f"/api/v1/elements/{element_id}")
        assert response.status_code == 200

    def test_delete_nonexisting(self, client):
        """Verifica 404 ao remover inexistente."""
        response = client.delete("/api/v1/elements/999")
        assert response.status_code == 404

    def test_list_empty_after_delete(self, client, sample_beam):
        """Verifica que lista fica vazia após remover."""
        create = client.post("/api/v1/elements", json=sample_beam)
        element_id = create.get_json()["data"]["id"]
        client.delete(f"/api/v1/elements/{element_id}")
        response = client.get("/api/v1/elements")
        data = response.get_json()
        assert data["data"]["total"] == 0
