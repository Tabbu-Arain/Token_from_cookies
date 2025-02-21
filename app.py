from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

FB_API_VERSION = os.getenv("FACEBOOK_API_VERSION", "v19.0")

# Home Page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Cookie to Token Extraction
@app.route("/extract", methods=["POST"])
def extract_token():
    data = request.get_json()
    fb_cookies = data.get("cookies")

    if not fb_cookies:
        return jsonify({"error": "No cookies provided"}), 400

    try:
        # URL of Facebook API to convert cookies to access token
        fb_url = f"https://business.facebook.com/{FB_API_VERSION}/adsmanager"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
            "Cookie": fb_cookies,  # Sending cookies in headers
        }

        response = requests.get(fb_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if request fails

        # Extracting token from the response
        if "access_token" in response.text:
            token = response.json().get("access_token")
            return jsonify({"access_token": token})
        else:
            return jsonify({"error": "Could not extract access token"}), 401

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
