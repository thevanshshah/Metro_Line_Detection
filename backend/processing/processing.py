from pathlib import Path
from PIL import Image, ImageDraw

from .folder_utils import clear_folders, create_folders
from .ml.utils import process_images
from .video_utils import fragment_video, create_video_from_images
from config import *

# Ensure folders exist
create_folders([IMAGES_FOLDER, PROCESSED_FRAMES_FOLDER])


async def process_video(path_to_file: Path, mode: str, fps: int) -> Path:
    """
    Full video processing pipeline:
    1. Clear temp folders
    2. Extract frames from video
    3. Process frames
    4. Recombine into processed video
    """
    clear_folders([IMAGES_FOLDER, PROCESSED_FRAMES_FOLDER])

    # Step 1: Extract frames from video
    fragment_video(video_path=path_to_file, output_folder=IMAGES_FOLDER, fps=fps)

    # Step 2: Process images using ML pipeline
    await process_images(input_folder=IMAGES_FOLDER, mode=mode, output_folder=PROCESSED_FRAMES_FOLDER)

    # Step 3: Create video from processed images
    create_video_from_images(
        input_folder=PROCESSED_FRAMES_FOLDER,
        output_video_path=PROCESSED_VIDEO_PATH,
        fps=fps
    )

    return PROCESSED_VIDEO_PATH


def process_image(path_to_file: Path, mode: str) -> Path:
    """
    Dummy image processing for single image uploads (e.g., object detection or drawing overlays)
    Returns path to processed image.
    """
    print(f"Processing image at {path_to_file} with mode '{mode}'")

    try:
        # Open image
        image = Image.open(path_to_file).convert("RGB")
        draw = ImageDraw.Draw(image)

        if mode.lower() == "detection":
            # Draw dummy bounding box
            draw.rectangle([(50, 50), (250, 250)], outline="red", width=4)
            draw.text((60, 60), "Detected", fill="red")
        else:
            # Draw mode label
            draw.text((10, 10), f"Mode: {mode}", fill="blue")

        # Save output image
        output_path = path_to_file.parent / f"processed_{path_to_file.name}"
        image.save(output_path)

        print(f"Processed image saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error processing image: {e}")
        return path_to_file  # fallback
    