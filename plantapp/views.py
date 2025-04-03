import io

import numpy
import torch
from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
import cv2

# 1) Allow POST requests without CSRF token (if desired for quick testing)
from django.views.decorators.csrf import csrf_exempt

# 2) Import the Ultralytics YOLO class
from ultralytics import YOLO

#############################################
# REMOVE or COMMENT OUT your old custom model
#
# import torch.nn as nn
# import torchvision.transforms as transforms
#
# class MyModel(nn.Module):
#     def __init__(self):
#         super(MyModel, self).__init__()
#         self.fc = nn.Linear(10, 2)  # Example placeholder
#     def forward(self, x):
#         return self.fc(x)
#
# (We no longer need the manual checkpoint loading either.)
#############################################

# 3) Load YOLOv8 model directly from my_model.pt
#    Make sure my_model.pt is a YOLOv8-trained model file.
model = YOLO("my_model.pt")

# Optional: if you want to do pre-processing transforms yourself,
# you can define them here. YOLO can often handle input as a PIL image directly.
# e.g., transforms = transforms.Compose([...])  # But not strictly required

def index(request):
    return render(request, "index.html")

@csrf_exempt
def predict(request):
    # 4) Handle only POST requests
    if request.method == "POST":
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)

        file = request.FILES["file"]
        
        try:
            # 5) Read the uploaded file into a PIL image
            img_bytes = file.read()
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            # 6) Run YOLO detection
            # model(...) returns a list of results; we’ll grab the first one
            results = model(image)  # or model.predict(image) in some versions
            result = results[0]

            # 7) Parse detection results (bounding boxes, class IDs, confidence)
            detection_data = []
            if hasattr(result, 'boxes'):
                # For YOLO object detection, each "box" has xyxy coords, confidence, class ID
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    detection_data.append({
                        "class_id": class_id,
                        "confidence": confidence,
                        "box": xyxy,
                    })
            else:
                # If this is a classification model, you’d parse differently
                # But YOLOv8 classification typically uses result.probs
                # Example:
                # detection_data = result.names  # or however you want to handle classification
                pass

            # 8) Return results as JSON
            return JsonResponse({"detections": detection_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
