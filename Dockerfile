# Dockerfile for backend

# Use a Python image
FROM python:3.12.7

# Set working directory to backend folder
WORKDIR /app/backend

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend code to container
COPY . /app

# Expose the backend port
EXPOSE 5000

# Run the backend with run.py
CMD ["python", "run.py"]