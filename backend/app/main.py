# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .routes import newsletter, wordpress

# Initialize FastAPI app
app = FastAPI(
    title="Goochland GOP Newsletter Agent",
    description="AI-powered newsletter generation system",
    version="1.0.0"
)

# Parse CORS origins from comma-separated string
cors_origins_list = [origin.strip() for origin in settings.cors_origins.split(',')]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(newsletter.router)
app.include_router(wordpress.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Goochland GOP Newsletter Agent API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )