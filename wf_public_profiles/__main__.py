import uvicorn

from . import app
from .config import settings
from . import log


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT, log_config=log.UvicornLogger().dict())
