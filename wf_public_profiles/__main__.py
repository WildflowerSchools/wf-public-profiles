import uvicorn

from . import app
from . import log


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4050, log_config=log.UvicornLogger().dict())
