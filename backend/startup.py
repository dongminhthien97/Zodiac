#!/usr/bin/env python3
"""
Startup script for production deployment.
Handles port binding correctly for Railway and other platforms.
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Railway standard)
    port = int(os.environ.get("PORT", 8080))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Bind to all interfaces for production
        port=port,
        reload=False,    # Disable reload in production
        log_level="info"
    )