from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from shared.config.settings import settings
from api.rest_routes_lightcurve import router as lightcurve_router
from api.rest_routes_catalogue import router as catalogue_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HeliosAI API",
    description="Real-time space weather forecasting backend",
    version="1.0.0",
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lightcurve_router, prefix="/api/v1/lightcurve", tags=["Lightcurves"])
app.include_router(catalogue_router, prefix="/api/v1/catalogue", tags=["Catalogue"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "heliosai-api"}
