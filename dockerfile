FROM python:3

# Install OpenCV and other dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Copy the face recognition code into the container
COPY face.py /app/face.py

# Run the face recognition code when the container is started
CMD ["python", "/app/face.py"]
