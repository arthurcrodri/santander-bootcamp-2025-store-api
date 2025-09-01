# tests/conftest.py

import pytest_asyncio
from httpx import AsyncClient
from store.main import app

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac