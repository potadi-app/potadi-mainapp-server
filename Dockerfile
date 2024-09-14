# Gunakan image Python 3.11-slim sebagai basis
FROM python:3.11-slim

# Set working directory dalam container
WORKDIR /app

# Install netcat untuk keperluan wait-for-db
RUN apt-get update && \
    apt-get install -y \
    netcat-openbsd \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

# Copy requirements.txt dan install dependensi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to disable oneDNN custom operations
ENV TF_ENABLE_ONEDNN_OPTS=0

# Copy seluruh project ke dalam container
COPY . .

# Set environment variable untuk Django
ENV PYTHONUNBUFFERED 1
# Ubah menjadi 0 untuk produksi
ENV DEBUG 1

# Salin entrypoint.sh dan berikan hak akses eksekusi
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port untuk Django
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]