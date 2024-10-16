# Dockerfile
FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Zainstalowanie zależności systemowych
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Kopiowanie plików projektu do kontenera
COPY . /app

# Instalacja zależności Pythona
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Uruchomienie migracji bazy danych i serwera Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
