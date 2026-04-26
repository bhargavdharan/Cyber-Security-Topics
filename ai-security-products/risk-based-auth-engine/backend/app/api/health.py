"""Health check and monitoring endpoints."""
import time
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, engine
from app.db.redis_client import get_redis
from app.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()

start_time = time.time()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "1.0.0",
        "uptime_seconds": int(time.time() - start_time),
    }


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness probe - checks DB and Redis connectivity."""
    checks = {}
    
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
    
    # Check Redis
    try:
        r = await get_redis()
        await r.ping()
        checks["redis"] = "connected"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
    
    all_healthy = all(v == "connected" for v in checks.values())
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
    }


@router.get("/health/metrics")
async def metrics():
    """Basic metrics endpoint (extend with Prometheus if needed)."""
    from app.db.redis_client import get_redis
    
    r = await get_redis()
    
    # Simple counts - in production use proper metrics
    db_size = await r.dbsize()
    
    return {
        "uptime_seconds": int(time.time() - start_time),
        "redis_keys": db_size,
    }
