# Usa la imagen base de Python 3.11.5
FROM python:3.11.5

# Copia los archivos de tu proyecto al contenedor
COPY . /app
WORKDIR /app

# Instala las dependencias desde el archivo requirements.txt
RUN pip install -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Ejecuta tu aplicación FastAPI con uvicorn
CMD ["python", "main.py"]
