#!/usr/bin/env python3
"""
BhimLaw AI - Server Launcher
Starts the BhimLaw AI FastAPI server
"""

import uvicorn
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BhimLaw_AI_Launcher")

def main():
    """Launch BhimLaw AI server"""

    # Get port from environment variable (for Render compatibility) or default to 5001
    port = int(os.environ.get("PORT", 5001))

    print("\n🏛️  BhimLaw AI - Legal Assistant")
    print("🚀 Starting server...")
    print(f"📍 URL: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print("-" * 50)

    logger.info(f"Starting BhimLaw AI server on port {port}")

    try:
        # Import the FastAPI app
        from app import app

        # Run server with optimized configuration
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info",
            access_log=True
        )

    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)
    finally:
        print("\n🏛️  BhimLaw AI - Session ended")
        print("Thank you for using BhimLaw AI!")

if __name__ == "__main__":
    main()
