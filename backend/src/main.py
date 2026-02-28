from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.exception_handlers import register_exception_handlers
from src.api.routes import api_router
from src.config import settings

app = FastAPI(debug=settings.DEBUG)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
register_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
