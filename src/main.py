import json
import matplotlib.pyplot as plt
import numpy as np
from util import haversine, LatLon, Query
from call_mapbox import search

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
    plt.savefig("example-circle.png")
    plt.close()

    return ret_points, ret_query


def draw_geojson(points: list[LatLon], queries: list[Query], fn: str) -> None:
    geojson = {"type": "FeatureCollection", "features": []}

    # 地点はPoint
    for point in points:
        f = {
            "type": "Feature",
            "properties": {
                "marker-color": "#000000",
                "marker-size": "medium",
            },
            "geometry": {"type": "Point", "coordinates": [point.lon, point.lat]},
        }
        geojson["features"].append(f)

    # クエリする直線はLineString
    for query in queries:
        point1 = query.src
        point2 = query.dst
        f = {
            "type": "Feature",
            "properties": {
                "stroke": "#0000FF",
                "stroke-width": 2,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[point1.lon, point1.lat], [point2.lon, point2.lat]],
            },
        }
        geojson["features"].append(f)

    # 出力
    with open(fn, "w") as fp:
        json.dump(geojson, fp)


if __name__ == "__main__":
    point_tokyo_tower = LatLon(35.658581, 139.745433)
    points, queries = compute_points(point_tokyo_tower, dist=3, N=10)

    # データをgithubで可視化するためのgeojsonつくり
    # draw_geojson(points, queries, fn="geojson/sample.geojson")

    # 可視化する (w/ query)
    seq_latlons = []
    for q in queries:
        ret = search(q.src, q.dst)
        seq_latlons.append(ret)

    f = plt.figure()
    a = plt.gca()
    for ret in seq_latlons:
        a.plot([p.lon for p in ret], [p.lat for p in ret], color="k", lw=2)
    a.scatter([p.lon for p in points], [p.lat for p in points], marker="o")
    plt.tight_layout()
    plt.savefig("example.png")
    plt.show()
    plt.close()
