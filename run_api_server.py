import os
import sys
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    host = os.environ.get("API_HOST", "127.0.0.1")
    port = int(os.environ.get("API_PORT", "8989"))

    uvicorn.run(
        "api_server.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
    )
