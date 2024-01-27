import time
import requests
from util import LatLon
from API_KEY import MAPBOX_API_KEY

import matplotlib.pyplot as plt

plt.style.use("ggplot")

URL_BASE = "https://api.mapbox.com/directions/v5/mapbox"


def search(point1: LatLon, point2: LatLon, sleep_time: int = 2) -> list[LatLon]:
    """
    Mapbox APIに投げて簡易緯度経度列を取得する
    """
    time.sleep(sleep_time)
    url = f"{URL_BASE}/walking/{point1.lon},{point1.lat};{point2.lon},{point2.lat}?access_token={MAPBOX_API_KEY}&geometries=geojson"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    # route
    ret = []
    data = res.json()
    for elem in data["routes"][0]["geometry"]["coordinates"]:
        ret.append(LatLon(elem[1], elem[0]))
    return ret


if __name__ == "__main__":
    point1 = LatLon(35.66327949317488, 139.7452778147842)
    point2 = LatLon(35.65900818537974, 139.74570696819524)
    ret = search(point1, point2)
    print(ret)

    f = plt.figure(figsize=(5, 5))
    a = f.gca()
    a.plot([p.lon for p in ret], [p.lat for p in ret], color="k", lw=2)
    a.scatter([point1.lon], [point1.lat], marker="o")
    a.scatter([point2.lon], [point2.lat], marker="x")
    plt.tight_layout()
    plt.show()
    plt.close()
