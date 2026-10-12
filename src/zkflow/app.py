from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI(title="Arcane Proofworks", version="0.1.0")
app.include_router(api_router)
