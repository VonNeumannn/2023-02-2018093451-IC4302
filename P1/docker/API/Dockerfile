FROM python:3.11.5-slim-bullseye

# Set working directory
WORKDIR /app

# Copy app folder
COPY app/. .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Correr Unittests Primero
#RUN python -u tests.py

EXPOSE 5000
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]

