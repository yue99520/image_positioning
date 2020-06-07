from yolo_detector_tool.yolo_detection_adapter import ResultObject


class DetectionResult:
    _classes = None
    _objects = []
    _frame = None

    def __init__(self, frame, classes):
        self._frame = frame
        self._classes = classes

    def add_object(self, obj: ResultObject):
        self._objects.append(obj)

    def get_object(self):
        return self._objects

    def get_frame(self):
        return self._frame

    def get_classes(self):
        return self._classes