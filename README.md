# Video Downloader - Aplicacion Docker

Aplicacion web que permite descargar videos de diferentes redes sociales como TikTok, Instagram, Twitter/X, YouTube y Facebook. Construida con Flask y yt-dlp, containerizada con Docker.

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y ejecutandose
- Git (opcional, para clonar el repositorio)

---

## Estructura del proyecto

```
sem04/
├── app.py                  # Aplicacion principal (Flask + yt-dlp)
├── requirements.txt        # Dependencias de Python
├── Dockerfile              # Dockerfile basico (Debian)
├── Dockerfile.optimizado   # Dockerfile optimizado (Alpine)
├── Dockerfile.multistage   # Dockerfile multi-stage (Alpine)
└── README.md               # Este archivo
```

---

## Paso 1: Clonar el repositorio

### En PowerShell (Windows)
```powershell
git clone https://github.com/David910512/Repo_para_descargar_videos.git
cd Repo_para_descargar_videos
```

### En Terminal / Git Bash / Linux / Mac
```bash
git clone https://github.com/David910512/Repo_para_descargar_videos.git
cd Repo_para_descargar_videos
```

---

## Paso 2: Construir las imagenes Docker

Se tienen 3 versiones de Dockerfile, cada una con diferente nivel de optimizacion.

### Version 1.0 - Basica (Debian)

**PowerShell / CMD:**
```powershell
docker build -f Dockerfile -t mi-app:v1.0 .
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker build -f Dockerfile -t mi-app:v1.0 .
```

### Version 1.1 - Optimizada (Alpine)

**PowerShell / CMD:**
```powershell
docker build -f Dockerfile.optimizado -t mi-app:v1.1-alpine .
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker build -f Dockerfile.optimizado -t mi-app:v1.1-alpine .
```

### Version 1.2 - Multi-stage (Alpine)

**PowerShell / CMD:**
```powershell
docker build -f Dockerfile.multistage -t mi-app:v1.2-multistage .
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker build -f Dockerfile.multistage -t mi-app:v1.2-multistage .
```

---

## Paso 3: Verificar las imagenes creadas

**PowerShell / CMD:**
```powershell
docker images | findstr mi-app
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker images | grep mi-app
```

Resultado esperado:
```
mi-app    v1.2-multistage   xxxxxxxxxxxx   xx minutes ago   ~312MB
mi-app    v1.1-alpine       xxxxxxxxxxxx   xx minutes ago   ~329MB
mi-app    v1.0              xxxxxxxxxxxx   xx minutes ago   ~872MB
```

---

## Paso 4: Ejecutar la aplicacion

Elegir cualquiera de las 3 versiones para ejecutar:

**PowerShell / CMD / Terminal / Git Bash:**
```powershell
docker run -p 5000:5000 mi-app:v1.0
```

O con la version Alpine:
```powershell
docker run -p 5000:5000 mi-app:v1.1-alpine
```

O con la version Multi-stage:
```powershell
docker run -p 5000:5000 mi-app:v1.2-multistage
```

> Si el puerto 5000 esta ocupado, usar otro puerto:
> ```powershell
> docker run -p 5001:5000 mi-app:v1.0
> ```

---

## Paso 5: Usar la aplicacion

1. Abrir el navegador web
2. Ir a `http://localhost:5000` (o el puerto que hayas elegido)
3. Pegar el link del video (TikTok, Instagram, YouTube, etc.)
4. Hacer clic en **"Descargar Video"**
5. El video se descargara automaticamente

---

## Comandos utiles

### Ver contenedores en ejecucion

**PowerShell / CMD:**
```powershell
docker ps
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker ps
```

### Detener un contenedor

**PowerShell / CMD / Terminal:**
```powershell
docker stop <CONTAINER_ID>
```

### Detener todos los contenedores

**PowerShell / CMD:**
```powershell
docker stop $(docker ps -q)
```

**Terminal / Git Bash / Linux / Mac:**
```bash
docker stop $(docker ps -q)
```

### Eliminar las imagenes

**PowerShell / CMD / Terminal:**
```powershell
docker rmi mi-app:v1.0 mi-app:v1.1-alpine mi-app:v1.2-multistage
```

---

## Comparacion de Dockerfiles

| Caracteristica | Dockerfile | Dockerfile.optimizado | Dockerfile.multistage |
|---|---|---|---|
| Imagen base | python:3.11-slim (Debian) | python:3.11-alpine | python:3.11-alpine |
| Tamano aprox. | ~872MB | ~329MB | ~312MB |
| Usuario no-root | No | Si | Si |
| Health check | No | Si | Si |
| Multi-stage | No | No | Si |
| Seguridad | Basica | Media | Alta |

---

## Codigo fuente

### app.py
```python
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
```

### requirements.txt
```
Flask==3.0.0
yt-dlp==2024.12.6
```

### Dockerfile (Basico - Debian)
```dockerfile
FROM python:3.11-slim

LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Video Downloader - TikTok y mas"

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /tmp/downloads

EXPOSE 5000
CMD ["python", "app.py"]
```

### Dockerfile.optimizado (Alpine)
```dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /tmp/downloads

RUN adduser -D appuser && chown -R appuser /app /tmp/downloads
USER appuser

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || exit 1
CMD ["python", "app.py"]
```

### Dockerfile.multistage (Multi-stage Alpine)
```dockerfile
# Etapa 1: Builder
FROM python:3.11-alpine AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.11-alpine
RUN apk add --no-cache ffmpeg
WORKDIR /app
COPY --from=builder /install/deps /usr/local
COPY app.py .
RUN mkdir -p /tmp/downloads && \
    adduser -D appuser && \
    chown -R appuser /app /tmp/downloads
USER appuser

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || exit 1
CMD ["python", "app.py"]
```

---

## Redes sociales soportadas

- TikTok
- Instagram (Reels, publicaciones)
- Twitter / X
- YouTube (videos, shorts)
- Facebook

---

## Autor

- **David Carhuaz** - [David910512](https://github.com/David910512)
