# Base image 
FROM python:3.11.5-slim-bullseye

# Set working directory
WORKDIR /app

# Copy app folder
COPY app/. .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN ls

# Correr Unittests Primero
#RUN python -u tests.py

# Run app.py cuando se probaron los métodos y se inicia el contenedor 
CMD [ "python", "-u", "app.py" ]

