import os
import fastapi
import uvicorn
import recording

from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


HERE = os.path.abspath(os.path.dirname(__file__))


# init FastAPI app
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse(os.path.join(HERE, "index.html"))


@app.get("/video_feed")
async def get_video_feed():
    return StreamingResponse(
        recording.get_frame(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def run(config):
    uvicorn.run(app, host=config.Streaming.Host, port=config.Streaming.Port)
