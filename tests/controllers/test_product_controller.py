# tests/controllers/test_product_controller.py

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_should_create_product(client: AsyncClient):
    # DADOS DE ENTRADA DO PRODUTO
    product_data = {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8500.00", # httpx envia como string
        "status": True,
    }

    # FAZ A REQUISIÇÃO POST PARA A API
    response = await client.post("/products/", json=product_data)

    # VERIFICA A RESPOSTA
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["name"] == product_data["name"]
    assert response_json["quantity"] == product_data["quantity"]
    assert response_json["price"] == product_data["price"]
    assert response_json["status"] == product_data["status"]
    
    # VERIFICA SE OS CAMPOS DE CONTROLE FORAM ADICIONADOS
    assert "id" in response_json
    assert "created_at" in response_json
    assert "updated_at" in response_json