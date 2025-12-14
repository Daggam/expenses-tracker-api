from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import BaseAPIException
def register_exception_handlers(app):
    
    @app.exception_handler(BaseAPIException)
    async def app_exc_handler(
        request:Request,
        exc: BaseAPIException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message
            }
        )
    