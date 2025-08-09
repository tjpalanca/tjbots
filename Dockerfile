FROM python:3.12-slim-bookworm

# User configuration
RUN useradd -u 1000 -m tjbots

# Add {uv}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory 
RUN mkdir /tjbots
WORKDIR /tjbots

# Install dependencies
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

# Copy project files
COPY src .

# Command 
USER tjbots
EXPOSE 8080
CMD ["tjbots-chatbot"]