import pytest_asyncio
import asyncio
from httpx import AsyncClient
from store.main import app
from store.core.db import db_client

# Usar um loop de eventos diferente para os testes, se necessário
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def clear_collections():
    yield
    # Limpa a coleção de produtos depois de cada teste
    collections = await db_client.get_database().list_collection_names()
    if "products" in collections:
        await db_client.get_database().drop_collection("products")