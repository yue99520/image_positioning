class ResultObject:
    pos_x = None
    pos_y = None
    width = None
    height = None
    class_id = None
    confidence = None

    def __init__(self, pos_x, pos_y, width, height, class_id, confidence):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.class_id = class_id
        self.confidence = confidence

    def to_str(self):
        return 'x: ' + str(self.pos_x) + ', y: ' + str(self.pos_y)
