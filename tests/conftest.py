# tests/conftest.py

import pytest_asyncio
import asyncio
from httpx import AsyncClient
from store.core.db import db_client

# Esta fixture cria um event loop para toda a sessão de testes
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(base_url="http://127.0.0.1:8001") as ac:
        yield ac

# Esta fixture limpa o banco de dados após cada teste
@pytest_asyncio.fixture(autouse=True)
async def clear_collections():
    yield
    collections = await db_client.get_database().list_collection_names()
    if "products" in collections:
        await db_client.get_database().drop_collection("products")