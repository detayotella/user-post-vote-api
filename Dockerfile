# Dockerfile
FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set working directory
WORKDIR /app

# Copy only pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root


# Build stage
FROM base AS builder

# Copy the rest of the application
COPY . .

# Final stage
FROM python:3.12-slim

# Copy installed packages from base stage
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy the application code
COPY --from=builder /app .

# Expose the port the app runs on
EXPOSE 8000

# Use the CMD to run the application with uvicorn
CMD ["uvicorn", "app.main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]