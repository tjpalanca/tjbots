FROM python:3.12-bookworm

# Add {uv}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
ADD app /app
ADD pyproject.toml /app
ADD uv.lock /app

# Install dependencies
WORKDIR /app
RUN uv sync --locked

# Downgrade to non-root user 
RUN useradd -u 1000 -m appuser
USER appuser

# Command 
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]