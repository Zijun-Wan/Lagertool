# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if you have requirements.txt)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Run your Python app (replace app.py with your main file)
CMD ["python", "app.py"]