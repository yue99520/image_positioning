from Library.Entity import Coordinate


"""
依據座標系統計算物品的真實座標
coord: 座標系統物件
virtualPosition: 物品虛擬位置
return x, y 單位公分
"""
x1 = 0
y1 = 0


def find_real_position(coord: Coordinate, virtualPosition):
     if virtualPosition.id =="Origin":
          x1 = virtualPosition.x
          y1 = virtualPosition.y
         # 如果為圓形(原點)則將該座標設為(0,0)
     coord.origin=(0,0)
     coord.x=(virtualPosition.x-x1) /44.84 #(虛擬x座標-原點為0時所減去的數值)/44.84(比例)
     coord.y=(virtualPosition.y-y1)/44.84 #(虛擬y座標-原點為0時所減去的數值)/44.84(比例)
     return coord.x , coord.y