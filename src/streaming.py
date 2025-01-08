import os
import fastapi
import uvicorn
import recording

from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


# TODO get it from a config file
streaming_port = 5000
streaming_host = "0.0.0.0"


# script parent path
my_path = os.path.abspath(os.path.dirname(__file__))

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
    return FileResponse(os.path.join(my_path, "index.html"))


@app.get("/video_feed")
async def get_video_feed():
    return StreamingResponse(
        recording.get_frame(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def run():
    uvicorn.run(app, host=streaming_host, port=streaming_port)
