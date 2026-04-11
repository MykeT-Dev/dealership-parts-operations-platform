from fastapi import FastAPI

from app.api.parts import router as parts_router

app = FastAPI(title="Dealership Parts Operations Platform")


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

app.include_router(parts_router)