# Image Python 3.11-slim
FROM python:3.11-slim AS build-stage

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
    libxrender-dev \
    python3-dev \
    python3-pip 

# Copy requirements.txt dan install dependensi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh project ke dalam container
COPY . .

# Set environment variable untuk Django
ENV PYTHONUNBUFFERED=1

# Set to 0 in production
ENV DEBUG=1

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 for Django
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]