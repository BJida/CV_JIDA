# Dockerfile
# FROM python:3.13.3

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]

# Utilise une image officielle légère et récente
FROM python:3.13.3-slim

# Empêche l'écriture de .pyc et active le mode non bufferisé
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mise à jour des paquets système de manière sécurisée
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc libpq-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Mise à jour des outils Python pour corriger CVE setuptools/pip
RUN pip install --upgrade pip setuptools wheel

# Dossier de travail
WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l’application
COPY . .

# Lancement de l'application
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
