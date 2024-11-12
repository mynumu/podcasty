FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p /app/static/audio
RUN mkdir -p /app/data/audio/tmp

# Expose the port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api.index:app"]