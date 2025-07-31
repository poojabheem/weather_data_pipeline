# Use an official Python runtime
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Default command: run scheduler
CMD ["python", "scripts/scheduler.py"]
