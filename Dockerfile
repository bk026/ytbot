FROM python:3.11-slim

# Install ffmpeg (required by yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg gcc build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r app/requirements.txt

COPY app /app

RUN mkdir -p /tmp/ytbot
ENV TEMP_DIR=/tmp/ytbot

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
