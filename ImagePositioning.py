from YoloAdapter import *
import logging
import cv2 as cv

"""~~Logging config~~"""
LOGGING_LEVEL = logging.INFO

"""~~Yolo config~~"""
CONFIDENCE_THRESHOLD = 0.5
NON_MAXIMUM_SUPPRESSION_THRESHOLD = 0.4
INPUT_WIDTH = 416
INPUT_HEIGHT = 416

PATH_CONFIGURATION = './YoloData/yolov3-tiny-cfg'
PATH_WEIGHT = './YoloData/{{some-weight-name}}'
PATH_CLASSES_FILE = './TrainingData/{{some-.data-name}}'

CLASSES = ['Nothing']

"""~~Environment config~~"""
CAMERA_DEVICE_INDEX = 0
DOBOT_DEVICE_INDEX = 1


def init():
    logging.basicConfig(level=LOGGING_LEVEL)


def show_frame(result: DetectionResult):
    classes = result.get_classes()
    frame = result.get_frame()
    objects = result.get_objects()

    for obj in objects:
        if type(obj) is ResultObject:
            fromX = obj.pos_x - obj.width
            fromY = obj.pos_y - obj.height
            toX = obj.pos_x + obj.width
            toY = obj.pos_y + obj.height
            cv.rectangle(frame, (fromX, fromY), (toX, toY), (0, 0, 255), 2)

            name = classes[obj.class_id]
            confidence = obj.confidence
            cv.putText(frame,
                       name + ' : ' + str(confidence),
                       (fromX, fromY - 10),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 255), 1, cv.LINE_AA)

    cv.imshow('Result', frame)


def mock_result(frame, classes):
    mock = DetectionResult(frame, classes)
    mock.add_object(ResultObject(120, 160, 40, 60, 0, 0.9))
    return mock


if __name__ == '__main__':
    init()
    # detector = YoloAdapter(CLASSES, PATH_CONFIGURATION, PATH_WEIGHT)
    video = cv.VideoCapture(CAMERA_DEVICE_INDEX)

    count = 1
    while True:
        has_frame, frame = video.read()

        if has_frame:
            # result = detector.detect(frame)
            result = mock_result(frame, CLASSES)
            show_frame(result)
            if count == 100:
                count = 1
                print(result.to_str())

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        count += 1

    video.release()
    cv.destroyAllWindows()



