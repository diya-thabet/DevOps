# 1. Base Image: Use a lightweight Python image
FROM python:3.9-slim

# 2. Working Directory: Set the folder inside the container
WORKDIR /app

# 3. Copy Dependencies: Copy only requirements first to cache them
COPY requirements.txt .

# 4. Install Dependencies: Run pip install
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Code: Copy the rest of the application code
COPY . .

# 6. Expose Port: Tell Docker we listen on port 8000
EXPOSE 8000

# 7. Command: How to run the app
# "app.main:app" tells uvicorn where to look for the FastAPI instance
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]