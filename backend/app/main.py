from fastapi import FastAPI

app = FastAPI(title="Dealership Parts Operations Platform")


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}