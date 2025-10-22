# --- Stage 1: Build Stage ---
# Use a full Python image to install dependencies
FROM python:3.10-slim AS builder

WORKDIR /usr/src/app

# Install build dependencies
RUN pip install --upgrade pip

# Copy requirements file and install dependencies
# This creates a cached layer of our dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# --- Stage 2: Final Stage ---
# Use a minimal, secure base image
FROM python:3.10-slim AS final

WORKDIR /usr/src/app

# Create a non-root user for security
# This is a key security best practice
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY main.py .

# Change ownership to the non-root user
RUN chown -R appuser:appuser /usr/src/app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]