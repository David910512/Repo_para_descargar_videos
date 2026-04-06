from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Downloader</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #fff;
               display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: #16213e; padding: 40px; border-radius: 15px;
                     width: 90%; max-width: 500px; text-align: center; }
        h1 { margin-bottom: 10px; font-size: 1.8rem; }
        p.sub { color: #a0a0b0; margin-bottom: 25px; }
        input[type="text"] { width: 100%; padding: 12px 15px; border: 2px solid #0f3460;
                             border-radius: 8px; background: #1a1a2e; color: #fff;
                             font-size: 1rem; margin-bottom: 15px; }
        input[type="text"]:focus { outline: none; border-color: #e94560; }
        button { background: #e94560; color: #fff; border: none; padding: 12px 30px;
                 border-radius: 8px; font-size: 1rem; cursor: pointer; width: 100%; }
        button:hover { background: #c73650; }
        .msg { margin-top: 15px; padding: 10px; border-radius: 8px; }
        .error { background: #5c1a1a; color: #ff6b6b; }
        .success { background: #1a5c2a; color: #6bff8b; }
        .platforms { color: #a0a0b0; font-size: 0.85rem; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video Downloader</h1>
        <p class="sub">Descarga videos de TikTok y mas</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Pega el link del video aqui..."
                   value="{{ url or '' }}" required>
            <button type="submit">Descargar Video</button>
        </form>
        {% if error %}
            <div class="msg error">{{ error }}</div>
        {% endif %}
        {% if success %}
            <div class="msg success">{{ success }}</div>
        {% endif %}
        <p class="platforms">Soporta: TikTok, Instagram, Twitter/X, YouTube, Facebook</p>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            return render_template_string(HTML, error="Ingresa una URL valida", url=url)

        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            "outtmpl": filepath,
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "socket_timeout": 30,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(filepath, as_attachment=True, download_name="video.mp4")
        except Exception as e:
            return render_template_string(HTML, error=f"Error al descargar: {str(e)}", url=url)

    return render_template_string(HTML)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
