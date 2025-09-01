import pytest
from httpx import AsyncClient
from uuid import UUID

@pytest.mark.asyncio
async def test_should_create_product(client: AsyncClient):
    product_data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8500.00", "status": True}
    response = await client.post("/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Iphone 14 Pro Max"
    assert "id" in data

@pytest.mark.asyncio
async def test_should_get_product(client: AsyncClient):
    # Primeiro cria um produto para depois buscar
    product_data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8500.00", "status": True}
    response_create = await client.post("/products/", json=product_data)
    product_id = response_create.json()["id"]

    response_get = await client.get(f"/products/{product_id}")
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "Iphone 14 Pro Max"

@pytest.mark.asyncio
async def test_get_product_should_return_404(client: AsyncClient):
    random_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/products/{random_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_should_query_products_with_filter(client: AsyncClient):
    await client.post("/products/", json={"name": "Product A", "quantity": 1, "price": "4000.00", "status": True})
    await client.post("/products/", json={"name": "Product B", "quantity": 1, "price": "6000.00", "status": True})
    await client.post("/products/", json={"name": "Product C", "quantity": 1, "price": "9000.00", "status": True})
    
    response = await client.get("/products/?min_price=5000&max_price=8000")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    assert products[0]["name"] == "Product B"

@pytest.mark.asyncio
async def test_should_update_product(client: AsyncClient):
    product_data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8500.00", "status": True}
    response_create = await client.post("/products/", json=product_data)
    product_id = response_create.json()["id"]
    
    update_data = {"price": "8000.00", "quantity": 5}
    response_update = await client.patch(f"/products/{product_id}", json=update_data)
    assert response_update.status_code == 200
    assert response_update.json()["price"] == "8000.0" # Decimal vem como string
    assert response_update.json()["quantity"] == 5

@pytest.mark.asyncio
async def test_should_delete_product(client: AsyncClient):
    product_data = {"name": "Product to Delete", "quantity": 1, "price": "10.00", "status": True}
    response_create = await client.post("/products/", json=product_data)
    product_id = response_create.json()["id"]

    response_delete = await client.delete(f"/products/{product_id}")
    assert response_delete.status_code == 204
    
    response_get = await client.get(f"/products/{product_id}")
    assert response_get.status_code == 404