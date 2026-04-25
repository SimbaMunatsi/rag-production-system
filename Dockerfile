# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements and install them first (Docker caches this step for speed)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# --- THE MAGIC STEP ---
# Run the caching script. Docker will execute this, generate the .pkl file, 
# and permanently save it into the final image.
RUN python -m scripts.generate_bm25_cache

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]