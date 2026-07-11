from fastapi import FastAPI
from structlog import get_logger
from .api.rest.routes import router as rest_router
from .api.websockets.stream import router as ws_router

logger = get_logger(__name__)

app = FastAPI(
    title="HeliosAI Serving Layer",
    description="REST and WebSocket APIs for the HeliosAI space weather intelligence platform.",
    version="0.1.0"
)

# In a full implementation, we'd add CORS middleware, authentication middleware, etc.

app.include_router(rest_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("heliosai_serving_layer_started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("heliosai_serving_layer_shutting_down")
