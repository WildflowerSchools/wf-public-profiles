import os
import random
import string
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .log import logger
from .routes import router

app = FastAPI(title="wf-public-profiles", openapi_url="/api/v1/openapi.json")

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Thanks: https://philstories.medium.com/fastapi-logging-f6237b84ea64
@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={rid} started method={request.method} path={request.url.path}")
    start_time = time.time()

    request.state.rid = rid
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    logger.info(f"rid={rid} done completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


app.include_router(router, prefix="/api/v1/profiles")
app.mount("/static", StaticFiles(directory=f"{os.path.dirname(os.path.realpath(__file__))}/assets"), name="static")
