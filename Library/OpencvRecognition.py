def recognize_from_xy(image):
    # detect something in image by using opencv
    coord = Coordinate()
    highest_conf = 0
    item = None
    for position in virtual_positions:
        pos_id = position.id

        if pos_id is COORD_ORIGIN_ID:
            coord.origin = position
        elif pos_id is COORD_X_ID:
            coord.x = position
        elif pos_id is COORD_Y_ID:
            coord.y = position
        elif position.confidence > highest_conf:
            item = position

    return coord, item


def recognize_from_z(net: Darknet, image, find_id):
    # detect something in image by using opencv
    highest_conf = 0
    item = None
    for position in virtual_positions:
        pos_id = position.id
        if position.confidence > highest_conf and pos_id is find_id:
            item = position
    return item
