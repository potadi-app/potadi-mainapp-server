#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Fungsi untuk menunggu database siap sebelum melanjutkan
wait_for_db() {
  echo "Waiting for database to be ready..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
  done
}

# Menunggu database siap sebelum melanjutkan
if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
  wait_for_db
fi

# Jalankan perintah makemigrations jika ada perubahan pada model
echo "Running migrations..."
python manage.py migrate --noinput

# Jalankan collectstatic untuk mengumpulkan file statis
if [ "$DEBUG" = "0" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

# Menjalankan perintah Gunicorn (atau perintah lainnya) yang dikirimkan ke container
exec "$@"
