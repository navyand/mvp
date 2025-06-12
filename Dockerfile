FROM python:3.10-slim


WORKDIR /app

# Copia primero los archivos necesarios para instalar dependencias
COPY app/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la app
COPY app/ /app

# Comando de arranque
# CMD ["python", "main.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]

