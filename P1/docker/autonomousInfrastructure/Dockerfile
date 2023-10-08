# Base image 
FROM python:3.11.5-slim-bullseye

# Set working directory
WORKDIR /app

# Copy app folder
COPY app/. .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy modeloSQL folder 
# Using relative path from Dockerfile location
COPY modeloSQL /app/modeloSQL

# List folder to validate files copied
RUN ls -l /app/modeloSQL

# Run app.py when container starts  
CMD [ "python", "app.py" ]