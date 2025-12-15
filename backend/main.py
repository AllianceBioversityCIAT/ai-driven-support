"""
FreshAI Platform - Backend Main Server
Screaming Architecture: Features are immediately visible
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
app = FastAPI(title="FreshAI Platform - Feature-Driven Architecture")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Feature Routes (Screaming Architecture)
try:
    from features.ticket_management.presentation import router as ticket_management_router
    app.include_router(ticket_management_router, prefix="/api/tickets", tags=["Ticket Management"])
    logger.info("✅ Ticket Management feature registered")
except Exception as e:
    logger.error(f"❌ Failed to import Ticket Management feature: {e}")

try:
    from features.ticket_analysis.presentation import router as ticket_analysis_router
    app.include_router(ticket_analysis_router, prefix="/api/analysis", tags=["Ticket Analysis"])
    logger.info("✅ Ticket Analysis feature registered")
except Exception as e:
    logger.error(f"❌ Failed to import Ticket Analysis feature: {e}")

# Register Legacy Routes (Backward Compatibility)
try:
    from api.routes.tickets import router as legacy_tickets_router
    app.include_router(legacy_tickets_router, prefix="/api/tickets", tags=["Legacy Tickets"])
    logger.info("✅ Legacy Tickets routes registered")
except Exception as e:
    logger.error(f"❌ Failed to import legacy tickets routes: {e}")

# Register Webhook Routes
try:
    from api.routes.webhooks import router as webhooks_router
    app.include_router(webhooks_router, prefix="/api/webhooks", tags=["Webhooks"])
    logger.info("✅ Webhook routes registered")
except Exception as e:
    logger.error(f"❌ Failed to import webhook routes: {e}")

# Basic routes
@app.get("/health")
async def health():
    return {"status": "ok", "architecture": "screaming"}

@app.get("/debug/routes")
async def debug_routes():
    routes = [{"path": r.path, "methods": getattr(r, "methods", ["GET"])} for r in app.routes]
    return {"routes": routes}

@app.get("/features")
async def list_features():
    """List available features in the system"""
    return {
        "features": [
            {
                "name": "Ticket Management",
                "description": "CRUD operations for support tickets",
                "endpoints": "/api/tickets"
            },
            {
                "name": "Ticket Analysis",
                "description": "AI-powered ticket analysis",
                "endpoints": "/api/analysis"
            }
        ],
        "legacy_endpoints": {
            "note": "Legacy endpoints are still available for backward compatibility",
            "analyze_ticket": "POST /api/tickets/{ticket_id}/analyze"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FreshAI Platform...")
    logger.info("📐 Architecture: Screaming (Feature-Driven)")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
