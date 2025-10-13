# Multi-stage build for optimized image size
FROM python:3.12-slim as builder

WORKDIR /app

# Install uv for faster dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Production image
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment and code from builder
COPY --from=builder /app/.venv /app/.venv
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "server.py"]