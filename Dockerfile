# 1. Base Image
FROM python:3.11-slim-bookworm

# 2. Set Working Directory
WORKDIR /app

# 3. Install System Dependencies (Required for OpenCV/Ultralytics)
# This is the precise fix for Debian Trixie/Testing
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy ONLY requirements first to leverage Docker cache
COPY requirements.txt .

# 5. Optimization: Install CPU-only Torch to reduce size (from 3GB to ~700MB)
# If you need GPU, keep your current requirements but expect the long wait.
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.0 \
    torchvision==0.18.0

# 6. Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# 7. Finally, copy the rest of the project
COPY . .

# 8. Expose Streamlit port and the running the streamlit app via CMD
EXPOSE 8501

CMD ["streamlit", "run", "scripts/app/app.py", "--server.address", "0.0.0.0"]