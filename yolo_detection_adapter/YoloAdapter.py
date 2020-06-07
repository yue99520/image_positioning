import cv2 as cv
import numpy as np
from yolo_detector_tool.yolo_detection_adapter import ResultObject
from yolo_detector_tool.yolo_detection_adapter import DetectionResult


class YoloAdapter:
    CONFIDENCE_THRESHOLD = 0.5
    NON_MAXIMUM_SUPPRESSION_THRESHOLD = 0.4
    INPUT_WIDTH = 416
    INPUT_HEIGHT = 416

    _classes = None
    _configuration_path = None
    _weights_path = None
    _net = None

    _scale_factor = 1 / 255
    _special_size = (INPUT_WIDTH, INPUT_HEIGHT)
    _mean = [0, 0, 0]
    _swapRB = 1
    _crop = False

    def __init__(self, classes, configuration_path, weights_path):
        self._classes = classes
        self._configuration_path = configuration_path
        self._weights_path = weights_path
        self._get_dark_net()

    def detect(self, frame):
        after_blob_image = cv.dnn.blobFromImage(frame,
                                                self._scale_factor,
                                                self._special_size,
                                                self._mean,
                                                self._swapRB,
                                                self._crop)
        return self._generate_result(after_blob_image, frame)

    def _generate_result(self, after_blob_image, frame):
        self._net.setInput(after_blob_image)
        names = self._get_output_names(self._net)
        results = self._net.forward(names)
        return self._detection_result_factory(frame, results)

    def _detection_result_factory(self, frame, raw_results):
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        class_ids = []
        confidences = []
        boxes = []
        widths = []
        heights = []
        for result in raw_results:
            for detection in result:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)

                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)

                left = int(center_x - width / 2)
                top = int(center_y - height / 2)

                if confidence > self.CONFIDENCE_THRESHOLD:
                    widths.append(width)
                    heights.append(height)

                    class_ids.append(class_id)
                    boxes.append([left, top, width, height])
                    confidences.append(float(confidence))

        indices = cv.dnn.NMSBoxes(boxes, confidences,
                                  self.CONFIDENCE_THRESHOLD,
                                  self.NON_MAXIMUM_SUPPRESSION_THRESHOLD)

        result = DetectionResult(frame, self._classes)

        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            pos_x = left + width * 2
            pos_y = top + height * 2
            obj = ResultObject(pos_x, pos_y, width, height, class_ids[i], confidences[i])
            result.add_object(obj)

        return result

    def _get_dark_net(self, target: str = cv.dnn.DNN_TARGET_CPU):
        self._net = cv.dnn.readNetFromDarknet(self._configuration_path, self._weights_path)
        self._net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self._net.setPreferableTarget(target)

    @staticmethod
    def _get_output_names(net):
        layers_names = net.getLayerNames()
        return [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
