from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # AI Service Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # CORS Configuration
    CORS_ALLOW_ORIGINS: str = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "https://zodiacs-jet.vercel.app,http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    )
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
    
    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Geocoding Configuration
    GEONAMES_USERNAME: str = os.getenv("GEONAMES_USERNAME", "century.boy")
    
    # Other API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Global settings instance
settings = Settings()

def log_startup_info():
    """Log startup information for debugging"""
    print("🚀 Application Configuration:")
    print(f"  - GROQ_API_KEY loaded: {'Yes' if settings.GROQ_API_KEY else 'No'}")
    if settings.GROQ_API_KEY:
        print(f"  - GROQ_API_KEY preview: {settings.GROQ_API_KEY[:5]}...")
    print(f"  - CORS_ALLOW_ORIGINS: {settings.CORS_ALLOW_ORIGINS}")
    print(f"  - CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    print(f"  - LOG_LEVEL: {settings.LOG_LEVEL}")
    print(f"  - GEONAMES_USERNAME: {settings.GEONAMES_USERNAME}")
    print(f"  - SUPABASE_URL configured: {'Yes' if settings.SUPABASE_URL else 'No'}")
    print(f"  - GOOGLE_API_KEY configured: {'Yes' if settings.GOOGLE_API_KEY else 'No'}")
    print()