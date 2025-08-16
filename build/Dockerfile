FROM python:3.12-slim-bookworm

# User configuration
RUN useradd -u 1000 -m tjbots

# Add {shiny-server}
ENV PATH="$PATH:/usr/local/shiny-server/bin"
ENV SHINY_LOG_STDERR=1
COPY --from=ghcr.io/tjpalanca/shiny-server:latest /usr/local/shiny-server /usr/local/shiny-server
RUN mkdir -p /etc/shiny-server 
COPY build/shiny-server.conf /etc/shiny-server
RUN mkdir -p /var/lib/shiny-server/bookmarks && chown tjbots /var/lib/shiny-server/bookmarks
RUN mkdir -p /var/log/shiny-server && chown tjbots /var/log/shiny-server

# Add {uv}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory 
RUN mkdir /tjbots
WORKDIR /tjbots

# Install dependencies
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked --only-group app

# Copy project files
COPY assets assets
COPY src src

# Command 
USER tjbots
EXPOSE 8080
CMD ["shiny-server"]