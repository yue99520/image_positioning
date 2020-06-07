import cv2 as cv
from yolo_detector_tool.yolo_detection_adapter.YoloAdapter import YoloAdapter

CONFIGURATION_PATH = '../cfg/yolov3.cfg'
WEIGHT_PATH = '../data/yolov3.weights'
CLASS_FILE_PATH = '../data/coco.names'

cap = cv.VideoCapture(0)

has_frame, frame = cap.read()

with open(CLASS_FILE_PATH, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
    yolo_adapter = YoloAdapter(classes, CONFIGURATION_PATH, WEIGHT_PATH)
    result = yolo_adapter.detect(frame)
    print(result.__str__())
