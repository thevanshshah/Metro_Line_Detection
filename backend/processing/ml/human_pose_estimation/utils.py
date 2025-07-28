from ultralytics import YOLO
from pathlib import Path
import torch
from ultralytics.utils.plotting import Annotator
import cv2

model = YOLO('./yolov8m-pose.pt')

# Human Pose Estimation function
async def hpe_images(input_folder: Path, output_folder: Path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Function: {hpe_images.__name__}. Device: {device}")

    global model
    model.to(device)

    with torch.no_grad():
        results = model.predict(
            source=input_folder,
            save=True,
            project="processed",
            name="hpe_frames",
            conf=0.3,
            exist_ok=True
        )

    return results

# ✅ Updated check_danger logic
def check_danger(img_path, box):
    """
    Determines if a person is in danger based on whether their feet
    (bottom 10% of the bounding box) intersect with the yellow segmented line.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    left, top, right, bottom = map(int, box)

    # Define the foot region (bottom 10% of the person box)
    foot_top = bottom - int((bottom - top) * 0.1)

    # Clip boundaries
    foot_top = max(0, foot_top)
    bottom = min(img.shape[0] - 1, bottom)
    left = max(0, left)
    right = min(img.shape[1] - 1, right)

    foot_region = img[foot_top:bottom, left:right]

    if foot_region.size == 0:
        return False  # Cannot decide

    # Count white pixels in foot region (white = yellow segment)
    white_pixel_ratio = (foot_region > 128).sum() / foot_region.size

    # Danger if ≥10% of foot area overlaps with yellow line
    return white_pixel_ratio >= 0.1

# Overlays bounding boxes on original image
def project_hpe_onto(hpe_results, segmented_folder: Path, project_onto_folder: Path, output_folder: Path):
    for i, result in enumerate(hpe_results):
        img_path = project_onto_folder.absolute().as_posix() + "/" + Path(result.path).name
        img = cv2.imread(img_path)
        annotator = Annotator(img)

        segmented_img_path = segmented_folder.absolute().as_posix() + "/" + Path(result.path).name

        boxes = result.boxes
        for box in boxes:
            b = box.xyxy[0]  # (left, top, right, bottom)
            in_danger = check_danger(segmented_img_path, b)
            
            # ✅ Label and color
            label = "DANGER" if in_danger else "SAFE"
            color = (0, 0, 255) if in_danger else (0, 255, 0)

            annotator.box_label(b, label, color=color)

        result_img = annotator.result()
        result_filename = output_folder.absolute().as_posix() + "/" + Path(result.path).name
        cv2.imwrite(result_filename, result_img)
