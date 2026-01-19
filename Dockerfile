# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
#EXPOSE 5000

# Command to run the application
#CMD ["python", "app.py"]

CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8080", "app:app"]