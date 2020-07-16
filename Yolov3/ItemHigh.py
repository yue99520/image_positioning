class ItemHigh:
    def calculate_item_high(self,distance,imageLength):
        FocalLength = 570 ##單位為pixel
        ##imageLength 圖片中物品的pixel
        ##distance    物品距離攝像頭的距離
        ItemHigh = float(distance)*float(imageLength)/FocalLength
        print(ItemHigh)