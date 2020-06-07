from YoloAdapter.ResultObject import ResultObject


class DetectionResult:

    def __init__(self, frame, classes):
        self._frame = frame
        self._classes = classes
        self._objects = []

    def add_object(self, obj: ResultObject):
        self._objects.append(obj)

    def get_objects(self):
        return self._objects

    def get_frame(self):
        return self._frame

    def get_classes(self):
        return self._classes

    def to_str(self):
        str = ''
        for obj in self._objects:
            str += self._classes[obj.class_id] + ' >>>  ' + obj.to_str() + '\n'
        return str