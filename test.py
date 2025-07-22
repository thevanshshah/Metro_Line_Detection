import os
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

image_path = r'D:\IVA\SubwayDetectionAssistant\research\detection\img.png'
results = model(image_path)

img_with_boxes = results[0].plot()

# Save in the same folder as the input image
save_path = os.path.join(os.path.dirname(image_path), 'img_detected.png')

cv2.imwrite(save_path, img_with_boxes)
print(f"Saved detected image to {save_path}")
