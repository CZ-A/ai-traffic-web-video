from flask import Flask, request, jsonify, render_template
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# File untuk menyimpan URL dan Video URL
URLS_FILE = "urls.json"
VIDEOS_FILE = "videos.json"

# Fungsi untuk memuat data dari file JSON
def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Fungsi untuk menyimpan data ke file JSON
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Inisialisasi daftar URL dan Video URL
list_URL = load_data(URLS_FILE)
list_Video = load_data(VIDEOS_FILE)

# Endpoint untuk menambahkan URL
@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if url and url.startswith("http"):
        list_URL.append(url)
        save_data(URLS_FILE, list_URL)  # Simpan ke urls.json
        return jsonify({"message": "URL added successfully!"}), 200
    return jsonify({"error": "Invalid or missing URL"}), 400

# Endpoint untuk menambahkan Video URL
@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    video_url = data.get("video_url")
    if video_url and video_url.startswith("http"):
        list_Video.append(video_url)
        save_data(VIDEOS_FILE, list_Video)  # Simpan ke videos.json
        return jsonify({"message": "Video added successfully!"}), 200
    return jsonify({"error": "Invalid or missing Video URL"}), 400

# Endpoint untuk menghasilkan traffic menggunakan Selenium
@app.route('/generate_traffic', methods=['POST'])
def generate_traffic():
    data = request.get_json()
    type_traffic = data.get("type")
    num_requests = int(data.get("num_requests", 1))

    if type_traffic == "web":
        for _ in range(num_requests):
            for url in list_URL:
                try:
                    print(f"Simulating web traffic to {url}")
                except Exception as e:
                    print(f"Error with {url}: {str(e)}")
        return jsonify({"message": f"Generated {num_requests} web traffic requests"}), 200

    elif type_traffic == "video":
        options = Options()
        options.add_argument("--headless")  # Menggunakan mode headless
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service("./chromedriver/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        for _ in range(num_requests):
            for video_url in list_Video:
                try:
                    driver.get(video_url)
                    time.sleep(3)  # Tunggu video dimuat
                    print(f"Video Traffic to {video_url}")
                except Exception as e:
                    print(f"Error with video {video_url}: {str(e)}")

        driver.quit()
        return jsonify({"message": f"Generated {num_requests} video traffic requests"}), 200

    return jsonify({"error": "Invalid traffic type"}), 400

# Endpoint untuk menampilkan halaman utama
@app.route('/')
def index():
    return render_template('index.html', url_list=list_URL, video_list=list_Video)

if __name__ == '__main__':
    # Pastikan file JSON ada dan berisi data kosong jika belum dibuat
    if not os.path.exists(URLS_FILE):
        save_data(URLS_FILE, [])
    if not os.path.exists(VIDEOS_FILE):
        save_data(VIDEOS_FILE, [])

    app.run(debug=True)