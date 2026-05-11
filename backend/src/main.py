import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.exception_handlers import add_exception_handlers
from src.api.routes import api_router
from src.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    yield


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

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
