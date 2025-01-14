import json
import os
import threading
from flask import Flask, jsonify, render_template

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Global variables
list_URL = []
list_Video = []

def load_data():
    global list_URL, list_Video
    # Memuat data untuk URL dari file urls.json
    if os.path.exists("urls.json") and os.path.getsize("urls.json") > 0:
        try:
            with open("urls.json", "r") as url_file:
                list_URL = json.load(url_file)
        except json.JSONDecodeError:
            print("Error decoding JSON in urls.json. Initializing empty list.")
            list_URL = []  # Inisialisasi dengan list kosong jika terjadi error
    else:
        list_URL = []  # Inisialisasi dengan list kosong jika file tidak ada atau kosong

    # Memuat data untuk Video dari file videos.json
    if os.path.exists("videos.json") and os.path.getsize("videos.json") > 0:
        try:
            with open("videos.json", "r") as video_file:
                list_Video = json.load(video_file)
        except json.JSONDecodeError:
            print("Error decoding JSON in videos.json. Initializing empty list.")
            list_Video = []  # Inisialisasi dengan list kosong jika terjadi error
    else:
        list_Video = []  # Inisialisasi dengan list kosong jika file tidak ada atau kosong

# Fungsi untuk menjalankan server
def run_server():
    app.run(debug=True, use_reloader=False)  # Gunakan use_reloader=False untuk mencegah aplikasi berjalan dua kali

# Route untuk homepage
@app.route('/')
def home():
    return render_template('index.html', url_list=list_URL, video_list=list_Video)

# Route untuk mendapatkan data URL dalam format JSON
@app.route('/api/urls')
def get_urls():
    return jsonify(list_URL)

# Route untuk mendapatkan data video dalam format JSON
@app.route('/api/videos')
def get_videos():
    return jsonify(list_Video)

if __name__ == '__main__':
    load_data()  # Memuat data dari file saat aplikasi dimulai
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
