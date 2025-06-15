# app/main.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env into os.environ

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import engine, Base
import app.models.user_orm  # ensure ORM model is registered
from app.routers.user import router as user_router
from app.routers import auth
from app.logger import get_logger
import time
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware


logger = get_logger("pep2-backend")

app = FastAPI(
    title="PEP2 Backend API",
    description="Backend API for the PEP2 platform, used by the Angular frontend",
    version="0.1.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication endpoints"},
        {"name": "users", "description": "User management operations"}
    ]
)


origins = [
    "http://localhost:4200",  # Angular dev server
    # Add more allowed origins here in future (e.g., production frontend)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  # mount /login and auth routes
app.include_router(user_router)  # mount user routes

@app.on_event("startup")
async def on_startup():
    """
    On app startup, create all tables in the DB
    (no-op if they already exist).
    Log startup event.
    """
    logger.info("Application startup: Creating database tables if not exist")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    """
    Log shutdown event.
    """
    logger.info("Application shutdown")

# Middleware for structured logging of requests and responses
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "client_host": request.client.host if request.client else None
        }
        logger.info("HTTP request completed", extra=log_data)
        return response

app.add_middleware(LoggingMiddleware)

# Exception handlers

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True, extra={
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None
    })
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTPException: {exc.detail}", extra={
        "method": request.method,
        "url": str(request.url),
        "status_code": exc.status_code,
        "client_host": request.client.host if request.client else None
    })
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}", extra={
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None
    })
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
