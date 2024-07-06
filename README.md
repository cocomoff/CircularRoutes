# Circular Routes


- 中心の周辺をジョギングできるようなルートを探したい


## 処理

### V2

- 経路の角を掃除する

### V1

- Zenn: https://zenn.dev/takilog/articles/575c58ed6b57de

- やったこと
  - 簡単実装: 中心点の周りに点を打ち、間の経路を探す
  - 間の経路はDirectionsAPI (e.g., Mapbox) で探す
    - API KEYは `./src/API_KEY.py` に置く (中身: `MAPBOX_API_KEY=XXXXXXX`)

#### geojsonの可視化例

![例の画像](outputs/vis-example.png)


#### Matplotlibの可視化

- 円上に点を打つ

![例の画像(円)](outputs/example-circle.png)


- 個別で経路を問い合わせる

![例の画像(経路)](output/sexample.png)