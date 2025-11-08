## URL shortener

### Functional requirements
1. Users should be able to submit a long URL and receive a shortened version.
1. Users should be able to access the original URL by using the shortened URL.

### Non-Functional Requirements
1. The system should ensure uniqueness for the short codes (no two long URLs can map to the same short URL)
1. The redirection should occur with minimal delay

### Architecture
* [Architecture Decision Records](doc/adr)
* Domain Driven Design  
* Ports and Adapters

### Development approach
* Python
* FastAPI
* uv - python package and project manager
* ruff - python linter and code formatter
* pytest
* testcontainers

## Build the repo

1. Install `uv`: https://docs.astral.sh/uv/getting-started/installation/
2. Run `uv sync`

### Running locally

* Add a `.env` file with the contents: `DATABASE_URL=postgresql+asyncpg://urls_user:urls_pass@localhost:5432/url_shortener_db`
* Start the necessary docker containers: `docker-compose up -d`
* Run the FastAPI application locally: `.venv/bin/fastapi run src/main.py`
* Navigate to http://localhost:8000/docs in your browser to verify that the app is running correctly.

### Running the full service via Docker Compose

* Add a `.env` file with the contents: `DATABASE_URL=postgresql+asyncpg://urls_user:urls_pass@localhost:5432/url_shortener_db`
* Run with docker compose: `docker compose -f docker-compose.yml -f url-shortener-sevice.yml up --build -d`
* Navigate to http://localhost:8000/docs in your browser to verify that the app is running correctly.