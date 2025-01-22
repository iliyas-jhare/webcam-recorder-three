import os
import fastapi
import uvicorn

import recording
import logging_wrapper

from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
UI_DIR_PATH = os.path.join(HERE, "ui")
INDEX_HTML_PATH = os.path.join(UI_DIR_PATH, "index.html")

# Logger
log = logging_wrapper.LoggingWrapper().get_logger(__name__)


# FASTAPI app
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)
app.mount(
    "/ui", StaticFiles(directory=UI_DIR_PATH, html=True, check_dir=True), name="ui"
)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Sends index file HTML reponse"""
    try:
        return FileResponse(INDEX_HTML_PATH, media_type="text/html")
    except Exception as e:
        log.exception(e)


@app.get("/video_feed", response_class=StreamingResponse)
async def get_video_feed():
    """Sends encoded video frame streaming reponse."""
    try:
        return StreamingResponse(
            content=recording.get_video_frame(),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )
    except Exception as e:
        log.exception(e)


@app.post("/{command}")
async def post_command(command: str):
    """Receives recording command."""
    try:
        log.info(f"Command received: {command}")
        # recording.on_command(command)
    except Exception as e:
        log.exception(e)


def init(config):
    """Starts FastAPI server"""
    try:
        uvicorn.run(app, host=config.Streaming.Host, port=config.Streaming.Port)
    except Exception as e:
        log.exception(e)
