from collections import namedtuple
from math import radians, cos, sin, asin, sqrt

# 緯度経度 (サービスによって (lat, lon), (lon, lat) だったりするので、注意する)
LatLon = namedtuple("LatLon", ["lat", "lon"])

# クエリ (start -> goal)
Query = namedtuple("Query", ["src", "dst"])


def haversine(point1: LatLon, point2: LatLon) -> float:
    """
    緯度経度距離
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(
        radians, [point1.lon, point1.lat, point2.lon, point2.lat]
    )
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


if __name__ == "__main__":
    # Havesine距離の例
    # see: https://qiita.com/tomopict/items/c5661b48aa705d289cce
    point1 = LatLon(35.681283, 139.766765)
    point2 = LatLon(35.170406, 136.881695)
    print(haversine(point1, point2))
