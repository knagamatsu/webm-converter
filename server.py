from flask import Flask, request, jsonify, send_file, send_from_directory
import subprocess
import os
import tkinter as tk
from tkinter import filedialog
import hashlib
import time

app = Flask(__name__)

# グローバル変数として作業ディレクトリを保持
class Config:
    # Ubuntuのデフォルトスクリーンキャストフォルダ
    DEFAULT_SCREENCAST_DIR = os.path.expanduser("~/Videos/スクリーンキャスト")
    # 初期作業ディレクトリ（スクリーンキャストフォルダが存在すればそれを使用）
    WORK_DIR = DEFAULT_SCREENCAST_DIR if os.path.exists(DEFAULT_SCREENCAST_DIR) else os.path.dirname(os.path.abspath(__file__))
    # サムネイルキャッシュディレクトリ
    THUMBNAIL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.thumbnails')

# サムネイルディレクトリを作成
if not os.path.exists(Config.THUMBNAIL_DIR):
    os.makedirs(Config.THUMBNAIL_DIR)

def select_folder_dialog():
    """フォルダ選択ダイアログを表示"""
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示
    folder = filedialog.askdirectory(
        initialdir=Config.WORK_DIR,
        title='変換するWebMファイルがあるフォルダを選択'
    )
    root.destroy()
    return folder

def get_webm_files():
    """作業ディレクトリ内のWebMファイルを取得（詳細情報付き）"""
    files = []
    for f in os.listdir(Config.WORK_DIR):
        if f.lower().endswith('.webm'):
            file_path = os.path.join(Config.WORK_DIR, f)
            stats = os.stat(file_path)
            files.append({
                'name': f,
                'size': stats.st_size,
                'modified': stats.st_mtime
            })
    return sorted(files, key=lambda x: x['modified'], reverse=True)

def generate_thumbnail(video_path, output_path):
    """動画からサムネイルを生成"""
    try:
        # ffmpegを使用して動画の1秒目からサムネイルを生成
        subprocess.run([
            'ffmpeg', '-i', video_path,
            '-ss', '00:00:01',
            '-vframes', '1',
            '-vf', 'scale=320:-1',
            '-y',
            output_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/current-path')
def get_current_path():
    """現在の作業ディレクトリを返す"""
    return jsonify({'path': Config.WORK_DIR})

@app.route('/select-folder')
def select_folder():
    """フォルダ選択ダイアログを表示し、作業ディレクトリを更新"""
    try:
        folder = select_folder_dialog()
        if folder:
            Config.WORK_DIR = folder
            return jsonify({'success': True, 'path': Config.WORK_DIR})
        return jsonify({'success': True, 'path': Config.WORK_DIR})  # フォルダ未選択の場合は現在のパスを返す
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/list-files')
def list_files():
    """WebMファイルの一覧を返す"""
    return jsonify(get_webm_files())

@app.route('/thumbnail/<filename>')
def get_thumbnail(filename):
    """サムネイルを取得または生成"""
    # ファイル名のハッシュをサムネイル名として使用
    file_path = os.path.join(Config.WORK_DIR, filename)
    file_hash = hashlib.md5(f"{filename}_{os.path.getmtime(file_path)}".encode()).hexdigest()
    thumbnail_path = os.path.join(Config.THUMBNAIL_DIR, f"{file_hash}.jpg")
    
    # サムネイルが存在しない場合は生成
    if not os.path.exists(thumbnail_path):
        if not generate_thumbnail(file_path, thumbnail_path):
            # サムネイル生成に失敗した場合は404を返す
            return jsonify({'error': 'サムネイル生成エラー'}), 404
    
    return send_file(thumbnail_path, mimetype='image/jpeg')

@app.route('/video/<filename>')
def serve_video(filename):
    """動画ファイルを提供"""
    return send_from_directory(Config.WORK_DIR, filename)

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.get_json()
    input_file = data.get('inputFile')
    output_name = data.get('outputName')

    if not input_file or not output_name:
        return jsonify({'error': '入力ファイルと出力ファイル名が必要です'}), 400

    try:
        input_path = os.path.join(Config.WORK_DIR, input_file)
        mp4_output_path = os.path.join(Config.WORK_DIR, f"{output_name}.mp4")
        gif_output_path = os.path.join(Config.WORK_DIR, f"{output_name}.gif")

        if not os.path.exists(input_path):
            return jsonify({'error': '入力ファイルが見つかりません'}), 404

        # MP4への変換
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-vf', 'scale=ceil(iw/2)*2:ceil(ih/2)*2',
            '-r', '30',
            '-y',
            mp4_output_path
        ], check=True)

        # GIFへの変換
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-vf', 'fps=5,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1',
            '-loop', '0',
            '-y',
            gif_output_path
        ], check=True)

        return jsonify({'success': True})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'変換エラー: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)