from fastapi import FastAPI
from app.routers import user

app = FastAPI()

# Include user router
app.include_router(user.router)
