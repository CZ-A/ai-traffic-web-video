# AI Traffic Generator for Web and Video

This project generates clean traffic for websites and videos using Python. It includes an API to manage URL lists and generate traffic.

## Features
- API for managing URL lists (web and video).
- Generate web traffic using `requests`.
- Simulate video views using Selenium in headless mode.

## Installation
1. Clone the repository:
git clone https://github.com/CZ-A/ai-traffic-web-video.git
cd ai-traffic-web-video-api

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py

## API Endpoints
- Add URL: `POST /add_url`
- Get URLs: `GET /get_urls`
- Add Video URL: `POST /add_video`
- Get Video URLs: `GET /get_videos`
- Generate Traffic: `POST /generate_traffic`

## License
This project is licensed under the MIT License.
