import os
from dotenv import load_dotenv
from api.index import app

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    # Use port 8080 to match production, but allow override
    port = int(os.getenv("PORT", 8080))
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=port,
        debug=True       # Enable debug mode for development
    )