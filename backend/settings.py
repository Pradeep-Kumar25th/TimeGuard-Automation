"""
Application Settings and Configuration
Uses Pydantic for environment variable validation
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for pydantic v1
    from pydantic import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application Configuration
    app_name: str = "TimeGuard AI API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # API Configuration
    api_title: str = "TimeGuard AI API - Automation Module"
    api_version: str = "1.0.0"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # Data Storage Configuration
    data_dir: str = "./data"
    pdf_output_dir: str = "./generated_pdfs"
    
    # File Upload Configuration
    max_file_size_mb: int = 50
    allowed_file_extensions: List[str] = [".xlsx", ".xls"]
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = ""
    
    # Security Configuration (optional - for future use)
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes"""
        return self.max_file_size_mb * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()

