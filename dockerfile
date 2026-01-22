# 1. Imagen base
FROM python:3.13-slim

# 2. Variables de entorno para Python
#Le dice a Python que no genere carpetas __pycache__ ni archivos .pyc (archivos compilados).
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias del sistema 
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código de la aplicación
COPY . .

# 7. Exponer el puerto
EXPOSE 8000

# 8. Comando de arranque
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]