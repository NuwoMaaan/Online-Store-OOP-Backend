# Use a slim Python image
FROM python:3.11-slim

# Avoid buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Create app dir and set it as working dir
WORKDIR /app

# Install OS packages needed (if any). Keep minimal.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for layer caching
COPY Backend/requirements.txt ./requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY Backend/ ./

# Set a non-root user (optional)
# RUN useradd --create-home appuser
# USER appuser

# Default command: run the CLI app
# Use -it when running to allow interactive input
CMD ["python", "main.py"]