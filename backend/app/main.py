from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.parts import router as parts_router

app = FastAPI(title="Dealership Parts Operations Platform")

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

app.include_router(parts_router)