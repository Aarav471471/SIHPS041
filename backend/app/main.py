from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import auth
# We will import other routers later

app = FastAPI(title="Suraksha-AR API")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
from app.routers import content, sync, verify, admin
app.include_router(content.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")
app.include_router(verify.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
