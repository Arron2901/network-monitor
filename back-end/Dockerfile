# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI (with reload for dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
