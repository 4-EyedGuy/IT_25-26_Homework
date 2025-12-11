import pytest
import pytest_asyncio
import asyncio
import sys
import os
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app.main import app

os.environ["TESTING"] = "1"

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac