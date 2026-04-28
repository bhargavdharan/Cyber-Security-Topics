"""Pytest fixtures."""
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.db import redis_client

# Use SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# In-memory fake Redis for tests
_fake_redis = {}


async def fake_get_redis():
    """Fake Redis that uses in-memory dict."""
    return FakeRedis()


class FakeRedis:
    async def get(self, key):
        return _fake_redis.get(key)
    
    async def set(self, key, value, ex=None):
        _fake_redis[key] = value
    
    async def delete(self, key):
        _fake_redis.pop(key, None)
    
    async def ping(self):
        return True
    
    async def lpush(self, key, value):
        if key not in _fake_redis:
            _fake_redis[key] = []
        _fake_redis[key].insert(0, value)
    
    async def ltrim(self, key, start, end):
        if key in _fake_redis:
            items = _fake_redis[key]
            if end == -1:
                end = len(items)
            _fake_redis[key] = items[start:end+1]
    
    async def lrange(self, key, start, end):
        items = _fake_redis.get(key, [])
        if end == -1:
            end = len(items)
        return items[start:end+1]
    
    async def expire(self, key, seconds):
        pass  # No TTL support in FakeRedis
    
    def pipeline(self):
        return FakePipeline()
    
    async def zadd(self, key, mapping):
        if key not in _fake_redis:
            _fake_redis[key] = []
        for member, score in mapping.items():
            _fake_redis[key].append((member, score))
    
    async def zrange(self, key, start, end, withscores=False):
        items = _fake_redis.get(key, [])
        if end == -1:
            end = len(items)
        return items[start:end]
    
    async def dbsize(self):
        return len(_fake_redis)


class FakePipeline:
    """Fake Redis pipeline for batch operations."""
    def __init__(self):
        self._ops = []
    
    def lpush(self, key, value):
        self._ops.append(('lpush', key, value))
        return self
    
    def ltrim(self, key, start, end):
        self._ops.append(('ltrim', key, start, end))
        return self
    
    def expire(self, key, seconds):
        self._ops.append(('expire', key, seconds))
        return self
    
    async def execute(self):
        for op in self._ops:
            if op[0] == 'lpush':
                await FakeRedis().lpush(op[1], op[2])
            elif op[0] == 'ltrim':
                await FakeRedis().ltrim(op[1], op[2], op[3])
            elif op[0] == 'expire':
                await FakeRedis().expire(op[1], op[2])
        self._ops = []


# Patch Redis client
redis_client.get_redis = fake_get_redis


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
