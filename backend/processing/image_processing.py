# processing/image_processing.py

from pathlib import Path
import cv2

async def process_image(path_to_file: Path, mode: str) -> Path:
    img = cv2.imread(str(path_to_file))

    # Example detection/processing logic (e.g., drawing a rectangle)
    if mode == "demo":
        h, w, _ = img.shape
        cv2.rectangle(img, (int(w*0.3), int(h*0.3)), (int(w*0.7), int(h*0.7)), (0, 0, 255), 4)

    # Save processed image
    processed_path = path_to_file.parent / f"processed_{path_to_file.name}"
    cv2.imwrite(str(processed_path), img)
    return processed_path
