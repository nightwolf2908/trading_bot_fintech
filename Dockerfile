# ============================================
# DOCKERFILE - Trading Bot
# ============================================
# Este archivo le dice a Docker cómo construir
# la imagen de tu bot de trading.
#
# ¿QUÉ HACE?
# 1. Toma Python como base
# 2. Instala las dependencias
# 3. Copia tu código
# 4. Configura el punto de entrada
# ============================================

# ----- PASO 1: Imagen base -----
# Usamos Python 3.11 (versión ligera 'slim' para ahorrar espacio)
FROM python:3.11-slim

# ----- PASO 2: Información del mantenedor -----
LABEL maintainer="abdielitopro4800s@gmail.com"
LABEL description="Trading Bot - Sistema de Comercio Algorítmico Cuantitativo"
LABEL version="1.0.0"

# ----- PASO 3: Variables de entorno de Python -----
# PYTHONDONTWRITEBYTECODE=1 → No guarda archivos .pyc (ahorra espacio)
ENV PYTHONDONTWRITEBYTECODE=1
# PYTHONUNBUFFERED=1 → Muestra logs en tiempo real (sin buffer)
ENV PYTHONUNBUFFERED=1

# ----- PASO 4: Directorio de trabajo -----
WORKDIR /app

# ----- PASO 5: Instalar dependencias del sistema -----
# Necesarias para algunos paquetes de Python
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ----- PASO 6: Copiar e instalar dependencias de Python -----
# Primero copiamos requirements.txt (para usar caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----- PASO 7: Copiar el código fuente -----
# Copiamos TODO el código al contenedor
COPY . .

# ----- PASO 8: Crear usuario no-root (seguridad) -----
# Esto evita que el bot corra como administrador
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Comando por defecto: ejecuta el bot completo
CMD ["python", "main.py"]