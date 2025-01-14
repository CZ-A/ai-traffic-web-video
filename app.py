from flask import Flask, request, jsonify, render_template
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# File JSON
URLS_FILE = "urls.json"
VIDEOS_FILE = "videos.json"

# Global Variables
list_URL = []
list_Video = []

# Fungsi untuk memuat data dari file JSON
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file_path}. Initializing empty list.")
    return []

# Fungsi untuk menyimpan data ke file JSON
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Load data saat aplikasi dimulai
list_URL = load_data(URLS_FILE)
list_Video = load_data(VIDEOS_FILE)

# Route untuk homepage
@app.route('/')
def index():
    return render_template('index.html', url_list=list_URL, video_list=list_Video)

# Route untuk menambahkan URL
@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if url and url.startswith("http"):
        list_URL.append(url)
        save_data(URLS_FILE, list_URL)  # Simpan ke urls.json
        return jsonify({"message": "URL added successfully!"}), 200
    return jsonify({"error": "Invalid or missing URL"}), 400


# Route untuk menambahkan video URL
@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    video_url = data.get("video_url")
    if video_url and video_url.startswith("http"):
        list_Video.append(video_url)
        save_data(VIDEOS_FILE, list_Video)  # Simpan ke videos.json
        return jsonify({"message": "Video added successfully!"}), 200
    return jsonify({"error": "Invalid or missing Video URL"}), 400

# Route untuk mendapatkan semua URL
@app.route('/get_urls', methods=['GET'])
def get_urls():
    return jsonify({"urls": list_URL}), 200

# Route untuk mendapatkan semua video URL
@app.route('/get_videos', methods=['GET'])
def get_videos():
    return jsonify({"videos": list_Video}), 200

# Route untuk menghasilkan traffic
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
        options.add_argument("--headless")
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

if __name__ == '__main__':
    app.run(debug=True)