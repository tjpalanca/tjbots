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

# Command 
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]