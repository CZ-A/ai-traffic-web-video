from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time

app = Flask(__name__)

# Konfigurasi Selenium WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opsi headless untuk berjalan tanpa GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Sesuaikan path driver jika diperlukan
    driver_path = os.getenv("CHROME_DRIVER_PATH", "chromedriver")
    return webdriver.Chrome(service=ChromeService(driver_path), options=chrome_options)

@app.route("/process", methods=["POST"])
def process_video():
    try:
        # Ambil URL dari request JSON
        data = request.get_json()
        if "url" not in data:
            return jsonify({"error": "URL is required"}), 400

        url = data["url"]
        driver = get_driver()

        # Buka halaman yang diberikan
        driver.get(url)
        time.sleep(5)  # Tunggu hingga halaman termuat

        # Ambil elemen video jika ada
        video_elements = driver.find_elements(By.TAG_NAME, "video")
        if not video_elements:
            return jsonify({"error": "No video elements found on the page"}), 404

        video_urls = []
        for video in video_elements:
            video_src = video.get_attribute("src")
            if video_src:
                video_urls.append(video_src)

        driver.quit()
        return jsonify({"videos": video_urls}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the video processing API!",
        "endpoints": {
            "/process": "POST a URL to extract video links"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
