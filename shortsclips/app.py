from flask import Flask, jsonify, request, render_template_string, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'reels.json'

# JSON file ensure karo
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# ==================== FRONTEND (User Page) ====================
@app.route('/')
def home():
    with open(DATA_FILE, 'r') as f:
        videos = json.load(f)
    videos.reverse()

    # HTML generate karo (Bina alag file ke, ekdum simple)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reels</title>
        <style>
            *{ margin:0; padding:0; box-sizing:border-box; }
            body{ background:black; overflow:hidden; height:100vh; }
            .app{ height:100vh; overflow-y:scroll; scroll-snap-type:y mandatory; }
            .slide{ height:100vh; scroll-snap-align:start; position:relative; background:black; display:flex; justify-content:center; align-items:center; }
            video{ width:100%; height:100%; object-fit:cover; }
            .title{ position:absolute; bottom:20px; left:20px; color:white; font-size:18px; background:rgba(0,0,0,0.6); padding:10px; border-radius:10px; }
        </style>
    </head>
    <body>
        <div class="app">
    """

    if len(videos) == 0:
        html += '<div class="slide" style="color:white; text-align:center;"><h2>No Reels Yet</h2><p>Admin will add soon.</p></div>'
    else:
        for v in videos:
            html += f"""
            <div class="slide">
                <video src="{v['url']}" loop playsinline muted autoplay></video>
                <div class="title">{v['title']}</div>
            </div>
            """

    html += "</div></body></html>"
    return html

# ==================== API (User ke liye Data) ====================
@app.route('/api/get-videos')
def get_videos():
    with open(DATA_FILE, 'r') as f:
        videos = json.load(f)
    videos.reverse()
    return jsonify(videos)

# ==================== ADMIN (Merge & Add) ====================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')
        if title and url:
            with open(DATA_FILE, 'r') as f:
                videos = json.load(f)
            videos.append({'title': title, 'url': url})
            with open(DATA_FILE, 'w') as f:
                json.dump(videos, f, indent=4)
        return redirect('/admin')
    
    # GET request pe Admin Panel dikhao
    with open(DATA_FILE, 'r') as f:
        videos = json.load(f)
    
    admin_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>
        <style>
            body{ font-family:Arial; background:#111; color:white; padding:20px; }
            .box{ max-width:500px; margin:auto; background:#222; padding:20px; border-radius:10px; }
            input, button{ width:100%; padding:12px; margin:10px 0; border:none; border-radius:6px; }
            button{ background:gold; font-weight:bold; cursor:pointer; }
            .card{ background:#333; padding:10px; margin:10px 0; border-radius:6px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🔥 Admin Add Reel</h2>
            <form method="POST">
                <input type="text" name="title" placeholder="Title" required>
                <input type="text" name="url" placeholder="Video URL (mp4)" required>
                <button type="submit">Add Reel</button>
            </form>
            <hr>
            <h3>Current List</h3>
    """
    for v in videos:
        admin_html += f'<div class="card"><b>{v["title"]}</b><br><small>{v["url"][:30]}...</small></div>'
    admin_html += "</div></body></html>"
    return admin_html

if __name__ == '__main__':
    # Render ke liye PORT fix
    port = int(os.environ.get('PORT', 5000))
    print(f"✅ Server running on port {port}")
    print(f"✅ Admin Panel at: /admin")
    # Host='0.0.0.0' Render ke liye zaroori hai
    app.run(host='0.0.0.0', port=port)
