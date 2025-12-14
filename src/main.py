from fastapi import FastAPI
from src.core.config import settings
from src.api.V1.router import api_router
from src.core.exceptions_handler import register_exception_handlers
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router,prefix=settings.API_V1_STR)
register_exception_handlers(app)