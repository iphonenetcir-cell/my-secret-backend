from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# आपका Google Sheet का सही CSV लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTlllkrfjfOeVwH2sX2bsQDYIOxlVWaItjIyOV96xRQbl85AATy4L3zIqfisr-8LnZYPF0s8bzRjX8N/pub?output=csv"

# ==================== USER API (Data Fetch) ====================
@app.route('/api/get-videos', methods=['GET'])
def get_videos():
    try:
        # Google Sheet से CSV डेटा fetch करें
        response = requests.get(SHEET_CSV_URL)
        csv_text = response.text
        
        # CSV को पार्स करके JSON में बदलें
        rows = csv_text.strip().split('\n')
        
        videos = []
        # पहली लाइन (Header) को छोड़कर, बाकी लाइनें पढ़ें
        for row in rows[1:]:
            cols = row.split(',')
            if len(cols) >= 2:
                title = cols[0].strip()
                url = cols[1].strip()
                
                # अगर URL खाली नहीं है, तो इसे लिस्ट में डालें
                if url:
                    videos.append({
                        'title': title,
                        'url': url
                    })
                    
        return jsonify(videos)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([])

# ==================== ROOT Route ====================
@app.route('/')
def home():
    return "Backend is running successfully with Google Sheets!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
