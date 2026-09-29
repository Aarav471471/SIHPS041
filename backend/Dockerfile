FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
# Create a dummy README to satisfy build tools
RUN touch README.md

RUN pip install --no-cache-dir .

COPY . .

# Expose port
EXPOSE 8000

# Command is provided by docker-compose
