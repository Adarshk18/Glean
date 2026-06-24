from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth

app = FastAPI(
    title="Glean",
    description="Upload documents and chat with them",
    version="0.1.0",
)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health", tags=["health"])
def healthcheck():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


@app.get("/", tags=["health"])
def root():
    return {"message": "Glean SaaS API is running. See /docs for interactive API documentation."}
