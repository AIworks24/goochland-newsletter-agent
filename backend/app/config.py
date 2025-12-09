# backend/app/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str
    openai_api_key: str
    
    # WordPress
    wordpress_url: str
    wordpress_username: str
    wordpress_app_password: str
    
    # Application
    environment: str = "development"
    debug: bool = True
    cors_origins: str = "http://localhost:3000"
    
    # File Upload
    max_upload_size: int = 10485760  # 10MB
    upload_dir: str = "./temp/uploads"
    
    # Model Configuration
    default_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8000
    
    # Optional Database
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)