from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.api.v1.user import router as user
from app.api.v1.role import router as role
from app.logging_settings import configure_logging
import logging

app = FastAPI()

configure_logging(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app.include_router(user, prefix="/api")
app.include_router(role, prefix="/api")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    error_msg = exc.errors()[0]["msg"]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_msg}
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}
