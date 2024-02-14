# Stage 1: Build qBittorrent-nox
FROM ubuntu:latest AS qbittorrent-build

# Install qBittorrent-nox dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository -y ppa:qbittorrent-team/qbittorrent-stable \
    && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    qbittorrent-nox

# Stage 2: Final image with qBittorrent-nox and Python
FROM python:3.8-slim

# Copy qBittorrent-nox binaries from the previous stage
COPY --from=qbittorrent-build /usr/bin/qbittorrent-nox /usr/bin/qbittorrent-nox

# Install Python dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy Python script into the container
COPY script.py /app/script.py

# Run Python script
CMD ["python", "/app/script.py"]
