FROM python:3.12-slim-bookworm

# User configuration
RUN useradd -u 1000 -m shiny

# Add {uv}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies
RUN mkdir /app
WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

# Copy project files
COPY app/app.py .
COPY app/www www
COPY assets ../assets

# Command 
USER shiny
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]