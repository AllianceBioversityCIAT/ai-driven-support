"""
Configuration for FreshAI Platform
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # FreshService Configuration
    FRESHSERVICE_API_KEY = os.getenv("FRESHSERVICE_API_KEY", "")
    FRESHSERVICE_DOMAIN = os.getenv("FRESHSERVICE_DOMAIN", "alliance")
    API_BASE_URL = os.getenv("API_BASE_URL", f"https://{FRESHSERVICE_DOMAIN}.freshservice.com/api/v2")
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./freshai.db")
    
    # API Server
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Environment
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def get_summary(self):
        return {
            "freshservice_domain": self.FRESHSERVICE_DOMAIN,
            "api_host": self.API_HOST,
            "api_port": self.API_PORT,
            "debug": self.DEBUG
        }
    
    def validate(self):
        return True  # Always return True for now

# Create config instance
config = Config()
