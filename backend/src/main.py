import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.exception_handlers import add_exception_handlers
from src.api.routes import api_router
from src.cache.manager import CacheManager
from src.config import configure_logging, settings

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    aioredis.Redis()
    pool = aioredis.BlockingConnectionPool(timeout=2)
    redis = aioredis.Redis(
        host=settings.REDIS.HOST,
        port=settings.REDIS.PORT,
        db=settings.REDIS.DB,
        password=settings.REDIS.PASSWORD,
        username=settings.REDIS.USER,
        connection_pool=pool,
        socket_connect_timeout=1.0,
        socket_timeout=1.0,
    )
    CacheManager.init(redis)
    yield
    await redis.aclose()


app = FastAPI(debug=settings.DEBUG, lifespan=lifespan)
if settings.DEBUG:
    app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
add_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        proxy_headers=True,
        forwarded_allow_ips="172.18.0.0/16",
    )
