# WebM Converter

WebMファイルをMP4とGIFに一括変換するシンプルなWebアプリケーションです。

![アプリケーションのデモ](./demo.gif)

## 特徴

- シンプルなドラッグ＆ドロップインターフェース
- プレビュー機能付き
- フォルダ選択機能
- 高品質なMP4/GIF出力
- 固定されたプレビュー画面で快適な操作性

## 必要条件

- Python 3.7以上
- FFmpeg
- モダンなWebブラウザ（Chrome, Firefox, Safari, Edge）

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/knagamatsu/webm-converter.git
cd webm-converter
```

2. 必要なPythonパッケージをインストール：
```bash
pip install flask
```

3. FFmpegのインストール：
   - Windows: [FFmpeg公式サイト](https://ffmpeg.org/download.html)からダウンロード
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## 使い方

1. サーバーを起動：
```bash
python server.py
```

2. ブラウザで以下のURLにアクセス：
```
http://localhost:5000
```

3. 使用方法：
   - フォルダ選択ボタンで変換したいWebMファイルがあるフォルダを選択（オプション）
   - 左サイドバーに表示されたWebMファイル一覧から変換したいファイルを選択
   - プレビューで内容を確認
   - 出力ファイル名を入力（デフォルトでは元のファイル名）
   - 「変換開始」ボタンをクリック
   - MP4とGIFが同じフォルダに生成されます

## ファイル構成

```
webm-converter/
├── server.py          # サーバーサイドスクリプト
├── index.html         # フロントエンドインターフェース
├── README.md          # このファイル
└── demo.gif           # デモンストレーション動画
```

## 仕様

### MP4変換設定
```python
ffmpeg -i input.webm -vf "scale=ceil(iw/2)*2:ceil(ih/2)*2" -r 30 output.mp4
```
- 30fps
- 元の解像度を維持（2の倍数に調整）

### GIF変換設定
```python
ffmpeg -i input.webm -vf "fps=5,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1" output.gif
```
- 15fps
- 幅640px（高さは自動調整）
- 高品質なカラーパレット生成
- lanczosスケーリングによる高品質な変換

## 注意事項

- 変換後のファイルは元のファイルと同じフォルダに保存されます
- 同名のファイルが存在する場合は上書きされます
- ファイルサイズによって変換時間が異なります

## ライセンス

MITライセンス