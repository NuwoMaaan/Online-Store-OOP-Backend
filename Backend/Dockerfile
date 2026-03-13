
FROM python:3.14-slim AS build

# Copy the uv binary
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/bin/uv

# Set workdir and install dependencies
WORKDIR /app
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev

# Copy app and sync
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# --- Runtime Stage ---
FROM python:3.14-slim AS runtime
WORKDIR /app
COPY --from=build /app .
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "main"]
