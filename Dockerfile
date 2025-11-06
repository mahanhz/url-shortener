FROM python:3.12-slim

# Install compiler, headers, and PostgreSQL client libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . .

# Install the application dependencies.
WORKDIR .
RUN uv sync --frozen --no-cache

# Run the application.
CMD [".venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]
