from fastapi import FastAPI
from datetime import datetime
from routers.tagihan import router as tagihan_router
from routers.kalkulator import router as kalkulator_router

app = FastAPI(
    title="LUNAS API",
    description="Backend engine untuk aplikasi pelunasan utang cerdas LUNAS",
    version="0.1.0"
)

app.include_router(tagihan_router)
app.include_router(kalkulator_router)

@app.get("/")
def root():
    return {
        "message": "LUNAS Engine is Running!",
        "status": "healthy",
        "team": "ERRNOR"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "database": "not connected yet"
    }

@app.get("/api/v1/info")
def api_info():
    return {
        "api_version": "0.1.0",
        "features": ["avalanche", "nudging", "snap-bi-simulation"]
    }