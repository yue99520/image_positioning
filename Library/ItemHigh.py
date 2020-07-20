from Config import FOCAL_LENGTH


"""
    由實際距離與攝影機焦距取得物品實際高度
    @param distance 物品距離攝像頭的距離（公分）
    @param virtual_length 圖片中物品的虛擬高度（pixel）
"""


def calculate_item_high(distance, virtual_length):
    item_high = float(distance) * float(virtual_length) / FOCAL_LENGTH
    return item_high
