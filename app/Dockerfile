# Build Shiny Server Open Source -----------------------------
FROM buildpack-deps:bookworm AS builder

# Linux dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential cmake && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository from GitHub
RUN git clone --depth 1 --branch v1.5.23.1030 https://github.com/rstudio/shiny-server.git
# Install node
WORKDIR /shiny-server 
RUN mkdir tmp 
WORKDIR /shiny-server/tmp
RUN ../external/node/install-node.sh
ENV PATH="/shiny-server/bin:$PATH"

# Prepare, build, and install
RUN cmake -DCMAKE_INSTALL_PREFIX=/usr/local /shiny-server
RUN make
RUN mkdir /shiny-server/build
RUN /shiny-server/bin/npm ci --omit-dev
RUN make install

# Configuration file 
RUN mkdir -p /etc/shiny-server
RUN cp ../config/default.config /etc/shiny-server/shiny-server.conf

# # Application File ------------------------------------------------
FROM python:3.12-slim-bookworm AS app

# Add {shiny-server}
COPY --from=builder /usr/local/shiny-server /usr/local/shiny-server
ENV PATH="$PATH:/usr/local/shiny-server/bin"
COPY --from=builder /etc/shiny-server /etc/shiny-server
    
# Add {uv}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
ADD app /app
ADD pyproject.toml /app
ADD uv.lock /app

# Install dependencies
WORKDIR /app
RUN uv sync --locked

# Copy assets 
ADD assets ../assets

# Downgrade to non-root user 
RUN useradd -u 1000 -m shiny
USER shiny

# Command 
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]