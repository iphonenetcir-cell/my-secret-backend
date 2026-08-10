from flask import Flask, jsonify
import requests
import os
import base64

app = Flask(__name__)

# ✅ नया Google Sheet CSV लिंक (जो आपने आज Publish किया था)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTlllkrfjfOeVwH2sX2bsQDYIOxlVWaItjIyOV96xRQbl85AATy4L3zIqfisr-8LnZYPF0s8bzRjX8N/pub?output=csv"

# ⚡ एन्क्रिप्शन फंक्शन (Base64)
def encrypt(text):
    return base64.b64encode(text.encode()).decode()

@app.route('/api/get-videos', methods=['GET'])
def get_videos():
    try:
        response = requests.get(SHEET_CSV_URL)
        csv_text = response.text
        rows = csv_text.strip().split('\n')
        
        videos = []
        # पहली लाइन (Header) को छोड़ें
        for row in rows[1:]:
            cols = row.split(',')
            if len(cols) >= 2:
                title = cols[0].strip()
                url = cols[1].strip()
                if url:
                    # URL को एन्क्रिप्ट करें
                    encrypted_url = encrypt(url)
                    videos.append({
                        'title': title,
                        'encrypted_url': encrypted_url
                    })
        return jsonify(videos)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
