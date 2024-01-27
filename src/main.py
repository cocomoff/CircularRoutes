import matplotlib.pyplot as plt
import numpy as np
from util import haversine, LatLon, Query

plt.style.use("ggplot")


def compute_points(point: LatLon, dist: float = 3, N: int = 6) -> list[Query]:
    # 中心から0.1動いたときの距離を測定する
    dx_point = LatLon(point.lat + 0.1, point.lon)
    dy_point = LatLon(point.lat, point.lon + 0.1)
    dx = haversine(point, dx_point)
    dy = haversine(point, dy_point)
    avg = (dx + dy) / 2
    print(f"Lat+0.1: {dx} [km]")
    print(f"Lon+0.1: {dy} [km]")
    print(f"Avg    : {avg} [km]")

    # 距離 `dist` を達成するための、緯度経度数値の必要量
    desired_value = dist / avg * 0.1
    print(f"Des    : {desired_value}")

    # 半径は必要量 2 pi r が必要量になる半径
    radius = desired_value / (2 * np.pi)
    print(f"Rad    : {radius}")

    # 中心 `point`、半径 `radius` の円に `N` 個の点を置く
    ret_points = []
    theta = np.linspace(0, 2 * np.pi, num=N, endpoint=False)
    seqLat = point.lat + radius * np.cos(theta)
    seqLon = point.lon + radius * np.sin(theta)
    for j in range(len(seqLat)):
        ret_points.append(LatLon(seqLat[j], seqLon[j]))

    # 検索クエリ
    ret_query = []

    # 可視化
    f = plt.figure(figsize=(5, 5))
    a = f.gca()
    sum_dist = 0.0
    for i in range(N):
        j = (i + 1) % N
        pi = LatLon(seqLat[i], seqLon[i])
        pj = LatLon(seqLat[j], seqLon[j])
        ret_query.append(Query(pi, pj))
        dij = haversine(pi, pj)
        sum_dist += dij
        a.plot(seqLon[[i, j]], seqLat[[i, j]], color="k")
    a.set_title(f"Dist(Hav) {sum_dist:>.3f}")
    a.scatter(seqLon, seqLat, marker="o")
    plt.tight_layout()
    plt.show()
    plt.close()

    return ret_points, ret_query


def draw_geojson(points: list[LatLon], queries: list[Query], fn: str) -> None:
    pass


if __name__ == "__main__":
    point_tokyo_tower = LatLon(35.658581, 139.745433)
    points, queries = compute_points(point_tokyo_tower, dist=3, N=10)

    # データをgithubで可視化するためのgeojsonつくり
    draw_geojson(points, queries, fn="geojson/sample.geojson")
