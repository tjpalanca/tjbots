FROM python:3.12-slim-bookworm

# User configuration
RUN useradd -u 1000 -m shiny

# Add {shiny-server}
ENV PATH="$PATH:/usr/local/shiny-server/bin"
ENV SHINY_LOG_STDERR=1
COPY --from=ghcr.io/tjpalanca/shiny-server:latest /usr/local/shiny-server /usr/local/shiny-server
COPY --from=ghcr.io/tjpalanca/shiny-server:latest /etc/shiny-server /etc/shiny-server
RUN mkdir -p /var/lib/shiny-server/bookmarks && chown shiny /var/lib/shiny-server/bookmarks
RUN mkdir -p /var/log/shiny-server && chown shiny /var/log/shiny-server

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
COPY app/shiny-server.conf /etc/shiny-server/shiny-server.conf

# Command 
USER shiny
EXPOSE 8080
CMD ["/usr/local/shiny-server/bin/shiny-server"]