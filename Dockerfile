# Imagen base - Python oficial (Debian)
FROM python:3.11-slim

# Metadata
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Video Downloader - TikTok y mas"

# Instalar ffmpeg para procesamiento de video
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo de la aplicacion
COPY app.py .

# Crear directorio de descargas
RUN mkdir -p /tmp/downloads

# Exponer el puerto
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]
