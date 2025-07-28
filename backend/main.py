import asyncio
import shutil
from io import BytesIO
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from config import *
from processing.folder_utils import create_folders, clear_folders
from processing.processing import process_video, process_image

app = FastAPI()

HOST = "51.250.83.97"

origins = [
    "http://localhost",
    "http://localhost:3000",
    f"http://{HOST}",
    f"http://{HOST}:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_folders([UPLOADED_VIDEO_FOLDER])

@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    mode: str = Form(...),
    fps: int = Form(...)
):
    clear_folders([UPLOADED_VIDEO_FOLDER])
    file_path = UPLOADED_VIDEO_FOLDER / file.filename
    print(f"Mode: {mode}, FPS: {fps}")
    print("File path: ", file_path)

    # Save uploaded file
    with file_path.open("wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    # Detect file type and process accordingly
    if file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        # Async video processing
        process_task = asyncio.create_task(process_video(path_to_file=file_path, mode=mode, fps=fps))
        await process_task
        processed_path = process_task.result()
    elif file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
        # Sync image processing offloaded to thread
        processed_path = await asyncio.to_thread(process_image, path_to_file=file_path, mode=mode)
    else:
        return {"error": "Unsupported file format."}

    print("Processed path: ", processed_path)

    # Return processed file as stream
    with processed_path.open("rb") as result:
        content = result.read()
        return StreamingResponse(
            BytesIO(content),
            media_type="image/png" if processed_path.suffix in ['.png', '.jpg', '.jpeg'] else "video/mp4",
            headers={"Content-Disposition": f"filename={file.filename}"}
        )
