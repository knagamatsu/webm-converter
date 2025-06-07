# WebM Converter V3

WebMファイルをMP4とGIFに変換する、YouTubeスタイルのモダンなWebアプリケーションです。

![アプリケーションのデモ](./demo.gif)

## 特徴

- **YouTubeスタイルのグリッドレイアウト** - サムネイル付きで動画を一覧表示
- **自動サムネイル生成** - 各動画の1秒目から自動的にサムネイルを生成
- **モダンなUI** - Google Fonts (Inter)を使用した洗練されたデザイン
- **Webベースのフォルダブラウザ** - ブラウザ上で直接フォルダを選択可能
- **プレビュー機能** - 変換前に動画内容を確認
- **高品質な変換** - MP4とGIFを同時に生成
- **キャッシュ機能** - サムネイルをキャッシュして高速表示

## 必要条件

- Python 3.7以上
- FFmpeg
- モダンなWebブラウザ（Chrome, Firefox, Safari, Edge）
- uv (Python環境管理ツール)

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/knagamatsu/webm-converter.git
cd webm-converter
```

2. uvで環境をセットアップ：
```bash
uv init
uv venv
uv add flask
```

3. FFmpegのインストール：
   - Windows: [FFmpeg公式サイト](https://ffmpeg.org/download.html)からダウンロード
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## 使い方

1. サーバーを起動：
```bash
uv run python server.py
```

2. ブラウザで以下のURLにアクセス：
```
http://localhost:5000
```

3. 使用方法：
   - フォルダ選択ボタンでWebMファイルがあるフォルダを選択
   - グリッド表示された動画サムネイルから変換したいファイルをクリック
   - モーダルウィンドウでプレビューを確認
   - 出力ファイル名を編集（デフォルトでは元のファイル名）
   - 「MP4とGIFに変換」ボタンをクリック
   - 変換完了後、MP4とGIFが同じフォルダに生成されます

## ファイル構成

```
webm-converter-v3/
├── server.py          # Flaskサーバー（サムネイル生成、ファイル変換）
├── index.html         # フロントエンド（YouTubeスタイルUI）
├── pyproject.toml     # uv依存関係設定
├── uv.lock           # 依存関係ロックファイル
├── .gitignore        # Git除外設定
├── .thumbnails/      # サムネイルキャッシュ（自動生成）
├── README.md         # このファイル
└── demo.gif          # デモンストレーション動画
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
- 5fps
- 幅640px（高さは自動調整）
- 高品質なカラーパレット生成
- lanczosスケーリングによる高品質な変換

### サムネイル生成設定
```python
ffmpeg -i input.webm -ss 00:00:01 -vframes 1 -vf scale=320:-1 thumbnail.jpg
```
- 動画の1秒目から生成
- 幅320px（高さは自動調整）
- JPG形式でキャッシュ

## 主な改善点 (V3)

- **UIの刷新**: YouTubeライクなグリッドレイアウトを採用
- **サムネイル機能**: 動画の自動サムネイル生成とキャッシュ
- **フォルダブラウザ**: Webベースのフォルダ選択（tkinter不要）
- **モダンなデザイン**: Google Fontsを使用した洗練されたUI
- **UXの向上**: モーダルウィンドウでの直感的な操作

## 注意事項

- 変換後のファイルは元のファイルと同じフォルダに保存されます
- 同名のファイルが存在する場合は上書きされます
- ファイルサイズによって変換時間が異なります
- デフォルトでUbuntuの`~/Videos/スクリーンキャスト`フォルダを表示

## ライセンス

MITライセンス