from math import radians, cos, sin, asin, sqrt


# 比较经纬度
def PositionContrast(lng1, lat1, lng2, lat2, maxDis):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    if dis <= maxDis:
        return True
    else:
        return False


def demo(dict1, dict2):
    if PositionContrast(dict1.get('latitude'), dict1.get('longitude'), dict2.get('latitude'), dict2.get('longitude')):
        print("检测成功")
    else:
        print("检测失败")
# 测试
# place1={'latitude':123,'longitude':456}
# place2={'latitude':123,'longitude':455.9999999999}
# demo(place1,place2)
