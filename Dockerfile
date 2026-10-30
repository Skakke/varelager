FROM python:3.14-slim

# Henter uv (pakkehåndtereren prosjektet bruker)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Installerer avhengighetene først, så Docker kan cache dette laget
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# Kopierer resten av appen, inkludert database.db
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
