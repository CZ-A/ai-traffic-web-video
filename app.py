from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Daftar URL dan video yang akan digunakan
list_URL = []
list_Video = []

# Fungsi untuk menambahkan URL
@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if url:
        list_URL.append(url)
        return jsonify({"message": "URL added successfully!"}), 200
    return jsonify({"error": "URL not provided"}), 400

# Fungsi untuk menambahkan video URL
@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    video_url = data.get("video_url")
    if video_url:
        list_Video.append(video_url)
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

# Fungsi untuk menghasilkan traffic web
@app.route('/generate_traffic', methods=['POST'])
def generate_traffic():
    data = request.get_json()
    type_traffic = data.get("type")
    num_requests = int(data.get("num_requests", 1))

    if type_traffic == "web":
        for _ in range(num_requests):
            for url in list_URL:
                try:
                    response = requests.get(url)
                    print(f"Web Traffic to {url}: {response.status_code}")
                except Exception as e:
                    print(f"Error with {url}: {str(e)}")
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
    app.run(debug=True)
