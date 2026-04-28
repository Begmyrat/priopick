# Use slim Python image — smaller and faster
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker caching optimization)
# If requirements don't change, Docker won't reinstall them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Start FastAPI with live reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]