import cv2
import torch
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = YOLO('app/model.pt')
model.to(device)
model.eval()

def get_prediction(img_array):
    results = model(img_array)  # includes NMS
    annotator = Annotator(img_array)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)], (200,0,0))

    image = annotator.result()
    return image, results


class PredictCamera(object):
    def __init__(self):
        self.data_result = None
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        result = get_prediction(frame)
        image_result = result[0]
        self.data_result = result[1]

        ret, jpeg = cv2.imencode('.jpg', image_result)

        return jpeg.tobytes()

    def get_data(self):
        if self.data_result is None:
            return "Nothing detected"
        else:
            output = ""
            for r in self.data_result:
                output = r.to_json()
            return f"{output}"

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#         ret, frame = self.video.read()
#
#         # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
#
#         ret, jpeg = cv2.imencode('.jpg', frame)
#
#         return jpeg.tobytes()