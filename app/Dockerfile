# Base Image
FROM python:3.12-slim

# Create and switch to the application directory
WORKDIR /app

# Copy dependency file first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Expose Flask application port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
