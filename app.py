from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import os

app = Flask(__name__)

# Inisialisasi daftar URL dan video
list_URL = []
list_Video = []

# Fungsi untuk memuat data dari file JSON
def load_data():
    global list_URL, list_Video
    if os.path.exists("url_list.json"):
        with open("url_list.json", "r") as url_file:
            list_URL = json.load(url_file)
    if os.path.exists("video_list.json"):
        with open("video_list.json", "r") as video_file:
            list_Video = json.load(video_file)

# Fungsi untuk menyimpan data ke file JSON
def save_data():
    with open("url_list.json", "w") as url_file:
        json.dump(list_URL, url_file, indent=4)
    with open("video_list.json", "w") as video_file:
        json.dump(list_Video, video_file, indent=4)

# Fungsi untuk menambahkan URL
@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if url:
        list_URL.append(url)
        save_data()  # Simpan perubahan ke file
        return jsonify({"message": "URL added successfully!"}), 200
    return jsonify({"error": "URL not provided"}), 400

# Fungsi untuk menambahkan video URL
@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    video_url = data.get("video_url")
    if video_url:
        list_Video.append(video_url)
        save_data()  # Simpan perubahan ke file
        return jsonify({"message": "Video added successfully!"}), 200
    return jsonify({"error": "Video URL not provided"}), 400

# Fungsi untuk mengambil semua URL
@app.route('/get_urls', methods=['GET'])
def get_urls():
    return jsonify({"urls": list_URL}), 200

# Fungsi untuk mengambil semua video URL
@app.route('/get_videos', methods=['GET'])
def get_videos():
    return jsonify({"videos": list_Video}), 200

# Fungsi untuk menghasilkan traffic web dan video menggunakan Selenium
@app.route('/generate_traffic', methods=['POST'])
def generate_traffic():
    data = request.get_json()
    type_traffic = data.get("type")
    num_requests = int(data.get("num_requests", 1))

    if type_traffic == "web":
        options = Options()
        options.add_argument("--headless")  # Menggunakan mode headless
        service = Service("./chromedriver/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        # Membuka URL yang ada di list_URL menggunakan Selenium
        for _ in range(num_requests):
            for url in list_URL:
                try:
                    driver.get(url)  # Mengakses URL menggunakan Selenium
                    time.sleep(3)  # Tunggu agar halaman sepenuhnya dimuat
                    print(f"Web Traffic to {url}")
                except Exception as e:
                    print(f"Error with {url}: {str(e)}")

        driver.quit()
        return jsonify({"message": f"Generated {num_requests} web traffic requests"}), 200

    elif type_traffic == "video":
        options = Options()
        options.add_argument("--headless")  # Menggunakan mode headless
        service = Service("./chromedriver/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        for _ in range(num_requests):
            for video_url in list_Video:
                try:
                    driver.get(video_url)
                    time.sleep(3)  # Menunggu video dimuat
                    print(f"Video Traffic to {video_url}")
                except Exception as e:
                    print(f"Error with video {video_url}: {str(e)}")

        driver.quit()
        return jsonify({"message": f"Generated {num_requests} video traffic requests"}), 200

    return jsonify({"error": "Invalid traffic type"}), 400

if __name__ == '__main__':
    load_data()  # Memuat data dari file saat aplikasi dimulai
    app.run(debug=True)