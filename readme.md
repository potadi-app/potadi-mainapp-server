# Setup with Docker and Docker Compose
## Prerequisites

Before starting, make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

1. **Clone repository:**
   ```bash
   git clone https://github.com/potadi-app/potadi-mainapp-server.git

2. **Build and Run the Container (with daemon)**
   ```bash
   docker-compose up -d --build

### Other Command
- build-up (with daemon):
  ```bash
  docker-compose up -d --build
- restart (with daemon):
  ```bash
  docker-compose down && docker compose up -d
- restart:
  ```bash
  docker logs -f potadiapp-web

# API Documentation
  ```bash
  http://localhost:8000/v1/docs
