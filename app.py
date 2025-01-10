from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
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

# Fungsi untuk menghasilkan trafik web dan video menggunakan Selenium
@app.route('/generate_traffic', methods=['POST'])
def generate_traffic():
    data = request.get_json()
    type_traffic = data.get("type")
    num_requests = int(data.get("num_requests", 1))

    if type_traffic == "web":
        options = Options()
        options.add_argument("--headless")  # Menggunakan mode headless
        options.add_argument('--disable-gpu')  # Menghindari masalah dengan GPU di beberapa sistem
        options.add_argument('--no-sandbox')  # Menjalankan di lingkungan aman
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # User-Agent
        service = Service("./chromedriver/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        # Membuka URL yang ada di list_URL menggunakan Selenium
        for _ in range(num_requests):
            for url in list_URL:
                try:
                    driver.get(url)  # Mengakses URL menggunakan Selenium
                    time.sleep(random.randint(5, 10))  # Tunggu agar halaman sepenuhnya dimuat (meniru pengunjung nyata)
                    print(f"Web Traffic to {url}")

                    # Simulasikan pengunjung nyata (scrolling dan klik acak)
                    body = driver.find_element("tag name", "body")
                    body.click()  # Klik body untuk mensimulasikan interaksi
                    time.sleep(random.randint(2, 5))  # Tunggu acak
                    actions = ActionChains(driver)
                    actions.move_to_element(body).perform()  # Scroll halaman
                    time.sleep(random.randint(5, 10))  # Lihat halaman lebih lama

                except Exception as e:
                    print(f"Error with {url}: {str(e)}")

        driver.quit()
        return jsonify({"message": f"Generated {num_requests} web traffic requests"}), 200

    elif type_traffic == "video":
        options = Options()
        options.add_argument("--headless")  # Menggunakan mode headless
        options.add_argument('--disable-gpu')  # Menghindari masalah dengan GPU di beberapa sistem
        options.add_argument('--no-sandbox')  # Menjalankan di lingkungan aman
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # User-Agent
        service = Service("./chromedriver/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        for _ in range(num_requests):
            for video_url in list_Video:
                try:
                    driver.get(video_url)
                    time.sleep(random.randint(5, 10))  # Menunggu video dimuat
                    print(f"Video Traffic to {video_url}")

                    # Simulasikan pengunjung nyata (scrolling)
                    body = driver.find_element("tag name", "body")
                    actions = ActionChains(driver)
                    actions.move_to_element(body).perform()  # Scroll video
                    time.sleep(random.randint(5, 10))  # Tonton video lebih lama

                except Exception as e:
                    print(f"Error with video {video_url}: {str(e)}")

        driver.quit()
        return jsonify({"message": f"Generated {num_requests} video traffic requests"}), 200

    return jsonify({"error": "Invalid traffic type"}), 400

if __name__ == '__main__':
    load_data()  # Memuat data dari file saat aplikasi dimulai
    app.run(debug=True, host='0.0.0.0', port=5000)  # Bind ke alamat 0.0.0.0 agar dapat diakses di jaringan