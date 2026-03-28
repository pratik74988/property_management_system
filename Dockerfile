FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FORCE copy everything explicitly
COPY . /app

# DEBUG

RUN echo "=== CORE MIGRATIONS ==="
RUN ls -la /app/core
RUN ls -la /app/core/migrations
# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn --bind 0.0.0.0:8080 shivtej_V_0.wsgi:application"]