# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]