"""
FreshAI Platform - Backend Main Server
"""
import logging
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(title="FreshAI Platform")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
try:
    from api.routes.tickets import router as tickets_router
    app.include_router(tickets_router, prefix="/api/tickets", tags=["tickets"])
    logger.info("✅ Tickets routes registered")
except Exception as e:
    logger.error(f"❌ Failed to import tickets routes: {e}")

# Basic routes
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/debug/routes")
async def debug_routes():
    routes = [{"path": r.path, "methods": getattr(r, "methods", ["GET"])} for r in app.routes]
    return {"routes": routes}

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
